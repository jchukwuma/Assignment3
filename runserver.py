#!/usr/bin/env python

#--------------------------------------------------------------
# runserver.py
# Author: Justice Chukwuma
#--------------------------------------------------------------

from sys import argv, exit, stderr
from penny import app
import argparse

def main():

    try:
        parser = argparse.ArgumentParser(
        description="The registar application")
        parser.add_argument('port',
         help='the port at which the server should listen')
        args = parser.parse_args()
        port = int(argv[1])
    except Exception as ex:
        print(ex, file=stderr)
        exit(2)
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
