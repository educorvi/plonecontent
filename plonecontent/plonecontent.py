# -*- coding: utf-8 -*-
import pkg_resources
import json

from django.template import Context, Template
from restclient import GET

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class PloneContentXBlock(XBlock):
    """
    This XBlock reads the content of a content-Object stored in CMS-Plone.
    The Plone-data will be read over json-interface. You need to install
    the plone.restapi package at plone-site.
    """

    # Fields

    display_name = String(display_name="Anzeigename",
        default="Plone-Content",
        scope=Scope.settings,
        help="Dieser Name erscheint im Kopf des Dokuments im Kursinhalt.")

    url = String(display_name="Content-URL",
        default="http://plone-site/path/path",
        scope=Scope.content,
        help="Die Webadresse des Plone-Contents.")

    username = String(display_name="Benutzername",
            scope=Scope.content,
            help=u"Falls eine Anmeldung erforderlich ist können Sie hier den Benutzernamen eintragen.")

    password = String(display_name="Passwort",
            scope=Scope.content,
            help=u"Falls eine Anmeldung erforderlich ist können Sie hier das Passwort eintragen.")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, template_path, context={}):
        """ 
        Evaluate a template by resource path, applying the provided context
        """
        template_str = self.load_resource(template_path)
        return Template(template_str).render(Context(context))


    # TO-DO: change this view to display your data your own way.

    def format_plonedocument(self, data):
        context = {}
        context['title'] = data['title']
        context['description'] = data['description']
        context['text'] = data['text']['data']
        mytemplate = "static/html/plonedocument.html"
        return (context, mytemplate)

    def student_view(self, context=None):
        """
        The primary view of the PloneContentXBlock, shown to students
        when viewing courses.
        """
        if self.username and self.password:
            myresponse = GET(self.url, accept=['application/json'], credentials=(self.username, self.password))
        else:
            myresponse = GET(self.url, accept=['application/json'])
        data = json.loads(myresponse)
        if data['@type'] == "Document":
            context, mytemplate = self.format_plonedocument(data)
        else:
            context = {'title':data.get('title'),
                       'description':data.get('description'),
                       'display_name':self.display_name,
                       'url':self.url}
            mytemplate = "static/html/plonecontent.html"
        html = self.render_template(mytemplate, context)
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/plonecontent.css"))
        frag.add_javascript(self.resource_string("static/js/src/plonecontent.js"))
        frag.initialize_js('PloneContentXBlock')
        return frag

    def studio_view(self, context=None):
        """ 
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'username': self.username,
            'password': self.password,
            }
        html = self.render_template('static/html/plonecontent_edit.html', context)
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/plonecontent.css"))
        frag.add_javascript(self.resource_string("static/js/src/plonecontent.js"))
        frag.initialize_js('PloneContentXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def save_plonecontent(self, data, suffix=''):
        """
        Saving handler
        """
        self.display_name = data['display_name']
        self.username = data['username']
        self.password = data['password']
        self.url = data['url']
        return {'result':'success'}

    #def increment_count(self, data, suffix=''):
    #    """
    #    An example handler, which increments the data.
    #    """
    #    # Just to show data coming in...
    #    assert data['hello'] == 'world'
    #
    #    self.count += 1
    #    return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PloneContentXBlock",
             """<plonecontent/>
             """),
            ("Multiple PloneContentXBlock",
             """<vertical_demo>
                <plonecontent/>
                <plonecontent/>
                <plonecontent/>
                </vertical_demo>
             """),
        ]
