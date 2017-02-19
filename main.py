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
import webapp2
import cgi
import os
import jinja2
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Post(db.Model):
    title = db.StringProperty(required = True)
    entry = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **b):
        self.response.write(*a)
    def render_str(self,template, **b):
        t = jinja_env.get_template(template)
        return t.render(b)
    def render(self,template, **c):
        self.write(self.render_str(template, **c))
#submission page
t = jinja_env.get_template("title.html")
main_page = t.render()
class MainPage(Handler):
    def render_front(self, title="", entry="", error=""):
        self.render("title.html", title = title, entry=entry, error=error)

    def get(self):
        self.render_front()
    def post(self):
        title = self.request.get("title")
        entry = self.request.get("entry")
        created = self.request.get("created")

        if title and entry:
            a = Post(title = title, entry = entry)
            a.put()
            self.redirect("/blog")
        else:
            error = "Sorry, we need both a title and a blog post"
            self.render_front(title, entry, error = error)
class Blog(MainPage):
    def get(self):
        entry_list = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC limit 5")

        #self.render("title.html", entry_list)
        self.render("database.html", entry_list = entry_list)

    # def post(self):
    #     test="test"

app = webapp2.WSGIApplication([
    ('/newpost', MainPage),
    ('/blog', Blog)
], debug=True)
