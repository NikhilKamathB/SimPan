import json
from django import template

register = template.Library()

@register.filter
def parse_json(value):
    return json.loads(value)