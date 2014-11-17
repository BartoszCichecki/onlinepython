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
import pypy_runner as pyrun

#Own created modules
import jinjafilters

env = Environment(loader=FileSystemLoader('templates'))
env.filters.update({
    'exists':jinjafilters.exists
})

class Index(object):

    @cherrypy.expose()
    def index(self):
        if 'loggedIn' in cherrypy.session:
            raise cherrypy.HTTPRedirect("/interview")

        tmpl = env.get_template('interview_login.html')
        return tmpl.render()

    @cherrypy.expose(alias='doInterviewLogin')
    def do_interview_login(self, username, password):
        db.check_interview_credentials(username, password)
        if not db.check_interview_credentials(username, password):
            raise cherrypy.HTTPRedirect("/")

        cherrypy.session['loggedIn'] = True
        cherrypy.session['user_id'] = db.get_interview_id(username)
        raise cherrypy.HTTPRedirect("/interview")

    @cherrypy.expose
    def interview(self):
        self.verify_session()
        tmpl = env.get_template('interview_home.html')
        exercise_list = db.get_exercises()
        data = db.get_interviews(self.get_id())
        selected_exercises = db.get_interview_exercise_ids(self.get_id())
        if len(selected_exercises) > 0:
            return tmpl.render(full_name=data.full_name, username=data.username, exercises=exercise_list, selected_exercises=selected_exercises)
        return tmpl.render(full_name=data.full_name, username=data.username)
    
    @cherrypy.expose
    def submit(self, ex_id):
        self.verify_session()
        tmpl = env.get_template('interview_submit.html')
        data = db.get_interviews(self.get_id())
        return tmpl.render(full_name=data.full_name, exercise_id=ex_id)

    @cherrypy.expose(alias='submitExercise')
    def submit_exercise(self, exercise_id, script):
        self.verify_session()
        interview = db.get_interviews(self.get_id())
        exercise = db.get_exercises(exercise_id)
        result = pyrun.run_file(interview, exercise, script)
        return str(result)

    def verify_session(self):
        if 'loggedIn' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/")
    
    def get_id(self):
        return 'user_id' in cherrypy.session

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
        interview_list = db.get_interviews()
        tmpl = env.get_template('admin_console.html')
        return tmpl.render(exercises=exercise_list, interviews=interview_list)

    @cherrypy.expose
    def edit_exercise(self, exercise_id=None, new=None):
        self.verify_session()
        tmpl = env.get_template('admin_edit_exercise.html')
        if exercise_id:
            data = db.get_exercises(exercise_id)
            return tmpl.render(friendly_name = data.friendly_name, description=data.description, output=data.expected_output, timelimit=data.time_limit, exercise_id=data.id)
        return tmpl.render()

    @cherrypy.expose
    def delete_exercise(self, exercise_id=None):
        self.verify_session()
        if exercise_id:
            db.delete_exercise(exercise_id)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose(alias='doEditExercise')
    def do_edit_exercise(self, exercise_id, friendly_name, description, output, timeLimit):
        self.verify_session()
        success = True
        if exercise_id:
            success = db.edit_exercise(exercise_id, friendly_name, description, output, timeLimit)
        else:
            success = db.create_exercise(friendly_name, description, output, timeLimit)

        if success:
            raise cherrypy.HTTPRedirect("/admin/console")
        else:
            raise cherrypy.HTTPRedirect("/admin/edit_exercise?exercise_id="+exercise_id)

    @cherrypy.expose
    def edit_interview(self, interview_id=None, new=None):
        self.verify_session()
        tmpl = env.get_template('admin_edit_interview.html')
        exercise_list = db.get_exercises()
        if interview_id:
            data = db.get_interviews(interview_id)
            selected_exercises = db.get_interview_exercise_ids(interview_id)
            return tmpl.render(full_name=data.full_name, username=data.username, password=data.password, exercises=exercise_list, selected_exercises=selected_exercises, interview_id = data.id)
        return tmpl.render(exercises=exercise_list)

    @cherrypy.expose
    def delete_interview(self, interview_id=None):
        self.verify_session()
        if interview_id:
            db.delete_interview(interview_id)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose(alias='doEditInterview')
    def do_edit_interview(self, interview_id, full_name, username, password, exerciseIds=[]):
        self.verify_session()
        success = True
        if interview_id:
            success = db.edit_interview(interview_id, full_name, username, password, exerciseIds)
        else:
            success = db.create_interview(full_name, username, password, exerciseIds)

        if success:
            raise cherrypy.HTTPRedirect("/admin/console")
        else:
            raise cherrypy.HTTPRedirect("/admin/edit_interview?exercise_id="+id)

    def verify_session(self):
        if 'loggedInAdmin' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/admin")

def initialize():
    index = Index()
    index.admin = AdminIndex()
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': 8081,
                            'tools.sessions.on' : True,
                            'tools.encode.on' : True,
                            'tools.encode.encoding' : 'utf-8'
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
