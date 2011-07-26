#!/usr/bin/python

import os
import re
import subprocess
import BaseHTTPServer as http

SOURCE_PATHS = ['/work/chrome/', '/work/chrome/src/']


def map_path(path):
    if path.startswith('/'):
        path = path[1:]
    for source in SOURCE_PATHS:
        fullpath = os.path.normpath(os.path.join(source, path))
        if fullpath.startswith(source) and os.path.exists(fullpath):
            return fullpath
    return None


class EditHandler(http.BaseHTTPRequestHandler):
    def do_POST(self):
        path = map_path(self.path)
        if not path:
            self.send_response(404)
            self.end_headers()
            return

        print self.path, path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        subprocess.check_call(['emacsclient', '-n', path])
        self.wfile.write('sent to emacs\n')


server = http.HTTPServer(('', 0xED17), EditHandler)
server.serve_forever()
