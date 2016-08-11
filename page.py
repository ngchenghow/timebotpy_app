#!/usr/bin/env python

class Tag(object):
    attrs={}
    name=""
    childs=[]
    text=""
    close_tag=True

    data=""

    def __init__(self,tag_name):
        self.name=tag_name
        self.close_tag=True
        self.attrs={}
        self.childs=[]
        self.text=""
        pre_tabs = ""

    def add_tag(self,tag):
        self.childs.append(tag)
        return tag

    def set_attrs(self,attrs_dict):
        self.attrs=attrs_dict

    #add with html tag string
    def add_tag_data(self,data):
        new_tag=Tag('')
        new_tag.data=data
        return self.add_tag(new_tag)

    def add_tag_name(self,tag_name,attrs={},close_tag=True):
        new_tag=Tag(tag_name)
        new_tag.set_attrs(attrs)
        new_tag.close_tag=close_tag
        return self.add_tag(new_tag)

    def add_text(self,t):
        self.text=t

    def render(self,pre=0):
        pre_tabs = "\t" * pre

        if self.data:
            return pre_tabs+self.data+"\n"

        result=""

        attrs_str=""

        for attr,value in self.attrs.iteritems():
            if(value!=None):
                attrs_str+=" %s='%s'" % (attr,value)
            else:
                attrs_str+=" %s" % (attr)

        if not attrs_str.strip():
            attrs_str=""

        if self.childs:
            result+="\n"
            for child in self.childs:
                result+=child.render(pre+1)
            result="%s<%s%s>%s%s%s</%s>\n" % (pre_tabs,self.name,attrs_str,pre_tabs,result,pre_tabs,self.name)
        elif self.text:
            result+="%s<%s%s>%s</%s>\n" % (pre_tabs,self.name,attrs_str,self.text,self.name)
        else:
            result+="%s<%s%s>" % (pre_tabs,self.name,attrs_str)
            result += "</%s>\n" % (self.name) if self.close_tag else "\n"

        return result


class Page(Tag):
    doc_type="<!DOCTYPE html>"
    head=""
    body=""

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

    def add_stylesheet(self,url):
        self.head.add_tag_name("link", {'rel': 'stylesheet','href': url},False)

    def add_js(self,url,defer=False):
        if defer:
            attrs={'src': url,'defer':None}
        else:
            attrs={'src': url}

        tag=self.head.add_tag_name("script", attrs,True)