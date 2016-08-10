#!/usr/bin/env python

class Tag(object):
    attr={}
    name=""
    childs=[]
    text=""

    def __init__(self,tag_name):
        self.name=tag_name
        self.attr={}
        self.childs=[]
        self.text=""
        pre_tabs = ""

    def add_tag(self,tag):
        self.childs.append(tag)
        return tag

    def add_tag_name(self,tag_name):
        new_tag=Tag(tag_name)
        return self.add_tag(new_tag)

    def add_text(self,t):
        self.text=t

    def render(self,pre=0):
        result=""
        if len(self.childs)>0:
            for child in self.childs:
                result+=child.render(pre+1)
            pre_tabs="\t" * pre
            result="%s<%s>\n%s%s%s</%s>\n" % (pre_tabs,self.name,pre_tabs,result,pre_tabs,self.name)
        else:
            result+="\t<%s>%s</%s>\n" % (self.name,self.text,self.name)

        return result


class Page(Tag):
    doc_type="<!DOCTYPE html>"

    def __init__(self):
        super(Page, self).__init__("html")
        self.name="html"

    def get_html(self):
        return self.doc_type+'\n'+self.render()

    def html_snippet(self):
        head = self.add_tag_name("head")
        title = head.add_tag_name("title")
        body = self.add_tag_name("body")

        return (head,title,body)
