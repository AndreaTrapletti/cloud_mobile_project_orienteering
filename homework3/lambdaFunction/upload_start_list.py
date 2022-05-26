import json

import boto3,botocore.exceptions
from xml.dom import minidom

bucket_name= "garetgv"


def lambda_handler(event, context):
    global bucket_name

    race_id = event["queryStringParameters"]["race_id"]
    encoded_string = event["body"].encode("utf-8")
   
    xmldoc = minidom.parseString(encoded_string)
    gare=  xmldoc.getElementsByTagName('ClassStart')
    
    for i in gare:
        a = True    
        start_list = i.getElementsByTagName('Name')
        start_list = str(start_list[0].firstChild.data)
        file_name = "start_list/GRIGLIA_" + race_id + start_list+ ".xml"
        s3 = boto3.resource("s3")
        try:
            s3_client = boto3.client("s3")
            s3_client.get_object(Bucket=bucket_name, Key=file_name)
            
        except botocore.exceptions.ClientError as error:
            a = False
            if error.response['Error']['Code']=="NoSuchKey":
                s3.Bucket(bucket_name).put_object(Key=file_name, Body = i.toxml())
            else: 
                 return {
                    'statusCode': 400,
                    'body': "errore non specificato"
                    }
        if a == True : 
            s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            s3.Bucket(bucket_name).put_object(Key=file_name, Body = i.toxml())
    return {
        'statusCode': 200,
        'body': event["body"]
        }
