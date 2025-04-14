from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import time
import os

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgresql://userdata_rigq_user:UwIgIHpQ3GeZE2ybxQu0OG9bZJzobXBA@dpg-cvugfbq4d50c73av8gr0-a/userdata_rigq')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        wants_json = request.accept_mimetypes['application/json']
        
        name = request.form['name']
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Username already exists. Please choose a different one.'
                })
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists. Please choose a different one.'
                })
            flash('Email already exists. Please choose a different one')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(name=name, username=username, email=email, password=hashed_password)
            
        db.session.add(new_user)
        db.session.commit()
            
        if wants_json:
            return jsonify({
                'success': True,
                'message': 'Account Created Successfully, Please Login!',
                'redirect': url_for('login')  
            })
        flash('Account Created Successfully, Please Login!')
        return redirect(url_for('login'))  

    return render_template('register.html', time=int(time.time()))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wants_json = request.accept_mimetypes['application/json']
        email = request.form.get('email', '').lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if not user:
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Email has not been registered.',
                    'redirect': None
                })
            flash('Email has not been registered.', 'danger')
            return redirect(url_for('login'))

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            if wants_json:
                return jsonify({
                    'success': False,
                    'message': 'Incorrect password entered.',
                    'redirect': None
                })
            flash('Incorrect password entered.', 'danger')
            return redirect(url_for('login'))

        session.permanent = True
        session['user_id'] = user.id
        session['name'] = user.name
        session['last_active'] = int(time.time())
        
        if wants_json:
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'redirect': url_for('dashboard')
            })
        return redirect(url_for('dashboard'))

    return render_template('login.html', time=int(time.time()))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'name' in session:
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('login'))

@app.route('/save', methods=['POST'])
def save_story():
    name = request.form['name']
    title = request.form['title']
    content = request.form['content']
    if name and title and content:
        new_story = Story(name=name, title=title, content=content)
        db.session.add(new_story)
        db.session.commit()
    return redirect(url_for('StoryHome'))

@app.route('/story/<int:story_id>')
def ViewStory(story_id):
    story = Story.query.get_or_404(story_id)
    return render_template('ViewStory.html', story=story)

@app.route('/StoryHome')
def StoryHome():
    stories = Story.query.all()
    return render_template('StoryHome.html', stories=stories)

@app.route('/WriteStory')
def WriteStory():
    return render_template('WriteStory.html')

@app.route('/Englishquizselection')
def Englishquizselection():
    return render_template('Englishquizselection.html')

@app.route('/Verbsquestions')
def Verbsquestions():
    return render_template('Verbsquestions.html')

@app.route('/Tensesquestions')
def Tensesquestions():
    return render_template('Tensesquestions.html')

@app.route('/Nounsquestions')
def Nounsquestions():
    return render_template('Nounsquestions.html')

@app.route('/Sciencequizselection')
def Sciencequizselection():
    return render_template('Sciencequizselection.html')

@app.route('/EasySciencequestions')
def EasySciencequestions():
    return render_template('EasySciencequestions.html')

@app.route('/MediumSciencequestions')
def MediumSciencequestions():
    return render_template('MediumSciencequestions.html')

@app.route('/HardSciencequestions')
def HardSciencequestions():
    return render_template('HardSciencequestions.html')

@app.route('/Mathsquizselection')
def Mathsquizselection():
    return render_template('Mathsquizselection.html')

@app.route('/EasyMathsquestions')
def EasyMathsquestions():
    return render_template('EasyMathsquestions.html')

@app.route('/MediumMathsquestions')
def MediumMathsquestions():
    return render_template('MediumMathsquestions.html')

@app.route('/HardMathsquestions')
def HardMathsquestions():
    return render_template('HardMathsquestions.html')

@app.route('/Geographyquizselection')
def Geographyquizselection():
    return render_template('Geographyquizselection.html')

@app.route('/EasyGeographyquestions')
def EasyGeographyquestions():
    return render_template('EasyGeographyquestions.html')

@app.route('/MediumGeographyquestions')
def MediumGeographyquestions():
    return render_template('MediumGeographyquestions.html')

@app.route('/HardGeographyquestions')
def HardGeographyquestions():
    return render_template('HardGeographyquestions.html')

@app.route('/GKquizselection')
def GKquizselection():
    return render_template('GKquizselection.html')

@app.route('/EasyGKquestions')
def EasyGKquestions():
    return render_template('EasyGKquestions.html')

@app.route('/MediumGKquestions')
def MediumGKquestions():
    return render_template('MediumGKquestions.html')

@app.route('/HardGKquestions')
def HardGKquestions():
    return render_template('HardGKquestions.html')

@app.route('/Historyquizselection')
def Historyquizselection():
    return render_template('Historyquizselection.html')

@app.route('/EasyHistoryquestions')
def EasyHistoryquestions():
    return render_template('EasyHistoryquestions.html')

@app.route('/MediumHistoryquestions')
def MediumHistoryquestions():
    return render_template('MediumHistoryquestions.html')

@app.route('/HardHistoryquestions')
def HardHistoryquestions():
    return render_template('HardHistoryquestions.html')

@app.route('/GuessTheFlagQuiz')
def GuessTheFlagQuiz():
    return render_template('GuessTheFlagQuiz.html')

@app.route('/GuessTheFoodQuiz')
def GuessTheFoodQuiz():
    return render_template('GuessTheFoodQuiz.html')

@app.route('/DemoQuiz')
def DemoQuiz():
    return render_template('DemoQuiz.html')

@app.route('/DemoQuizResult')
def DemoQuizResult():
    return render_template('DemoQuizResult.html')

@app.route('/Result')
def Result():
    return render_template('result page.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacy policy.html')

@app.route('/termsofuse')
def termsofuse():
    return render_template('terms of use.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)