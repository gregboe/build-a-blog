#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Post(db.Model):

    title = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **params):
        self.write(self.render_str(template,**params))

class MainPage(Handler):
    def render_main(self, title="", body="",error=""):

        self.render("main.html",title=title, body=body,error=error)

    def get(self):
        self.render("main.html")

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        error = "We need a title and content!"

        if title and body:
            p = Post(title=title,body=body)
            p.put()

            self.redirect('/blog')

        else:
            self.render_main(title,body,error)

class BlogHandler(Handler):

    def get(self):

        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("blog.html", posts=posts)

    def post(self):

        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC")

        self.render("blog.html", posts=posts)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogHandler),
], debug=True)
