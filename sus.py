from flask import Flask, url_for, redirect, request, render_template, flash, session
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = b'\xccM6\x16\xbfVw>b\xbd\xde{\xd4\x01\x83\x90'
#app.wsgi_app = ProxyFix(app.wsgi_app)

all_responses = {}
sum_of_scores = 0.0

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index_sus.html', username=session['username'], \
            respond_already=(session['username'] in all_responses))
    else:
        return render_template('index_sus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and 'username' in session\
        and session['username'] != None:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != None\
            and request.form['username'] != '':
            flash('Successfully logged in.')
            session['username'] = request.form['username']
            return redirect(url_for('questionnaire'))
        else:
            error = 'Please put your username.'
    return render_template('login_sus.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if request.method == 'GET' and ('username' not in session\
        or session['username'] == None):
        return redirect(url_for('login'))
    if request.method == 'POST':
        valid = True
        score = 0.0
        responses = []
        for i in range(1, 11):
            if str(i) not in request.form or request.form[str(i)] == None:
                valid = False
                responses.append([False, False, False, False, False, True])
            else:
                temp = float(request.form[str(i)])
                score += temp
                temp2 = [False, False, False, False, False, False]
                temp2[int(temp)] = True
                responses.append(temp2)
        if valid:
            score *= 2.5
            # TODO update server DB
            all_responses[session['username']] = responses
            global sum_of_scores
            sum_of_scores += score
            response_count = len(all_responses)
            print('New response has been recorded! Username: ' + session['username'] + \
                ', Score: ' + str(score) + \
                ', Response count: ' + str(response_count) + \
                ', Avg. of scores: ' + str(sum_of_scores / response_count))

            flash('Thank you! Your response has been recorded.')
            return redirect(url_for('result'))
        else:
            error = 'Please respond to all 10 questions before submit.'
            return render_template('questionnaire_sus.html', error=error, responses=responses, \
                respond_already=(session['username'] in all_responses))

    if session['username'] in all_responses:
        return render_template('questionnaire_sus.html', \
            responses=all_responses[session['username']], \
            respond_already=(session['username'] in all_responses))
    else:
        return render_template('questionnaire_sus.html', \
            respond_already=(session['username'] in all_responses))

@app.route('/result')
def result():
    if request.method == 'GET' and ('username' not in session\
        or session['username'] == None):
        return redirect(url_for('login'))

    if len(all_responses) > 0:
        return render_template('result_sus.html', username=session['username'], \
            respond_already=(session['username'] in all_responses), \
            response_count=str(len(all_responses)), \
            average=str(sum_of_scores / len(all_responses)))
    else:
        return render_template('result_sus.html', username=session['username'], \
            respond_already=(session['username'] in all_responses), \
            response_count='0', \
            average='0')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found_sus.html'), 404
