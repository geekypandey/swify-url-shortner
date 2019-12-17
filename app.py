from flask import Flask,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ssshhh!!!'
#make use of sqlite database here

class UrlForm(FlaskForm):
    url = StringField('Enter your url here:')
    submit = SubmitField('Submit')

@app.route('/',methods=['POST','GET'])
def index():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        #shorten the url and save it in database
        #return the link of the shorter url
    return render_template('index.html',form=form)

@app.route('/<string:url>')
def url_redirect(url):
    #redirect the user to the long-url
    return f'<h2>{url}</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
