# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

# Sample data for demonstration purposes
data = {
    'requests': [
        {
            'id': 1,
            'name': 'AI Research Proposal',
            'status': 'completed',
            'link': 'https://example.com/ai-research-proposal.pdf',
            'description': 'A comprehensive proposal on the integration of AI in healthcare.',
            'type': 'PDF Document',
            'category': 'Research',
            'date': '2023-01-10'
        },
        {
            'id': 2,
            'name': 'Sustainability Initiative Presentation',
            'status': 'completed',
            'link': 'https://example.com/sustainability-initiative.pptx',
            'description': 'A presentation on sustainable practices and initiatives.',
            'type': 'PowerPoint Presentation',
            'category': 'Presentations',
            'date': '2023-02-15'
        },
        {
            'id': 3,
            'name': 'Digital Transformation Strategy Document',
            'status': 'in progress',
            'link': 'https://example.com/digital-transformation-strategy.docx',
            'description': 'A strategy document outlining steps for digital transformation in businesses.',
            'type': 'Word Document',
            'category': 'Strategy',
            'date': '2023-03-05'
        },
        {
            'id': 4,
            'name': 'Healthcare Innovations Report',
            'status': 'completed',
            'link': 'https://example.com/healthcare-innovations.pdf',
            'description': 'A report on the latest innovations in healthcare technology.',
            'type': 'PDF Document',
            'category': 'Reports',
            'date': '2023-04-20'
        },
        {
            'id': 5,
            'name': 'Urban Planning Strategies',
            'status': 'completed',
            'link': 'https://example.com/urban-planning.docx',
            'description': 'Strategies for effective urban planning to create sustainable cities.',
            'type': 'Word Document',
            'category': 'Urban Development',
            'date': '2023-05-12'
        },
        {
            'id': 6,
            'name': 'The Future of Work Article',
            'status': 'completed',
            'link': 'https://example.com/future-of-work-article.pdf',
            'description': 'An article discussing how work is changing in the digital age.',
            'type': 'PDF Document',
            'category': 'Articles',
            'date': '2023-06-01'
        },
        {
            'id': 7,
            'name': 'Climate Change and Its Impact Study',
            'status': 'completed',
            'link': 'https://example.com/climate-change-study.pdf',
            'description': 'A study on climate change, its causes, and effects on the environment.',
            'type': 'PDF Document',
            'category': 'Research',
            'date': '2023-07-15'
        },
        {
            'id': 8,
            'name': 'Blockchain Technology Overview',
            'status': 'completed',
            'link': 'https://example.com/blockchain-overview.docx',
            'description': 'An overview of blockchain technology and its applications.',
            'type': 'Word Document',
            'category': 'Technology',
            'date': '2023-08-10'
        },
        {
            'id': 9,
            'name': 'Data Privacy Guidelines',
            'status': 'completed',
            'link': 'https://example.com/data-privacy-guidelines.pdf',
            'description': 'Guidelines for protecting personal information in the digital age.',
            'type': 'PDF Document',
            'category': 'Guidelines',
            'date': '2023-09-05'
        },
        {
            'id': 10,
            'name': 'AI Ethics Discussion Paper',
            'status': 'completed',
            'link': 'https://example.com/ai-ethics-paper.docx',
            'description': 'A discussion on the ethical implications of artificial intelligence.',
            'type': 'Word Document',
            'category': 'Ethics',
            'date': '2023-10-01'
        },
    ],
}

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html')


@blueprint.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    results = []

    # Search through requests
    for req in data['requests']:
        if query and query.lower() in req['name'].lower():
            results.append(req)

    return render_template('home/search_results.html', query=query, results=results)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500
