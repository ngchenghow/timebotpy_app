#!/usr/bin/env python

import webapp2
from page import Page
from material_design import MDLPage,MDLTag

class Index(webapp2.RequestHandler):
    def get(self):
        page=MDLPage("TimebotPy - Home")

        # grid in total of 12
        page.add_grid((4,4,4))

        #add buttons to row cols..
        page.add_flat_button("Button1")
        page.next()

        page.add_fab_button("add")
        page.add_fab_button("face")
        page.next()

        page.add_raised_button("Button3")
        page.next()

        #badges grid
        page.add_grid((4,6,2))

        page.add_flat_button("Button1")
        page.add_link('link with badge','http://www.google.com').add_badge('12')
        page.add_plain_fab_button("account_box")
        page.next()

        page.add_fab_button("account_box")

        page.add_fab_button("face")
        page.next()

        page.add_raised_button("Button3")
        page.next()

        #cards
        page.add_grid((4,4,4))
        page.add_div().card().add_div().card_title("Welcome")

        self.response.write(page.get_html())

app = webapp2.WSGIApplication([
    ('/', Index),
], debug=True)