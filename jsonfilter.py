#!/usr/bin/env python

from flask import Flask, request, Response
import json
import dotenv
import os
import pika

app = Flask(__name__)
dotenv.load_dotenv()

def sendJsonToRmq(msg):

    slack = os.environ.get('QUEUE_SLACK')
    restapi = os.environ.get('QUEUE_RESTAPI')

    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=os.environ.get('RMQ_HOST'), port=os.environ.get('RMQ_PORT'), credentials=pika.PlainCredentials(os.environ.get('RMQ_LOGIN'), os.environ.get('RMQ_PASS'))))
    channel = connection.channel()

    channel.queue_declare(queue=slack)
    channel.queue_declare(queue=restapi)

    channel.basic_publish(exchange='', routing_key=os.environ.get('QUEUE_SLACK'), body=msg)
    channel.basic_publish(exchange='', routing_key=os.environ.get('QUEUE_RESTAPI'), body=msg)

    print("Done!")
    connection.close()

def parseOpened(data, base_issue, base_user):
    res = {}
    res['html_url'] = base_issue.get('html_url')
    res['id'] = base_issue.get('id')
    res['number'] = base_issue.get('number')
    res['state'] = base_issue.get('state')
    res['title'] = base_issue.get('title')
    res['body'] = base_issue.get('body')
    res['user'] = {}
    user = res['user']
    user['login'] = base_user.get('login')
    user['html_url'] = base_user.get('html_url')
    user['avatar_url'] = base_user.get('avatar_url')
    base_labels = base_issue['labels']
    labels = []
    for label in base_labels:
        a_label = {'name': label['name']}
        labels.append(a_label)
    res['labels'] = labels
    res['data'] = base_issue['created_at']
    res['repository'] = {}
    repo = res['repository']
    repo['name'] = data['repository']['name']
    repo['html_url'] = data['repository']['html_url']
    return res

def parseOther(base_issue, base_user):
    res = {}
    res['id'] = base_issue.get('id')
    res['state'] = base_issue.get('state')
    res['user'] = {}
    user = res['user']
    user['login'] = base_user.get('login')
    user['html_url'] = base_user.get('html_url')
    user['avatar_url'] = base_user.get('avatar_url')
    res['data'] = base_issue['updated_at']
    return res

# endpoint to listen for webhooks
@app.route('/', methods=['POST'])
def jsonFilter():
    try:
        data = request.json
        result_dict = {}
        action = data['action']
        base_issue = dict(data['issue'])
        base_user = dict(data['issue']['user'])
        print("[*] New Issue UPD: " + action)
        if action == 'opened':
            result_dict['action'] = action
            result_dict['issue'] = parseOpened(data, base_issue, base_user)            # selects required fields
        elif action == 'assigned':
            result_dict['action'] = action
            assignee = base_issue['assignee']
            result_dict['issue'] = parseOther(base_issue, assignee)                     # selects required fields
        else:
            result_dict['action'] = action
            result_dict['issue'] = parseOther(base_issue, base_user)

        json_result = json.dumps(result_dict, indent=4)         # result JSON

        
        print(json_result)

        sendJsonToRmq(json_result)              # send msg to RMQ

        status_code = Response(status=200)                      # sends status '200 OK' in response
        return status_code

    except ValueError as err:
        status_code = Response(status=500)  # send status 'OK' in response
        return status_code, err

if __name__ == '__main__':
    app.run(os.environ.get('HOST'), os.environ.get('PORT'))     # use environmental variables for host addr and port
    # app.run()


    