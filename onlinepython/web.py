# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 20:47:49 2014

@author: Bartosz
"""

#Python modules
import cherrypy
import db
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class Index(object):

    @cherrypy.expose
    def index(self):
        if 'loggedIn' in cherrypy.session:
            raise cherrypy.HTTPRedirect("/interview")

        tmpl = env.get_template('interview_login.html')
        return tmpl.render()

    @cherrypy.expose(alias='doInterviewLogin')
    def do_interview_login(self, username, password):
        if not db.check_interview_credentials(username,password):
            raise cherrypy.HTTPRedirect("/")

        cherrypy.session['loggedIn'] = True
        raise cherrypy.HTTPRedirect("/interview")

    @cherrypy.expose
    def interview(self):
        self.verify_session()

        return "OK"

    def verify_session(self):
        if 'loggedIn' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/")

class AdminIndex(object):

    @cherrypy.expose()
    def index(self):
        if 'loggedInAdmin' in cherrypy.session:
            raise cherrypy.HTTPRedirect("/admin/console")

        tmpl = env.get_template('admin_login.html')
        return tmpl.render()

    @cherrypy.expose(alias='doAdminLogin')
    def do_admin_login(self, username, password):
        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            raise cherrypy.HTTPRedirect("/admin")

        cherrypy.session['loggedInAdmin'] = True
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose
    def console(self):
        self.verify_session()

        return "OK"

    def verify_session(self):
        if 'loggedInAdmin' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/admin")

def initialize():
    index = Index()
    index.admin = AdminIndex()

    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': 8081,
                            'tools.sessions.on' : True
                           })
    cherrypy.quickstart(index, '/')
