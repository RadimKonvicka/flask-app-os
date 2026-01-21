# Feedback App

Simple web application with feedback, weather, file upload, and selection features.

## Features
- Feedback form with validation
- Weather lookup (mock)
- File upload and download
- Selection form

## Setup
1. Clone the repo
2. Copy env.example to .env and fill in values
3. Install dependencies: pip install -r requirements.txt
4. Run migrations: flask db upgrade
5. Run app: python app.py

## Docker
Build: docker build -t feedback-app .
Run: docker run -p 5000:5000 feedback-app

## Kubernetes
Apply: kubectl apply -f k8s/