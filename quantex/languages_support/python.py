import json

class Python:
    def __init__(self, api):

        python_syntax = {}
        with open('languages_support/json/python.json', 'r') as f:
            python_syntax = json.load(f)
        
        for type in python_syntax:
            for syntax in python_syntax[type]:
                api.add(syntax)