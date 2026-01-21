from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import html
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "devkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    try:
        db.create_all()  # vytvoří tabulku Feedback
        print("Připojení k SQL Serveru OK")
    except Exception as e:
        print("Chyba připojení:", e)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)


class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = html.escape(request.form.get("name", "").strip())
        email = html.escape(request.form.get("email", "").strip())
        message = html.escape(request.form.get("message", "").strip())

        if not name or not email or not message:
            flash("Vyplň všechna pole")
            return redirect(url_for("index"))

        feedback = Feedback(name=name, email=email, message=message)
        db.session.add(feedback)
        db.session.commit()

        flash("Zpráva uložena")
        return redirect(url_for("index"))

    feedbacks = Feedback.query.all()
    return render_template("index.html", feedbacks=feedbacks)


@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    if request.method == "POST":
        city = html.escape(request.form.get("city", "").strip())
        if city:
            # Mock weather data
            weather_data = {
                "city": city,
                "temperature": "20°C",
                "description": "Sunny"
            }
        else:
            flash("Zadej město")
    return render_template("weather.html", weather=weather_data)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_file = UploadedFile(filename=filename, original_filename=file.filename)
            db.session.add(uploaded_file)
            db.session.commit()
            flash('File uploaded successfully')
            return redirect(url_for('upload'))
    files = UploadedFile.query.all()
    return render_template("upload.html", files=files)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/selection")
def selection():
    options = ["Option 1", "Option 2", "Option 3"]
    selected = request.args.get('selected')
    return render_template("selection.html", options=options, selected=selected)


if __name__ == "__main__":
    app.run(debug=True)
