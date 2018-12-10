import json
import os
import random
import time

from flask import (make_response, redirect, render_template, request,
                   send_file, send_from_directory, session, url_for)
from lib.task import taskset

from index import app

from .login import cklogin

task = taskset()


@app.route('/Task', methods=['GET', 'POST'])
@cklogin()
def TaskHome():
    return render_template('Task.html')


@app.route('/CreatTask', methods=['POST'])
@cklogin()
def CreatTask():
    data = request.values.to_dict()
    if data['type'] == 'week':
        if data['week'] == '7':
            data['week'] = 0
    data['creatTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data['taskID'] = str(time.time() + random.random())
    try:
        task.CreatTask(data)
    except Exception as e:
        return json.dumps({'resultCode': 1, 'result': str(e)})
    return json.dumps({'resultCode': 0, 'result': 'success'})


@app.route('/SelectTask', methods=['POST'])
@cklogin()
def SelectTask():
    return json.dumps({'resultCode': 0, 'result': task.GetTaskList()})


@app.route('/DeleteTask', methods=['POST'])
@cklogin()
def DeleteTask():
    try:
        taskid = request.values.get('taskid')
        task.DeleteTask(taskid)
    except Exception as e:
        return json.dumps({'resultCode': 1, 'result': str(e)})
    return json.dumps({'resultCode': 0, 'result': task.GetTaskList()})
