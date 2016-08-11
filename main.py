#!/usr/bin/env python

import webapp2
from page import Page
from material_design import MDLPage

class Index(webapp2.RequestHandler):
    def get(self):
        page=MDLPage("TimebotPy - Home")

        # grid in total of 12
        page.add_grid((4,4,4))

        #add buttons to row cols..
        page.add_flat_button("Button1").next()
        page.add_fab_button("add").add_fab_button("face").next()
        page.add_raised_button("Button3").next()

        self.response.write(page.get_html())

app = webapp2.WSGIApplication([
    ('/', Index),
], debug=True)