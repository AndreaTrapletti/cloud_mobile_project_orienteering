import json, boto3, botocore.exceptions
from xml.dom import minidom
from boto3.dynamodb.conditions import Key
bucket_name = "garetgv"
def lambda_handler(event, context):
    global bucket_name
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('GareOrienteering')
    id = event["params"]["querystring"]["id"]
        
    response = table.query(ProjectionExpression="Categoria", KeyConditionExpression= Key('race_id').eq(id))
    doc = minidom.Document()
    roots = doc.createElement("ResultList")
    roots.setAttribute("xmlns","http://www.orienteering.org/datastandard/3.0")
    roots.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    for i in range(len(response["Items"])):
        filename = id +response["Items"][i]["Categoria"]+".xml"
        s3 = boto3.resource("s3")
        s3_client = boto3.client("s3")
        file = s3_client.get_object(Bucket=bucket_name, Key=filename)["Body"].read()
        root= minidom.parseString(file).documentElement
        roots.appendChild(root)
        doc.appendChild(roots)
    return doc.toxml(encoding="utf-8")
