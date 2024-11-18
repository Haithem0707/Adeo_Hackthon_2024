from google.cloud import firestore
from datetime import datetime
from typing import List, Dict, Optional

class FirebaseService:
    def __init__(self, project_id: str):
        self.db = firestore.Client(project=project_id)
    
    def save_chat_message(self, session_id: str, message: Dict) -> str:
        """Save a chat message to Firebase"""
        try:
            chat_ref = self.db.collection('chats').document(session_id)
            messages_ref = chat_ref.collection('messages')
            
            # Add timestamp
            message['timestamp'] = datetime.now()
            
            # Add message to Firebase
            message_ref = messages_ref.add(message)[1]
            
            # Update chat metadata
            chat_ref.set({
                'last_updated': datetime.now(),
                'status': 'active'
            }, merge=True)
            
            return message_ref.id
            
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            raise
    
    def get_chat_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get chat history for a session"""
        try:
            messages_ref = (self.db.collection('chats')
                          .document(session_id)
                          .collection('messages')
                          .order_by('timestamp')
                          .limit(limit))
            
            messages = []
            for msg in messages_ref.stream():
                message_data = msg.to_dict()
                message_data['id'] = msg.id
                messages.append(message_data)
                
            return messages
            
        except Exception as e:
            print(f"Error getting chat history: {str(e)}")
            raise

    def save_analysis_history(self, session_id: str, analysis_data: Dict) -> str:
        """
        Save analysis results to Firebase with enhanced metadata and organization
        """
        try:
            # Create references
            analysis_ref = self.db.collection('analysis_history').document(session_id)
            results_ref = analysis_ref.collection('results')

            # Prepare metadata
            timestamp = datetime.now()
            
            # Structure the analysis record
            analysis_record = {
                'timestamp': timestamp,
                'analysis_data': analysis_data,
                'metadata': {
                    'session_id': session_id,
                    'analysis_type': self._determine_analysis_type(analysis_data),
                    'department': analysis_data.get('metadata', {}).get('department', 'general'),
                    'created_at': timestamp,
                    'status': 'completed',
                    'version': '1.0'
                },
                'search_data': {
                    'keywords': self._extract_keywords(analysis_data),
                    'topics': self._extract_topics(analysis_data),
                    'summary': self._extract_summary(analysis_data)
                },
                'metrics': {
                    'content_length': len(str(analysis_data)),
                    'processing_time': self._calculate_processing_time(analysis_data),
                    'confidence_score': self._extract_confidence_score(analysis_data)
                }
            }

            # Add to Firebase
            result_ref = results_ref.add(analysis_record)[1]

            # Update session metadata
            analysis_ref.set({
                'last_updated': timestamp,
                'total_analyses': firestore.Increment(1),
                'latest_analysis_id': result_ref.id,
                'status': 'active',
                'summary_metrics': {
                    'total_documents': firestore.Increment(1),
                    'last_analysis_type': analysis_record['metadata']['analysis_type'],
                    'departments_analyzed': firestore.ArrayUnion([analysis_record['metadata']['department']])
                }
            }, merge=True)

            return result_ref.id

        except Exception as e:
            print(f"Error saving analysis history: {str(e)}")
            raise

    def get_analysis_history(
        self,
        session_id: str,
        limit: int = 50,
        department: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
        ) -> List[Dict]:
        """
        Get analysis history with filtering options
        """
        try:
            # Start with base query
            query = self.db.collection('analysis_history')\
                         .document(session_id)\
                         .collection('results')\
                         .order_by('timestamp', direction=firestore.Query.DESCENDING)

            # Apply filters if provided
            if department:
                query = query.where('metadata.department', '==', department)
            if date_from:
                query = query.where('timestamp', '>=', date_from)
            if date_to:
                query = query.where('timestamp', '<=', date_to)

            # Apply limit
            query = query.limit(limit)

            # Execute query and format results
            analyses = []
            for doc in query.stream():
                analysis_data = doc.to_dict()
                analysis_data['id'] = doc.id
                analyses.append(analysis_data)

            return analyses

        except Exception as e:
            print(f"Error getting analysis history: {str(e)}")
            raise

    def get_analysis_summary(self, session_id: str) -> Dict:
        """
        Get summary statistics for all analyses in a session
        """
        try:
            summary_ref = self.db.collection('analysis_history').document(session_id)
            summary = summary_ref.get()

            if not summary.exists:
                return {
                    "status": "not_found",
                    "message": "No analysis history found for this session"
                }

            return summary.to_dict()

        except Exception as e:
            print(f"Error getting analysis summary: {str(e)}")
            raise

    def delete_analysis(self, session_id: str, analysis_id: str) -> Dict:
        """
        Delete a specific analysis from history
        """
        try:
            analysis_ref = self.db.collection('analysis_history')\
                             .document(session_id)\
                             .collection('results')\
                             .document(analysis_id)

            analysis_ref.delete()

            return {
                "status": "success",
                "message": f"Analysis {analysis_id} deleted successfully"
            }

        except Exception as e:
            print(f"Error deleting analysis: {str(e)}")
            raise

    def _determine_analysis_type(self, analysis_data: Dict) -> str:
        """Determine the type of analysis from the data"""
        if 'model' in analysis_data:
            return analysis_data['model']
        return 'unknown'

    def _extract_keywords(self, analysis_data: Dict) -> List[str]:
        """Extract keywords from analysis data"""
        try:
            if 'technicalAnalysis' in analysis_data:
                return analysis_data['technicalAnalysis']['keywordAnalysis']['criticalTerms']
            return []
        except:
            return []

    def _extract_topics(self, analysis_data: Dict) -> List[str]:
        """Extract topics from analysis data"""
        try:
            if 'technicalAnalysis' in analysis_data:
                return analysis_data['technicalAnalysis']['topicClassification']['primaryTopics']
            return []
        except:
            return []

    def _extract_summary(self, analysis_data: Dict) -> str:
        """Extract summary from analysis data"""
        try:
            if 'executiveSummary' in analysis_data:
                return analysis_data['executiveSummary']['briefOverview']
            return ""
        except:
            return ""

    def _calculate_processing_time(self, analysis_data: Dict) -> float:
        """Calculate processing time if available"""
        try:
            if 'metadata' in analysis_data and 'processingMetrics' in analysis_data['metadata']:
                return analysis_data['metadata']['processingMetrics'].get('processingTime', 0.0)
            return 0.0
        except:
            return 0.0

    def _extract_confidence_score(self, analysis_data: Dict) -> float:
        """Extract confidence score from analysis data"""
        try:
            if 'metadata' in analysis_data:
                return analysis_data['metadata'].get('confidenceScore', 0.0)
            return 0.0
        except:
            return 0.0