import json

def getImports():
    return json.load(open("Imports.json", "r"))

def getCalls():
    return json.load(open("Calls.json", "r"))