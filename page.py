#!/usr/bin/env python

class Tag(object):

    def __init__(self,tag_name=''):
        self.name=tag_name
        self.close_tag=True
        self.attrs={}
        self.childs=[]
        self.text=""
        self.data=""
        pre_tabs = ""
        self.flaten=False

    def flat(self,b=True):
        self.flaten=b

    def add_tag(self,tag):
        self.childs.append(tag)
        return tag

    def set_attrs(self,attrs_dict):
        self.attrs=attrs_dict

    def add_class(self,class_name):
        if not 'class' in self.attrs:
            self.attrs['class']=''

        self.attrs['class']+=" %s" % class_name
        self.attrs['class']=self.attrs['class'].strip()

    def add_attr(self,attr_key,attr_value):
        self.attrs[attr_key]=attr_value

    #add with html tag string
    def add_tag_data(self,new_tag,data):
        new_tag.data=data
        return self.add_tag(new_tag)

    def add_tag_name(self,new_tag,attrs={},close_tag=True):
        if attrs:
            new_tag.set_attrs(attrs)
        new_tag.close_tag=close_tag
        return self.add_tag(new_tag)

    def set_text(self,t):
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

        if self.flaten:
            result=result.replace('\t','')
            result=pre_tabs+result.replace('\n','')+'\n'
            return result

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
        head = self.add_tag_name(Tag("head"))
        title = head.add_tag_name(Tag("title"))
        body = self.add_tag_name(Tag("body"))

        return (head,title,body)

    def add_stylesheet(self,url):
        self.head.add_tag_name(Tag("link"), {'rel': 'stylesheet','href': url})

    def add_js(self,url,defer=False):
        if defer:
            attrs={'src': url,'defer':None}
        else:
            attrs={'src': url}

        self.head.add_tag_name(Tag("script"), attrs,True)