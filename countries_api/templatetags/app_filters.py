# countries_api/templatetags/app_filters.py
import json
from django import template

register = template.Library()

@register.filter(name='to_json_object_string')
def to_json_object_string(value):
    print(f"---- CUSTOM FILTER CALLED ----") # Add this line
    print(f"FILTER INPUT: type(value)={type(value)}, repr(value)={repr(value)}")
    
    if not value:
        actual_value = {} if value is None else value
    else:
        actual_value = value

    try:
        if not isinstance(actual_value, (dict, list)):
            print(f"WARNING: to_json_object_string received non-dict/list: {type(actual_value)}")
            return '{}'

        json_string = json.dumps(actual_value)
        print(f"FILTER json.dumps OUTPUT: {repr(json_string)}")
        return json_string
    except TypeError as e:
        print(f"ERROR: TypeError in json.dumps within filter: {e}, value was: {repr(actual_value)}")
        return '{}'