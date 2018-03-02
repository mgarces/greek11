import boto3
import json

def respond(status, message=""):
    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "headers": {"whatevs": "yeah"},
        "body": json.dumps({
            "messages": message})
        
    }

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    tag_key = '{}'.format(request_body['tag_key'])
    tag_value = '{}'.format(request_body['tag_value'])
    message = list_instances_by_tag(tag_key, tag_value)
    return respond(200,message)


# returns a list of instances by defined tag
def list_instances_by_tag(tag_key, tag_value):
    ec2 = boto3.client('ec2')
    instance_ids = []
    filters = [{
        'Name': 'tag:' + tag_key,
        'Values': [tag_value]
    }]
    list_ids = ec2.describe_instances(Filters=filters)
    for reservation in list_ids["Reservations"]:
        for instance in reservation["Instances"]:
            instance_ids.append(instance["InstanceId"])
    return instance_ids