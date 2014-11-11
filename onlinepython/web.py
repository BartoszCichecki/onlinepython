# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 20:47:49 2014

@author: Bartosz
"""

#Python modules
import cherrypy
import db
import os
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
        exercise_list = db.get_exercises()
        user_list = db.get_users()
        tmpl = env.get_template('admin_console.html')
        return tmpl.render(exercises=exercise_list, users=user_list)

    @cherrypy.expose(alias='createExercise')
    def create_exercise(self, description, timeLimit, output):
        self.verify_session()
        db.create_exercise(description, timeLimit, output)
        raise cherrypy.HTTPRedirect("/admin/console")
        
    @cherrypy.expose(alias='createUser')
<<<<<<< HEAD
    def create_user(self, username, password):
=======
    def create_exercise(self, username, password):
>>>>>>> origin/master
        self.verify_session()
        db.create_user(username, password)
        raise cherrypy.HTTPRedirect("/admin/console")
        
    @cherrypy.expose
<<<<<<< HEAD
    def edit_exercise(self, id):
        self.verify_session()
        data = db.get_exercises(id)
        tmpl = env.get_template('admin_edit_exercise.html')
        return tmpl.render(description=data.description, timelimit=data.time_limit, output=data.expected_output, id=data.id)
        
    @cherrypy.expose(alias='editExercise')
    def edit_exercise_info(self, id, description, timeLimit, output):
        self.verify_session()
        db.edit_exercise(id, description, timeLimit, output)
        raise cherrypy.HTTPRedirect("/admin/console")
        
    @cherrypy.expose
    def edit_user(self, id):
        self.verify_session()
        open_data = db.get_user_exercises(id)
        exercise_data = db.get_exercises()
        user_data = db.get_users(id)
        tmpl = env.get_template('admin_edit_user.html')
        return tmpl.render(user=user_data, open_list=open_data, exercise_list=exercise_data)
        
    @cherrypy.expose(alias='editUser')
    def edit_user_info(self, user_id, ex_id, add):
        self.verify_session()
        db.add_user_exercise(user_id, ex_id, add)
        raise cherrypy.HTTPRedirect("/admin/console")
=======
    def edit(self, id):
        self.verify_session()
        data = db.get_exercises(id)
        tmpl = env.get_template('admin_edit.html')
        return tmpl.render(description=data.description, timelimit=data.time_limit, output=data.expected_output, id=data.id)
        
    @cherrypy.expose(alias='editExercise')
    def edit_exercise(self, id, description, timeLimit, output):
        self.verify_session()
        db.edit_exercise(id, description, timeLimit, output)
        raise cherrypy.HTTPRedirect("/admin/console")
>>>>>>> origin/master

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
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
     }
    cherrypy.quickstart(index, '/', conf)
