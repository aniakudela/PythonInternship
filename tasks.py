#!/usr/bin/env python

# CHAPTER II

import json
import sys
import os
import jsonpickle
import datetime


class ProgramArguments:
    def __init__(self, operation, name=None, deadline=None, description=None, task_hash=None, alltasks=False,
                 today=False):
        self.operation = operation
        self.name = name
        self.deadline = deadline
        self.description = description
        self.task_hash = task_hash
        self.alltasks = alltasks
        self.today = today

    def areValid(self):
        """Checks if valid arguments were given"""
        if self.operation == "add" and self.name is None:
            return False
        if (self.operation == "update" or self.operation == "remove") and self.task_hash is None:
            return False
        if self.operation == "list" and self.alltasks and self.today:
            return False
        return True


class Task:
    def __init__(self, task_hash, name, deadline="", description=""):
        self.name = name
        self.deadline = deadline
        self.description = description
        self.task_hash = task_hash

    def _prepareString(self, string):
        string.replace("\r\n", "\n")
        string.replace("\n\r", "\n")
        string.replace("\r", "\n")
        string.replace("\n", "\\n")
        return string

    def toStringRepresentation(self):
        return Task._prepareString(self.task_hash) + ";;" + Task._prepareString(self.name) + ";;" + Task._prepareString(
            self.deadline) + ";;" + Task._prepareString(self.description)


def fromStringRepresentation(strr):
    splitted = strr.split(";;")
    task_hash = int(splitted[0])
    name = splitted[1].replace("\\n", "\n")
    deadline = splitted[2]
    description = splitted[3]
    return Task(task_hash, name, deadline, description)


def processArguments():
    command = ProgramArguments(sys.argv[1])
    list_of_arguments = []
    for i in sys.argv:
        list_of_arguments.append(i)
    list_of_arguments = list_of_arguments[2:]
    while list_of_arguments:
        parameter = list_of_arguments[0]
        list_of_arguments.remove(list_of_arguments[0])
        if parameter == "--name" or parameter == "-n":
            param = list_of_arguments[0]
            list_of_arguments.remove(list_of_arguments[0])
            command.name = param
        elif parameter == "--deadline":
            param = list_of_arguments[0]
            list_of_arguments.remove(list_of_arguments[0])
            command.deadline = param
        elif parameter == "--description":
            param = list_of_arguments[0]
            list_of_arguments.remove(list_of_arguments[0])
            command.description = param
        elif parameter == "--all" or parameter == "-a":
            command.alltasks = True
        elif parameter == "--today" or parameter == "-t":
            command.today = True
        else:
            command.task_hash = parameter
    return command


def stringHash(task):
    """Creates the hash value for a specific task"""
    res = 0
    for c in task:
        res *= 31
        res += ord(c)
        res &= 0x0000FFFFFFFF
    return res


def doAdd(program_args):
    """Adds a task to a file"""
    new_task = Task(stringHash(program_args.name), name=program_args.name, deadline=program_args.deadline,
                    description=program_args.description)
    return new_task


def findObject(list_oftasks, hash_v):
    """Finds a taks with a specific hash value"""
    for tas in list_oftasks:
        if str(tas['task_hash']) == hash_v or tas['name'] == hash_v:
            return tas


def readTasks(path_):
    """Reads the file"""
    if os.path.exists(path_):
        with open(path_) as f:
            contents = f.read()
            contents = "[]" if len(contents) == 0 else contents
            return jsonpickle.decode(contents)
    else:
        with open("tasks.txt", "w") as new_file:
            new_file.write("[]")
            return []


def saveTasks(params, fil):
    """Saves the tasks in a file"""
    with open(fil, 'w') as ff:
        ff.write(jsonpickle.encode(params, unpicklable=False, make_refs=False))


program_arguments = processArguments()
if not program_arguments.areValid():
    print('Wrong arguments were given')
    sys.exit()
else:
    file = 'tasks.txt'
    list_of_tasks = readTasks(file)
    list_of_tasks_dec = jsonpickle.encode(list_of_tasks, unpicklable=False)
    if program_arguments.operation == "add":
        list_of_tasks.append(doAdd(program_arguments))
        saveTasks(list_of_tasks, file)
    if program_arguments.operation == "update":
        with open(file) as json_file:
            json_data = jsonpickle.dumps(json_file)
            found = findObject(list_of_tasks, program_arguments.task_hash)
            if program_arguments.name is not None:
                found['name'] = program_arguments.name
            if program_arguments.deadline is not None:
                found['deadline'] = program_arguments.deadline
            if program_arguments.description is not None:
                found['description'] = program_arguments.description
        saveTasks(list_of_tasks, file)
    if program_arguments.operation == "remove":
        with open(file) as json_file:
            json_data = jsonpickle.dumps(json_file)
            found = findObject(list_of_tasks, program_arguments.task_hash)
            list_of_tasks.remove(found)
        saveTasks(list_of_tasks, file)
    if program_arguments.operation == "list":
        if program_arguments.alltasks:
            print(list_of_tasks_dec)
        elif program_arguments.today:
            with open(file) as json_file:
                json_data = jsonpickle.dumps(json_file)
                today_tasks = list(filter(lambda atr: atr['deadline'] == str(datetime.date.today()), list_of_tasks))
                print(today_tasks)
