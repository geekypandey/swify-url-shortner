import os
import string

from flask import Flask,render_template,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'uKUAvkuscabZjkas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
base62 = list(string.digits + string.ascii_lowercase + string.ascii_uppercase)

class Mapping(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    long_url = db.Column(db.String(200),nullable=False)
    short_url = db.Column(db.String(200),nullable=False)

class UrlForm(FlaskForm):
    url = StringField('Enter your url here:')
    submit = SubmitField('Submit')

@app.before_first_request
def create_db():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def index():
    form = UrlForm()
    if form.validate_on_submit():
        long_url = form.url.data
        last_id = len(Mapping.query.all())
        #logic for short url
        rem = []
        while True:
            remainder = last_id%62
            rem.append(base62[remainder])
            last_id = int(last_id/62)
            if last_id == 0:
                break
        rem.reverse()
        short_url = ''.join(rem)
        entry = Mapping(long_url=long_url,short_url=short_url)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('show_url',short_url=entry.short_url))
    return render_template('index.html',form=form)


@app.route('/short_url/<string:short_url>')
def show_url(short_url):
    host = request.headers.get('host')
    url = f'{host}/{short_url}'
    return render_template('short_url.html',url=url)

@app.route('/<string:short_url>')
def url_redirect(short_url):
    result = Mapping.query.filter_by(short_url=short_url).first()
    if result is None:
        return '<h2>No such url found</h2>'
    return redirect(f'http://{result.long_url}')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
