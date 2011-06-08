#!/usr/bin/python

import os
import re
import subprocess
import BaseHTTPServer as http

SOURCE_PATH = '/work/chrome/'


def map_path(path):
    if path.startswith('/'):
        path = path[1:]
    path = os.path.normpath(os.path.join(SOURCE_PATH, path))
    if not path.startswith(SOURCE_PATH):
        return None
    return path


class EditHandler(http.BaseHTTPRequestHandler):
    def verify_path(self):
        path = map_path(self.path)
        if not path or not os.path.exists(path):
            self.send_response(404)
            self.end_headers()
            return
        return path

    def do_GET(self):
        path = self.verify_path()
        if not path:
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('%s => %s\n' % (self.path, map_path(self.path)))

    def do_POST(self):
        path = self.verify_path()
        if not path:
            return
        print self.path, path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        subprocess.check_call(['emacsclient', '-n', path])
        self.wfile.write('sent to emacs\n')


server = http.HTTPServer(('', 0xED17), EditHandler)
server.serve_forever()
