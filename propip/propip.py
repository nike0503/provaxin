#!/usr/bin/env python
# coding: utf-8

# In[15]:


import os
import json
import inspect
import re
import sys
import time
import importlib


# In[16]:


ImportBlackList = json.load(open("RULES/Imports.json", "r"))
ImportWhiteList = ['numpy','matplotlib','matplotlib.pyplot','random','math','scikit-learn','time','json','re','sys']
CallsBlackList = json.load(open("RULES/Calls.json","r"))
ImportDict = {}


# In[17]:


def get_code(filename):
        if os.path.isfile(filename):
            try:
                f = open(filename, "r")
            except Exception as opn_fle_err:
                time.sleep(0.8)
                print ('\n')
                exit("File could not be opened.\nReason: {} .".format(str(opn_fle_err)))
        else:
            time.sleep(0.8)
            print ('\n')
            exit('Specified file does not exist.')
        contents=f.read().split('\n')
        f.close()
        return contents

def check_imports(import_file, line_number, report):
    if import_file[0]=='`':
        import_file = import_file[1:-1]

    if import_file in ImportWhiteList:
        return

    for data in ImportBlackList['Import']:
        if import_file in data['qualnames']:
            if(not report.__contains__(line_number)):
                report[line_number] = []
            report[line_number].append({
                "code": "import " + import_file,
                "cwe": data["cwe"],
                "message": data["message"],
                "level": data["level"]
            })
            return
    if ImportDict.__contains__(import_file):
        if(not report.__contains__(line_number)):
            report[line_number] = []
        report[line_number].append(ImportDict[import_file])
    else:
        if importlib.util.find_spec(import_file) is None:
            if(not report.__contains__(line_number)):
                report[line_number] = []
            report[line_number].append({
                "code": "import " + import_file,
                "cwe": data["cwe"],
                "message": data["message"],
                "level": data["level"]
            })
            return

        import_code = str(inspect.getsource(importlib.import_module(import_file)))

        if(not report.__contains__(line_number)):
            report[line_number] = []
        ImportDict[import_file] = {}
        ImportDict[import_file] = {
            "code": "import " + import_file,
            "report": check_code(import_code.split("\n"))
        }
        report[line_number].append(ImportDict[import_file])

def update_module(words,module):
    if len(words) == 2:
        module[words[1]] = words[1]
    elif len(words) == 4:
        if words[2] == "as":
            module[words[3]] = words[1]
        elif words[3]!="*":
            module[words[1]+"."+words[3]] = words[1]+"."+words[3]
        else:
            module[words[1]] = words[3]
    elif len(words) == 6:
        module[words[5]] = words[1]+"."+words[3]

def update_report(report,line_no):
    if report.__contains__(line_no):
        for data in report[line_no]:
            if data.__contains__('level'):
                report[data['level']] += 1
            elif data.__contains__('report'):
                report['LOW'] += data['report']['LOW']
                report['MEDIUM'] += data['report']['MEDIUM']
                report['HIGH'] += data['report']['HIGH']

def update_report_data(data,report,line_number,qualname):
    if(not report.__contains__(line_number)):
        report[line_number] = []
    report[line_number].append({
        "code": "call " + qualname,
        "cwe": data["cwe"],
        "message": data["message"],
        "level": data["level"]
    })
    report[data["level"]] += 1


def check_code(file_code):
    report = {"LOW":0,"MEDIUM":0,"HIGH":0}
    modules = {}
    line_no = 0

    for line in file_code:
        line_no += 1
        words = re.split(r"[(,)\s\t]\s*\t*",line)

        if '' in words:
            words.remove("")

        if len(words) == 0 or words[0] == "#":
            continue
        elif words[0] == "import":
            update_module(words,modules)
            check_imports(words[1],line_no,report)
            update_report(report,line_no)
            continue
        elif words[0] == "from":
            update_module(words,modules)
            if words[3] != "*":
                check_imports(words[1]+"."+words[3],line_no,report)
            else:
                check_imports(words[1],line_no,report)
            update_report(report,line_no)
            continue

        for call in words:
            if("." in call):
                for data in CallsBlackList['Call']:
                    for qualname in data['qualnames']:

                        if call == qualname:
                            update_report_data(data,report,line_no,qualname)
                            continue

                        flag = 0
                        for module in modules:
                            if len(qualname) >= len(call) + len(module) + 1:
                                if qualname.startswith(module+".") and qualname.endswith(call):
                                    update_report_data(data,report,line_no,qualname)
                                    flag = 1
                                    break  
                        if flag:
                            continue

                        calls = call.split(".")
                        qual_split = qualname.split(".")

                        if modules.__contains__(calls[0]):
                            call = modules[calls[0]]
                            for method in calls[1:]:
                                call += "."+method
                            if call == qualname:
                                update_report_data(data,report,line_no,qualname)
    return report



# In[18]:


vulnerable_file = sys.argv[1]
f_code = get_code(vulnerable_file)
analysis = check_code(f_code)
open("ANALYSIS/analysis.json","w").write(json.dumps(analysis,indent=4))
