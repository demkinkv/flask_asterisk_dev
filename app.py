#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for
import json, pyCFunc

class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value
            #self.app.configs['JSON_AS_ASCII'] = False

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

flask_app = Flask(__name__, static_folder='static')

app = FlaskAppWrapper(flask_app)

def list_number():
    message = ''
    try:
        with open("data_number_db.json", 'rt', encoding='utf-8') as read_file_json:
                data_json = json.load(read_file_json)
                print(type(data_json))
    except:
        data_json = {
                    "data_number": [
                        {
                            "number": "Error",
                            "user": "JSON file",
                            "location": "please",
                            "outline": "Update JSON"
                        }
                        ]
                    }

    return render_template('list_number.html', data=data_json)

def summaryapi():
    with open("data_number_db.json", 'rt', encoding='utf-8') as read_file_json:
            data_json = json.load(read_file_json)
    return jsonify(data_json, 200)

def list_number_ping():
    if request.method == "POST":
        searchnumber = request.form['searchnumber']
        message_ping = ''
        print(f'Item: '+searchnumber)
        resultdata = str(pyCFunc.CFunc_conn.paramiko_conn("asterisk -rx 'pjsip show aor "+searchnumber+"' | awk '$1 == \"contact\" {print $3}'"))
        print(resultdata)
        if len(resultdata) < 10:
            testState = 'alert-warning'
            message_ping = 'NO DATA FILE'
        if len(resultdata) > 10:
            # *activate Link
            testState = 'alert-success'
            print(resultdata.split(":")[1].split("@")[1])
            resultdata_ping = resultdata.split(":")[1].split("@")[1]
            message_ping = (f'Last IP: '+str(resultdata_ping))
        print(message_ping)
        outputjs = {
            'testState':testState,
            'output':message_ping,
        }
        return jsonify(outputjs)
    return render_template('list_number.html')

def call_function():
    message_call = ''
    if request.method == 'POST':
        inputMobile = request.form.get('inputMobile') #? запрос к данным формы
        inputAstNumber = request.form.get('inputAstNumber') #? запрос к данным формы
        if not (inputMobile.isnumeric() and inputAstNumber.isnumeric()):
            message_call = 'введите телефоны в текстовом формате'
        elif not (len(inputMobile)==11 and len(inputAstNumber) == 4):
            message_call = 'введите телефоны правильной длины'
        else:
            select_flask = request.form.get('flask_select')
            src_flask = inputMobile
            dst_flask = inputAstNumber
            resultdata = str(pyCFunc.CFunc_conn.paramiko_conn(f"sh /root/asterisk/make-call/mobile_to_local.sh {dst_flask} {src_flask} {select_flask}"))
            message_call = (f"Ожидайте вызов на {src_flask}, потом на {dst_flask}, через {select_flask}.{resultdata}")
    return render_template('call_page.html', message_call=message_call)

def translate():
    message = ''
    username = ''
    if request.method == 'POST':
        # запрос к данным формы
        username = request.form.get('username')
        lang_tr = list(request.form.getlist('lang_tr'))
        message = pyCFunc.CFunc_translitizator.translitizator(username, lang_tr[0])
    return render_template('translate.html', data=message, data2=username)

def update():
    message = ''
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        print (username, password)
        if username == 'root' and password == 'pass':
            pyCFunc.CFunc_ast_to_number.ast_to_number()
            message = "Correct username and password. JSON Updates"
        else:
            message = "Wrong username or password"
    return render_template('update.html', message=message)

def about():
    return "About page"

def action():
    """ Function which is triggered in flask app """
    return "Hello World"

def test():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        output = firstname + lastname
        if firstname and lastname:
            return jsonify({'output': 'Your Name is ' + output + ', right?'})
        return jsonify({'error': 'Missing data!'})
    return render_template('test.html')

app.add_endpoint('/', 'list_number', list_number, methods=['GET'])
app.add_endpoint('/list_number/', 'list_number', list_number, methods=['GET'])
app.add_endpoint('/list_number/api/', 'summaryapi', summaryapi, methods=['POST', 'GET'])
app.add_endpoint('/list_number/searchnumber/', 'list_number_ping', list_number_ping, methods=['POST', 'GET'])
app.add_endpoint('/call_function/', 'call_function', call_function, methods=['POST', 'GET'])
app.add_endpoint('/tranlate/', 'translate', translate, methods=['POST', 'GET'])
app.add_endpoint('/update/', 'update', update,  methods=['POST', 'GET'])
app.add_endpoint('/about', 'about', about)
app.add_endpoint('/action', 'action', action, methods=['GET'])
app.add_endpoint('/test/', 'test', test, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
