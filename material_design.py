#!/usr/bin/env python
from page import Page

class MDLPage(Page):

    def __init__(self,title):
        super(MDLPage, self).__init__()
        self.stack=[]
        self.head, self.title, self.body = self.html_snippet()
        self.title.add_text(title)
        self.head.add_tag_data('''<meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">''')
        self.add_stylesheet(r'https://fonts.googleapis.com/icon?family=Material+Icons')
        self.add_stylesheet(r'https://code.getmdl.io/1.1.3/material.indigo-pink.min.css')
        self.add_js(r'https://code.getmdl.io/1.1.3/material.min.js')

    def add_flat_button(self,title):
        tag = self.stack[0]
        tag.add_tag_data('<button class="mdl-button mdl-js-button mdl-js-ripple-effect">%s</button>' % (title))
        return self

    def add_raised_button(self,title):
        tag = self.stack[0]
        tag.add_tag_data('<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">%s</button>' % (title))
        return self

    def add_fab_button(self,title):
        tag = self.stack[0]
        tag.add_tag_data('<button class="mdl-button mdl-js-button mdl-button--fab mdl-button--colored mdl-js-ripple-effect"><i class="material-icons">%s</i></button>' % (title))
        return self

    def add_grid(self,cols):
        # type: (int) -> object
        root_div=self.body.add_tag_name("div",{'class':'mdl-grid'})
        childs_div=[]

        for num in cols:
            childs_div.append(root_div.add_tag_name("div",{'class':'mdl-cell--%d-col'%(num)}))

        self.stack.extend(childs_div)
        return childs_div

    def next(self):
        self.stack.pop(0)
        return self