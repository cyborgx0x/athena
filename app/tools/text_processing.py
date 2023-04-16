import json
from datetime import datetime
from flask import Markup



class Process: 
    def __init__(self, app):
        
        ''''
        initialize the processing
        '''
        app.jinja_env.filters.setdefault('render', self)
    
    def __call__(self, stream):
        if stream:
            return self.editor_to_html(stream)
        else:
            return "Opps... nothing here"

    def text_to_json(self, text):
        '''
        take a text and return a json format that can be use in editorjs
        '''
        pass
    def editor_to_html(self, stream):
        '''
        take a json format from editorjs and return a text strings
        '''
        render = []
       
        for item in stream["blocks"]:
            if item["type"] == "paragraph":
                render.append("<p>" + item["data"]["text"] + "</p>")
            elif item["type"] == "header":
                render.append("<h2>" + item["data"]["text"] + "</h2>")
            elif item["type"] == "list":
                render.append(str(item["data"]))
            elif item["type"] == "image":
                render.append("<img class='render-image' src='{0}'>".format(item["data"]["file"]["url"]))
        output = "\n".join(render)
        return Markup(output)
