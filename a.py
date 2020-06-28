#!/usr/bin/env python 
# -*- coding=utf-8 -*-
import os
import sys
import ast

log = open("/home/student/wus2/Desktop/log.txt", "w")
post_req_log = open("/home/student/wus2/Desktop/post_req.txt", "w")
get_req_log = open("/home/student/wus2/Desktop/get_req.txt", "w")


def new_form(html='', name='', accept=-1):
    print('''
    <html>
    <body>''')
    print(html)

    print('''
    <h1>You are Invited!</h1> 

    details goes here
    <br/><br/><br/>

    <form action="/CGI_Test/a.py" method="POST">
        <label for="name">Your name:</label>
        <input type="text" name="name" pattern=".*[a-zA-Z].*" title="At least 1 English letter" {} autofocus required>
        <br/>
        <p2>Would you accept the invitation?</p2>
        <br/>
        <input type="radio" name="accept" value="1" required {}> Accept
        <input type="radio" name="accept" value="0" {}> Decline
        <br/>
        <input type="submit" value="Submit">
    </form>

    </body>
    </html>
    '''.format('' if name == '' else ("value=" + name),
               "checked" if accept == 1 else "",
               "checked" if accept == 0 else ""))


def submitted(name, response, update):
    print('''
    <html>
    <body>
    
    <h1>Your reply has been {}!</h1> 
    
    details goes here
    <br/><br/><br/>
    '''.format("updated" if update else "submitted"))
    print("Name: " + name)
    print('<br/>')
    print("Response: " + ("Accepted" if response == '1' else "Declined"))
    print('<form action="/CGI_Test/a.py" method="GET">')
    print('<button name="Anonymize" type="submit">Anonymize</button>')
    print('</form>')

    print('''
    </body>
    </html>
    ''')


def nuked():
    new_form('<p style="color:green">Previous record deleted.</p>')


# get cookies
cookies = {}
try:
    log.write(os.environ['HTTP_COOKIE'])
    for cookie in os.environ['HTTP_COOKIE'].split('; '):
        temp = cookie.split('=')
        cookies[temp[0]] = temp[1]
except KeyError:  # no cookie
    pass

# get POST Request
post_req = {}
try:
    raw_post_req = sys.stdin.read(int(os.environ.get('HTTP_CONTENT_LENGTH', 0)))
    post_req_log.write(raw_post_req)
    for a in raw_post_req.split('&'):
        temp = a.split('=')
        post_req[temp[0]] = temp[1]
except AttributeError:  # no POST request
    pass

dic = {}
try:
    with open("/home/student/wus2/Desktop/dic_db.txt", 'r') as d:
        dic = ast.literal_eval(d.read())
except FileNotFoundError:
    pass

# HTML Header
print("Content-type:text/html")

# get GET request, if Anonymize
get_req = {}
raw_get_req = str(os.environ.get('QUERY_STRING', 0))
if raw_get_req != '':
    get_req_log.write(raw_get_req)
    if raw_get_req == 'Anonymize=':
        print("Set-Cookie: {}={}".format('name', ''))
        print("Set-Cookie: {}={}".format('accept', ''))
        print()
        nuked()
        post_req_log.close()
        log.close()
        get_req_log.close()
        exit()
    for a in raw_get_req.split('&'):
        temp = a.split('=')
        get_req[temp[0]] = temp[1]

if len(post_req) == 0:
    print()
    if len(cookies) == 0 or cookies['name'] == '':  # no cookies
        new_form()
    else:
        new_form(name=cookies['name'], accept=int(cookies['accept']))
else:
    print("Set-Cookie: {}={}".format('name', post_req['name']))
    print("Set-Cookie: {}={}".format('accept', post_req['accept']))
    print()
    if dic.get(post_req['name']) is None:
        submitted(post_req['name'], post_req['accept'], update=False)
    else:
        submitted(post_req['name'], post_req['accept'], update=True)
    dic[post_req['name']] = post_req['accept']

with open("/home/student/wus2/Desktop/dic_db.txt", 'w') as d:
    print(dic, file=d)

post_req_log.close()
log.close()
get_req_log.close()
