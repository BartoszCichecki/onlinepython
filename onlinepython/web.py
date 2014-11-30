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

ENV = Environment(loader=FileSystemLoader('templates'))
ENV.filters.update({
    'exists':jinjafilters.exists
})

def nl2br(text):
    """Converts newlines to <br />

    Keyword arguments:
    text -- Text

    Return values:
    Converted text
    """
    text = str(text)
    text = text.replace('\r\n', '<br />')
    text = text.replace('\n', '<br />')
    text = text.replace('\r', '<br />')
    return text

class Index(object):
    """ User pages. """

    @cherrypy.expose()
    def index(self):
        """ Exposes a login page. """
        if 'loggedIn' in cherrypy.session:
            raise cherrypy.HTTPRedirect("/interview")

        tmpl = ENV.get_template('interview_login.html')
        return tmpl.render()

    @cherrypy.expose(alias='doInterviewLogin')
    def do_interview_login(self, username, password):
        """ Handles submitted form after logging in.

        Keyword arguments:
        username -- username
        password -- password
        """
        db.check_interview_credentials(username, password)
        if not db.check_interview_credentials(username, password):
            raise cherrypy.HTTPRedirect("/")

        cherrypy.session['loggedIn'] = True
        cherrypy.session['user_id'] = db.get_interview_id(username)
        raise cherrypy.HTTPRedirect("/interview")

    @cherrypy.expose()
    def interview(self):
        """ Exposes interview page. """
        self.verify_session()
        tmpl = ENV.get_template('interview_home.html')
        exercise_list = db.get_exercises()
        data = db.get_interviews(self.get_id())
        selected_exercises = db.get_interview_exercise_ids(self.get_id())
        correct_exercises = [exercise.id for exercise in exercise_list
                        if db.has_correct_solution(exercise_id=exercise.id,
                                                   interview_id=self.get_id())]
        if len(selected_exercises) > 0:
            return tmpl.render(full_name=data.full_name,
                               username=data.username,
                               exercises=exercise_list,
                               selected_exercises=selected_exercises,
                               correct_exercises=correct_exercises)
        return tmpl.render(full_name=data.full_name, username=data.username)

    @cherrypy.expose()
    def submit(self, ex_id):
        """ Exposes submit page.

        Keyword arguments:
        ex_id -- id of exercise to submit
        """
        self.verify_session()
        tmpl = ENV.get_template('interview_submit.html')
        data = db.get_interviews(self.get_id())
        return tmpl.render(full_name=data.full_name, exercise_id=ex_id)

    @cherrypy.expose(alias='submitExercise')
    def submit_exercise(self, exercise_id, script):
        """
        Exposes submit exercise page.

        Keyword arguments:
        exercise_id -- id of exercise
        script -- script to submit
        """
        self.verify_session()
        interview = db.get_interviews(self.get_id())
        exercise = db.get_exercises(exercise_id)
        data = db.get_interviews(self.get_id())
        result = pyrun.run_file(interview, exercise, script)
        if result['correct']:
            correct = "Correct"
        else:
            correct = "Not correct"
        tmpl = ENV.get_template('interview_submit_result.html')
        return tmpl.render(full_name=data.full_name,
                           correct=correct,
                           used_time=result['execution_time'],
                           used_mem=result['memory_usage'],
                           output=nl2br(result['output']),
                           expected_output=nl2br(result['expected_output']))

    def verify_session(self):
        """ Verifies user sessions. If user is not logged in,
        performs redirect.
        """
        if 'loggedIn' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/")

    def get_id(self):
        """ Gets user id from session. """
        return cherrypy.session['user_id']

    @cherrypy.expose()
    def logout(self):
        """ Exposes a logout page. """
        cherrypy.session.clear()
        raise cherrypy.HTTPRedirect("/")

class AdminIndex(object):
    """ Admin pages. """

    @cherrypy.expose()
    def index(self):
        """ Exposes login page. """
        if 'loggedInAdmin' in cherrypy.session:
            raise cherrypy.HTTPRedirect("/admin/console")

        tmpl = ENV.get_template('admin_login.html')
        return tmpl.render()

    @cherrypy.expose(alias='doAdminLogin')
    def do_admin_login(self, username, password):
        """ Handles submitted form after logging in.

        Keyword arguments:
        username -- username
        password -- password
        """
        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            raise cherrypy.HTTPRedirect("/admin")

        cherrypy.session['loggedInAdmin'] = True
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose()
    def console(self):
        """ Exposes admin console page. """
        self.verify_session()
        exercise_list = db.get_exercises()
        interview_list = db.get_interviews()
        tmpl = ENV.get_template('admin_console.html')
        return tmpl.render(exercises=exercise_list, interviews=interview_list)

    @cherrypy.expose()
    def info_exercise(self, exercise_id=None):
        """ Exposes page with information about exercise.

        Keyword arguments:
        exercise_id -- id of exercise to show info about
        """
        self.verify_session()
        tmpl = ENV.get_template('admin_info_exercise.html')
        if exercise_id:
            solutions = db.get_solutions(exercise_id=exercise_id)
            data = db.get_exercises(exercise_id)
            submits = len([x for x in solutions])
            corrects = len([x for x in solutions if x.correct == True]) * 1.0
            if submits == 0:
                correct_percent = "No submitted solutions"
            else:
                correct_percent = corrects / submits * 100.0
            return tmpl.render(friendly_name=data.friendly_name,
                               description=data.description,
                               output=data.expected_output,
                               time_limit=data.time_limit,
                               exercise_id=data.id,
                               correct_percent=correct_percent,
                               submits=submits)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose()
    def info_exercise_solutions(self, corrects=1, exercise_id=None):
        """ Exposes page with information about exercise.

        Keyword arguments:
        corrects -- 1 for show only correct solutions, 0 for all
        exercise_id -- id of exercise to show solutions about
        """
        self.verify_session()
        tmpl = ENV.get_template('admin_info_exercise_solutions.html')
        if exercise_id:
            solutions = db.get_solutions(exercise_id=exercise_id)
            data = db.get_exercises(exercise_id)
            if corrects == 1:
                solutions = [solution for solution in solutions
                                if solution.correct == True]
            for solution in solutions:
                solution.submitted_code = nl2br(solution.submitted_code)
            return tmpl.render(friendly_name=data.friendly_name,
                               description=data.description,
                               output=data.expected_output,
                               time_limit=data.time_limit,
                               exercise_id=data.id,
                               solutions=solutions)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose()
    def edit_exercise(self, exercise_id=None):
        """ Exposes page for editing exervice or creating new one,
        if exercise_id is None.

        Keyword arguments:
        exercise_id -- id of exercise to edit
        """
        self.verify_session()
        tmpl = ENV.get_template('admin_edit_exercise.html')
        if exercise_id:
            data = db.get_exercises(exercise_id)
            return tmpl.render(friendly_name=data.friendly_name,
                               description=data.description,
                               output=data.expected_output,
                               time_limit=data.time_limit,
                               exercise_id=data.id)
        return tmpl.render()

    @cherrypy.expose()
    def delete_exercise(self, exercise_id=None):
        """ Exposes url for deleting exercises.

        Keyword arguments:
        exercise_id -- id of exercise to delete
        """
        self.verify_session()
        if exercise_id:
            db.delete_exercise(exercise_id)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose(alias='doEditExercise')
    def do_edit_exercise(self, exercise_id, friendly_name, description, output,
                         time_limit):
        """ Handles and edit or create action.

        Keyword arguments:
        exercise_id -- id of exercise to edit
        friendly_name -- user friendly name of exercise
        description -- description of exercise
        output -- expected script output
        time_limit -- time limit for exercise in minutes
        """
        self.verify_session()
        success = True
        if exercise_id:
            success = db.edit_exercise(exercise_id, friendly_name, description,
                                       output, time_limit)
        else:
            success = db.create_exercise(friendly_name, description, output,
                                         time_limit)

        if success:
            raise cherrypy.HTTPRedirect("/admin/console")
        else:
            raise cherrypy.HTTPRedirect("/admin/edit_exercise?exercise_id="+
                                        exercise_id)

    @cherrypy.expose()
    def edit_interview(self, interview_id=None, new=None):
        """ Exposes a page for editing or creating new interview.

        Keyword arguments:
        interview_id -- interview to edit
        """
        self.verify_session()
        tmpl = ENV.get_template('admin_edit_interview.html')
        exercise_list = db.get_exercises()
        if interview_id:
            data = db.get_interviews(interview_id)
            selected_exercises = db.get_interview_exercise_ids(interview_id)
            return tmpl.render(full_name=data.full_name,
                               username=data.username,
                               password=data.password,
                               exercises=exercise_list,
                               selected_exercises=selected_exercises,
                               interview_id=data.id)
        return tmpl.render(exercises=exercise_list)

    @cherrypy.expose()
    def delete_interview(self, interview_id=None):
        """ Exposes url for deleting interviews.

        Keyword arguments:
        interview_id -- id of interview to delete
        """
        self.verify_session()
        if interview_id:
            db.delete_interview(interview_id)
        raise cherrypy.HTTPRedirect("/admin/console")

    @cherrypy.expose(alias='doEditInterview')
    def do_edit_interview(self, interview_id, full_name, username, password,
                          exercise_ids=None):
        """ Handles form action for editing/creating  new interview.

        Keyword arguments:
        interview_id -- interview to edit
        full_name -- full name of interviewee
        username -- username for interviewee
        password -- access password to interview
        """
        self.verify_session()

        if exercise_ids is None:
            exercise_ids = []

        success = True
        if interview_id:
            success = db.edit_interview(interview_id, full_name, username,
                                        password, exercise_ids)
        else:
            success = db.create_interview(full_name, username, password,
                                          exercise_ids)

        if success:
            raise cherrypy.HTTPRedirect("/admin/console")
        else:
            raise cherrypy.HTTPRedirect("/admin/edit_interview?exercise_id="+id)

    def verify_session(self):
        """ Verifies if admin is logged in. Otherwise forwards to login page."""
        if 'loggedInAdmin' not in cherrypy.session:
            raise cherrypy.HTTPRedirect("/admin")

    @cherrypy.expose()
    def logout(self):
        """ Exposes a logout page. """
        cherrypy.session.clear()
        raise cherrypy.HTTPRedirect("/admin")

def initialize():
    """ Starts webserver. """
    index = Index()
    index.admin = AdminIndex()
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
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
