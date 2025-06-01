from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
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
    return render_template('index.html', title='Home', user=user, posts=posts)