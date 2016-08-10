#!/usr/bin/env python

import webapp2
from page import Page

class Index(webapp2.RequestHandler):

    def get(self):
        page=Page()
        head,title,body=page.html_snippet()

        title.add_text("this is title")


        self.response.write(page.get_html())

app = webapp2.WSGIApplication([
    ('/', Index),
], debug=True)