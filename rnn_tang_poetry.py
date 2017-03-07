from flask import Flask, url_for, render_template, request, flash, redirect, jsonify #, session
from werkzeug.utils import secure_filename
import os

import threading
import subprocess
import uuid

app =Flask(__name__)

background_scripts = {}
result = {}

def run_evaluation(id, num):
    result[id] = subprocess.check_output(['./sample.py',
        '-n', num]).decode('utf-8')
    poems = result[id].split(u'][') # split into poems
    poems[0] = poems[0][1:] # get rid of the first '['
    poems[-1] = poems[-1][:poems[-1].index(u']')] # get rid of the last ']'
    result[id] = poems
    background_scripts[id] = True

# manager = Manager(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        num = request.form['num']
        return redirect(url_for('evaluate', num=num))
    else:
        return render_template('index.html')

@app.route('/evaluate/<num>')
def evaluate(num):
    id = str(uuid.uuid4())
    background_scripts[id] = False
    threading.Thread(target=lambda: run_evaluation(id, num)).start()
    return render_template('processing.html', id=id, num=num)

@app.route('/get_result')
def get_result():
    id = request.args.get('id', None)
    if id not in background_scripts:
        abort(404)
    return jsonify(done=background_scripts[id])

@app.route('/show_result/<id>')
def show_result(id):
    html='''
        <!DOCTYPE html>
        <html lang="en-US">
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <meta name="description" content="an RNN Chinese Tang Poetry Generator">
                <meta name="author" content="Shi Yin">

                <title>RNN Tang Poetry Generator</title>

                <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

        <!-- Custom CSS -->
        <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans:600">
        <link rel="stylesheet" href="'''
    html+=url_for('static', filename='css/style.css')
    html+='''">
            </head>

            <body>
            <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse-1" aria-expanded="false">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand">&nbsp;RNN Chinese Tang Poetry Generator</a>
                </div>

                <div class="collapse navbar-collapse" id="navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
    <li class=""><a href="#">About</a></li>
</ul>
                </div><!--/.nav-collapse -->
            </div>
        </nav>

                <div class="container">
                <div id="google_translate_element"></div><script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'zh-CN', layout: google.translate.TranslateElement.FloatPosition.TOP_LEFT}, 'google_translate_element');
}
</script><script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
                    <div class="row">
                        <table class="table">
        '''
    for p in result[id]:
        html +='''<tr><td>'''+p+'''</td></tr>'''
    html+='''
                </table>
                </div>
            </div>

            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        </body>
    </html>'''

    return html

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


