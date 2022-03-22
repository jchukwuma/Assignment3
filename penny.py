
#!/usr/bin/env python

#--------------------------------------------------------------
# penny.py
# Author: Justice Chukwuma
#--------------------------------------------------------------

from database import search_database, get_more_info
from flask import Flask, request, make_response
from flask import render_template
from urllib.parse import quote_plus, unquote_plus

#--------------------------------------------------------------
app = Flask(__name__, template_folder= 'templates')
#--------------------------------------------------------------
@app.route('/', methods=['GET'])

def index():

    params = {}
    dept = request.args.get('dept')
    num = request.args.get('num')
    area = request.args.get('area')
    title = request.args.get('title')
    if (dept is None) or (dept.strip()==''):
        dept = ""
    params["dept"]= dept

    if (num is None) or (num.strip()==''):
        num = ""
    params["number"]=num

    if (area is None) or (area.strip()==''):
        area= ""
    params["area"]=area

    if (title is None) or (title.strip()==''):
        title= ""
    title=unquote_plus(title)
    params["title"]=title
    try:
        results = search_database(params)
    except Exception:
        html = render_template('servererror.html')
        response = make_response(html)
        return response

    html = render_template('index.html', results = results,
        dept= dept,
        num = num,
        area = area,
        title = title, unquote_plus=unquote_plus)

    response = make_response(html)
    response.set_cookie('dept', dept)
    response.set_cookie('num', num)
    response.set_cookie('area', area)
    response.set_cookie('title', quote_plus(title))
    return response

#--------------------------------------------------------------
@app.route('/regdetails', methods=['GET'])
def regdetails():

    classid = request.args.get('classid')

    if (classid is None) or (classid.strip() ==''):
        html = render_template('missingid.html')
        response = make_response(html)
        return response
    if not classid.isdigit():
        html = render_template('nonintegerid.html')
        response = make_response(html)
        return response
    try:
        info = get_more_info(classid)
    except ValueError:
        print("ValueError")
        html = render_template('nonexistingid.html', coursenum=classid)
        response = make_response(html)
        return response
    except Exception:
        print("Any Other Error")
        html = render_template('servererror.html')
        response = make_response(html)
        return response

    prev_dept = request.cookies.get('dept')
    prev_num = request.cookies.get('num')
    prev_area = request.cookies.get('area')
    prev_title = request.cookies.get('title')

    html = render_template('regdetails.html', id = classid, info = info,
     prev_num=prev_num, prev_dept = prev_dept, prev_area=prev_area,
     prev_title = quote_plus(prev_title), unquote_plus=unquote_plus)


    response = make_response(html)

    return response
