from flask import flash, render_template, Flask, request, redirect, Blueprint

app=Flask(__name__, template_folder='templates')
app=Blueprint('iplookup', __name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/ip-lookup', methods=['GET', 'POST'])
def iplookup(IP):
        return IP==request.form['IP']
