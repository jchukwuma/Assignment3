#!/usr/bin/env python

#----------------------------------------------------------------------
# database.py
# Author: Justice Chukwuma
#----------------------------------------------------------------------

from sys import stderr
from contextlib import closing
from sqlite3 import connect
#----------------------------------------------------------------------
DATABASE_URL = 'file:reg.sqlite?mode=ro'

def query_dept(dept, params):
    dept = dept.replace('\'', '\'\'')
    if '%' in dept or '_' in dept:
        dept = dept.replace('%', '@%')
        dept = dept.replace('_', '@_')
        stmt = " crosslistings.dept LIKE ? ESCAPE '@'"
        params.append('%' +dept.upper() +'%')
    else:
        stmt = " crosslistings.dept LIKE ?"
        params.append('%' +dept.upper() +'%')
    return stmt, params

def query_num(num, params):
    num = num.replace('\'', '\'\'')
    if '%' in num or '_' in num:
        num = num.replace('%', '@%')
        num = num.replace('_', '@_')
        stmt = " crosslistings.coursenum LIKE ? ESCAPE '@'"
        params.append('%' +num +'%')
    else:
        stmt = " crosslistings.coursenum LIKE ?"
        params.append('%' +num +'%')

    return stmt, params

def query_area(area, params):
    area = area.replace('\'', '\'\'')
    if '%' in area or '_' in area:
        area = area.replace('%', '@%')
        area = area.replace('_', '@_')
        stmt = " courses.area LIKE ? ESCAPE '@'"
        params.append('%' +area.upper() +'%')

    else:
        stmt = " courses.area LIKE ?"
        params.append('%' +area.upper() +'%')
    return stmt, params

def query_title(title, params):
    title = title.replace('\'', '\'\'')
    if '%' in title or '_' in title:
        title = title.replace('%', '@%')
        title = title.replace('_', '@_')
        stmt = " courses.title LIKE ? ESCAPE '@'"
        params.append('%' +title +'%')
    else:
        stmt = " courses.title LIKE ?"
        params.append('%' +title +'%')
    return stmt, params


#*****************************************************************
def search_database(parameters):
    with connect(DATABASE_URL, isolation_level=None,
    uri=True) as connection:
        with closing(connection.cursor()) as cursor:
            params = []
            stmt_str = "SELECT classes.classid, "
            stmt_str += "crosslistings.dept, "
            stmt_str += "crosslistings.coursenum, "
            stmt_str += "courses.area, courses.title"
            stmt_str += " FROM classes INNER JOIN courses on "
            stmt_str += "classes.courseid = courses.courseid"
            stmt_str += " INNER JOIN crosslistings on"
            stmt_str += " classes.courseid = crosslistings.courseid"
            multiple_args = False
            for arg in parameters:
                if arg == "dept" and parameters[arg]:
                    if multiple_args:
                        stmt_str += " AND"
                    else:
                        stmt_str += " WHERE"
                    sub, params= query_dept(parameters[arg], params)
                    stmt_str += sub
                    multiple_args = True

                elif arg == "number" and parameters[arg]:
                    if multiple_args:
                        stmt_str += " AND"
                    else:
                        stmt_str += " WHERE"

                    sub, params= query_num(parameters[arg], params)
                    stmt_str += sub
                    multiple_args = True

                elif arg == "area" and parameters[arg]:
                    if multiple_args:
                        stmt_str += " AND"
                    else:
                        stmt_str += " WHERE"
                    sub, params = query_area(parameters[arg],
                     params)
                    stmt_str += sub
                    multiple_args = True

                elif arg == "title" and parameters[arg]:
                    if multiple_args:
                        stmt_str += " AND"
                    else:
                        stmt_str += " WHERE"
                    sub, params= query_title(parameters[arg],
                     params)
                    stmt_str += sub
                    multiple_args = True

            stmt_str += " ORDER BY crosslistings.dept"
            stmt_str += " ASC, crosslistings.coursenum ASC, "
            stmt_str += "classes.classid ASC;"
            cursor.execute(stmt_str, params)
            rows = cursor.fetchall()
            return rows
#********************************************************************

def get_more_info(classid):
    data = {}
    with connect(DATABASE_URL, isolation_level=None,
        uri=True) as connection:
        with closing(connection.cursor()) as cursor:

            stmt_str = "SELECT courseid, days, starttime,"
            stmt_str += " endtime, bldg, roomnum FROM classes"
            stmt_str += " WHERE classid = '" + classid + "'"
            cursor.execute(stmt_str)
            row = cursor.fetchone()
            if not row:
                raise ValueError("No such classid")
            print("Row: ", row)
            data["Course Id: "] = row[0]
            data["Days: "] = row[1]
            data["Start time: "] = row[2]
            data["End time: "] = row[3]
            data["Building: "] = row[4]
            data["Room: "] = row[5]
            data["Dept and Number: "] = []

            stmt_str = "SELECT dept, coursenum FROM crosslistings "
            stmt_str += "INNER JOIN classes on "
            stmt_str += "crosslistings.courseid=classes.courseid "
            stmt_str += "WHERE classes.classid = '" + classid
            stmt_str += "' ORDER BY dept ASC, coursenum ASC"
            cursor.execute(stmt_str)
            rows = cursor.fetchall()
            for row in rows:
                data["Dept and Number: "].append(row[0]+" "+row[1])

            stmt_str = "SELECT area, title, descrip,"
            stmt_str += " prereqs FROM courses"
            stmt_str += " INNER JOIN classes on"
            stmt_str += " courses.courseid=classes.courseid"
            stmt_str += " WHERE classes.classid = '" + classid + "'"
            cursor.execute(stmt_str)
            row = cursor.fetchone()
            data["Area: "] = row[0]
            data["Title: "] = row[1]
            data["Description: "] = row[2]
            data["Prerequisites: "] = row[3]


            stmt_str = "SELECT profname FROM"
            stmt_str += " profs JOIN coursesprofs "
            stmt_str += "on profs.profid=coursesprofs.profid"
            stmt_str += " JOIN classes on "
            stmt_str += "coursesprofs.courseid=classes.courseid"
            stmt_str += " WHERE classes.classid = '"
            stmt_str += classid + "' ORDER BY profname ASC"
            cursor.execute(stmt_str)
            rows = cursor.fetchall()
            data["Professor: "] = []
            for row in rows:
                data["Professor: "].append(row[0])
    return data
