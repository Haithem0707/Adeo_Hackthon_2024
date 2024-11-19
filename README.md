# 🌟 InnovateAI: Streamlining Internal Workflows Hackathon 🚀

## Project Title: **[Insert Your Project Title Here]**

---

## 📜 **Problem Statement**

### **Challenge 1: Streamlining Internal Opinion Request Processes**
The current process for handling internal opinion requests is **fragmented** and **inefficient**, leading to:
- Inconsistent responses between departments.
- Duplicate efforts and lack of standardized formats for analyzing and summarizing opinions.

The goal is to create a **unified system** that streamlines this process and ensures consistency across all departments. 💼

### **Challenge 2: Automating & Centralizing Research and Benchmarking for Key Topics**
Teams spend excessive time **manually researching** key topics, sifting through multiple sources to find relevant best practices, benchmarks, and trends. This results in:
- **Inefficiencies** and **information gaps**.
- **Duplicated research efforts** across teams.

This challenge aims to **automate** and **centralize** research, saving valuable time and improving information accuracy. 📊

---

## 💡 **Solution Overview**
This project addresses both challenges by developing a **unified platform** that:
- **Automates** the collection and analysis of internal opinion requests 📝.
- **Centralizes** research and benchmarking processes, enabling faster access to relevant information 🔍.

---

## 🛠️ **Reasoning Behind Technical Choices**

### **Technology Stack**:
- **Backend**: Flask 🐍  
- **AI Integration**: OpenAI (can be replaced with a local AI solution) 🤖  
- **Frontend**: HTML5, CSS3, JavaScript (React or vanilla JS) 🌐  
- **Deployment**: Nginx for serving static files and reverse proxying the Flask app 🔄  

### **Why These Tools**:
- **Flask**: Flask was chosen for its simplicity and flexibility, allowing us to quickly set up a lightweight backend to handle requests and integrate easily with OpenAI’s API or a local AI solution.
- **OpenAI**: OpenAI was used to leverage its powerful language models to automate and streamline opinion request analysis and research. However, you can replace OpenAI with a **local AI solution** if you prefer to host your own models or avoid external API calls.
- **HTML, CSS, JavaScript**: These frontend technologies were chosen for their wide usage, simplicity, and flexibility in designing a user-friendly interface and ensuring smooth interactions with the backend.
- **Nginx**: Nginx is used for handling static file serving and acting as a reverse proxy for Flask, improving performance and enabling production deployment.

### **Trade-offs**:
Given the limited time frame, we focused on building a functional prototype that covers core features, rather than implementing extensive features like advanced data visualization or offline functionalities. If we had more time, we would have enhanced the UI with interactive data visualizations and deeper integration with other enterprise tools.

---

## 📂 **File Structure**
```plaintext
apps/                  # Contains the Flask backend code and logic
  ├── app.py           # Main Flask app to handle backend routes
  ├── models/          # AI models or local AI integration
  ├── templates/       # Jinja2 templates for HTML rendering
  ├── static/          # Static files (CSS, JavaScript, images)
  └── tests/           # Unit and integration tests for the backend

media/                 # Media files (images, PDFs, documents) uploaded by users

nginx/                 # Nginx configuration for deployment
  ├── nginx.conf       # Nginx configuration file for serving static files and reverse proxy
  └── Dockerfile       # Dockerfile for setting up Nginx in a container

requirements.txt       # Python dependencies for Flask and OpenAI integration
run.py                 # Entry point to run the Flask application
