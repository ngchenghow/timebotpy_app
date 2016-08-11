#!/usr/bin/env python
from page import Page,Tag

class MDLTag(Tag):
    def __init__(self,tag_name):
        super(MDLTag, self).__init__(tag_name)

    def add_badge(self,title,no_bg=False):
        self.add_class("mdl-badge")
        if no_bg:
            self.add_class("mdl-badge--no-background")

        self.add_attr("data-badge",title)
        return self

    def card(self):
        self.add_class("demo-card-wide mdl-card mdl-shadow--2dp")
        return self

    def card_title(self,title):
        self.add_class("mdl-card__title")
        h2_tag=self.add_tag_name(MDLTag("h2"))
        h2_tag.add_class("mdl-card__title-text")
        h2_tag.set_text(title)
        return self

    def add_div(self):
        new_tag=self.add_tag_name(MDLTag("div"))
        return new_tag


class MDLPage(Page):

    def __init__(self,title):
        super(MDLPage, self).__init__()
        self.stack=[]
        self.head, self.title, self.body = self.html_snippet()
        self.title.set_text(title)
        self.head.add_tag_data(MDLTag(''),'''<meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">''')
        self.add_stylesheet(r'https://fonts.googleapis.com/icon?family=Material+Icons')
        self.add_stylesheet(r'https://code.getmdl.io/1.1.3/material.indigo-pink.min.css')
        self.add_js(r'https://code.getmdl.io/1.1.3/material.min.js')


    #buttons
    def add_flat_button(self,title):
        tag = self.stack[0]
        new_tag=MDLTag('button')
        new_tag.set_text(title)
        tag.add_tag_name(new_tag,{'class':'mdl-button mdl-js-button mdl-js-ripple-effect'})
        return new_tag


    def add_raised_button(self,title):
        tag = self.stack[0]
        new_tag=MDLTag('button')
        new_tag.set_text(title)
        tag.add_tag_name(new_tag,{'class':'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent'})

        return new_tag


    def add_fab_button(self,title):
        tag = self.stack[0]
        new_tag=self.create_icon_button(title,'mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect mdl-button--colored')
        tag.add_tag(new_tag)
        return new_tag

    def add_plain_fab_button(self,title):
        tag = self.stack[0]
        new_tag = self.create_icon_button(title,'mdl-button mdl-js-button mdl-button--fab mdl-js-ripple-effect')
        tag.add_tag(new_tag)
        return new_tag

    def create_icon_button(self,icon,class_name):
        new_tag = MDLTag('button')
        i_tag = MDLTag('i')
        i_tag.set_text(icon)
        i_tag.add_class('material-icons')
        new_tag.add_tag_name(i_tag)
        new_tag.add_class(class_name)
        new_tag.flat()
        return new_tag

    def add_grid(self,cols):
        # type: (int) -> object
        root_div=self.body.add_tag_name(MDLTag("div"),{'class':'mdl-grid'})
        childs_div=[]

        for num in cols:
            childs_div.append(root_div.add_tag_name(MDLTag("div"),{'class':'mdl-cell--%d-col'%(num)}))

        self.stack.extend(childs_div)
        return childs_div

    def add_link(self,text,url):
        tag = self.stack[0]
        a_tag=tag.add_tag_name(MDLTag('a'),{'href':url})
        a_tag.set_text(text)
        return a_tag

    def add_div(self):
        tag = self.stack[0]
        div_tag = tag.add_tag_name(MDLTag('div'))
        return div_tag

    def next(self):
        self.stack.pop(0)
        return self

    def get_tag(self):
        return self.stack[0]



