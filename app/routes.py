from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user
import sqlalchemy as sa

from app import app, db
from app.models import User
from app.forms import LoginForm, SignupForm
from config import Config

from openai import OpenAI


client = OpenAI(
    base_url=app.config['OPENROUTER_BASE_URL'],
    api_key=app.config['OPENROUTER_API_KEY'],
)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'drug': {'username': 'Asprin'},
            'content': 'Aspirin is a medication used to reduce pain, fever, or inflammation.'
        },
        {
            'drug': {'username': 'Ibuprofen'},
            'content': 'Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to reduce fever, pain, and inflammation.'
        },
        {
            'drug': {'username': 'Paracetamol'},
            'content': 'Paracetamol, also known as acetaminophen, is a medication used to treat pain and fever.'
        }
    ]

    drug_interactions = None
    searched_drug_name = None

    if request.method == 'POST':
        searched_drug_name = request.form.get('drug_name')
        if searched_drug_name:
            try:
                prompt = f"What are the major drug interactions for {searched_drug_name}? Provide a short answer in list format."
                completion = client.chat.completions.create(
                    model=app.config['OPENROUTER_MODEL'],
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                drug_interactions = completion.choices[0].message.content
            except Exception as e:
                flash(f"Error fetching drug interactions: {e}", "danger") # Using flash for user feedback
                drug_interactions = "Could not retrieve interactions at this time."

    else:
            flash("Please enter a drug name.", "warning")

    return render_template('index.html', 
                           title='Home', 
                           user=user, 
                           posts=posts, 
                           drug_interactions=drug_interactions,
                           searched_drug_name=searched_drug_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('signup'))
        flash(f'Signup requested for user {form.username.data} with email {form.email.data}')
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)
