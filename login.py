#!/usr/bin/env python3
import cgi
import cgitb
import json
import os
import sys
from templates import login_page, secret_page, after_login_incorrect
import secret
from http.cookies import SimpleCookie

# inspect all environment variables
print("-------------1-----------------")
# print(os.environ)
print(json.dumps(dict(os.environ), indent=2))
# HTML
print("Content-Type: text/html")
print("")

# What environment variable contains the query parameter data?
print("-------------2-----------------")
print(os.environ['QUERY_STRING'])

# What environment variable contains information about the user’s browser?
print("-------------3-----------------")
print(os.environ['HTTP_USER_AGENT'])

# to contain a login form that POSTs to itself
print("-------------4-----------------")
print(login_page())
form = cgi.FieldStorage()
username = form.getfirst('username')
password = form.getfirst('password')
# report the values of the POSTed data in the HTML
if "username" not in form or "password" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the username and password fields.")
else:
    print("<p>username:", form["username"].value)
    print("<p>password:", form["password"].value)
print("Content-Type: text/html")
print("")

# create cookies
print("-------------5-----------------")
form_ok = username == secret.username and password == secret.password
cookie = SimpleCookie(os.environ['HTTP_COOKIE'])
c_username = None
c_password = None
if cookie.get('username'):
    c_username = cookie.get('username').value
if cookie.get('password'):
    c_password = cookie.get('password').value

cookie_ok = c_username == secret.username and c_password == secret.password

if cookie_ok:
    username = c_username
    password = c_password

if form_ok:
    print('Set-Cookie: username=', username)
    print('Set-Cookie: password=', password)
print("")

print("------------6------------------")
if not username and not password:  # none
    print(login_page())
elif username == secret.username and password == secret.password:  # same
    print(secret_page(username, password))
else:
    print(after_login_incorrect())
