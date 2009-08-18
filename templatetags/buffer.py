from django import template
from django.db import models

register = template.Library()

Comic = models.get_model("nr_comics", "comic")

def do_buffer(parser, token):
    tokens = token.split_contents()
    if len(tokens) != 1:
        raise template.TemplateSyntaxError, "%r tag takes no arguments" % (tokens[0],)
    return BufferNode()

class BufferNode(template.Node):
    def render(self, context):
        try:
            c = Comic.comics.future().count()
        except:
            c = 0
        return c

register.tag('buffer', do_buffer)
            