import uuid
import json
import boto3
from datetime import date
from xml.dom import minidom
from lib import funzioni,Simulatore
f1 = funzioni.func()
simulatore = Simulatore.simulator()
contFile = 1

bucket_name= "xmlverdi"

def lambda_handler(event, context):
    
    metodo = event["httpMethod"]
    global bucket_name, contFile
    s3_client = boto3.client("s3")
    s3 = boto3.resource("s3")
    if metodo == "POST" :
        content = event["body"]
        
        if content[0]!="<":
            content= f1.pulizia(content)
            nomefile = "fileintero" + str(contFile) + ".xml"
            filepath = "fileinteri/" + nomefile
            sess= boto3.Session(region_name='us-east-1')
            ddb= sess.client('dynamodb')
            table = 'GareOrienteering'
            s3.Bucket(bucket_name).put_object(Key=filepath, Body = content)
            contenutofile =s3_client.get_object(Bucket=bucket_name, Key=filepath)["Body"].read() 
            contFile= contFile + 1
            f1.caricamentoDB(contenutofile)
            return{
                'statusCode': 200,
                'body': content
            }
        else:
            encoded_string = content.encode("utf-8")
            f1.caricamentoDB(encoded_string)
            return {
                'statusCode': 200,
                'body': event["body"]
            }
    elif metodo == "GET" :
        key = event["path"]
        key = key.split("/")
        lung = len(key)-1
        bucket = s3.Bucket(bucket_name)
        if key[lung] == bucket_name:
            
            listanomi=[]
            for key2 in bucket.objects.all():
                listanomi.append(key2.key)
            return {
                'statusCode': 200,
                'body': json.dumps(listanomi)
                }
        elif key[lung-1]=="fileinteri":
            path = key[lung-1]+"/"+key[lung]
            file_content = s3_client.get_object(Bucket=bucket_name, Key=path)["Body"].read()
            return{
                'statusCode': 200,
                'body': file_content
            };
        else:
            file_content = s3_client.get_object(Bucket=bucket_name, Key=key[lung])["Body"].read()
            return{
                'statusCode': 200,
                'body': file_content
            };
    elif metodo == "PUT":
        content = event["body"] 
        
        lista = simulatore.simulatore(content)
        return{
            'statusCode': 200,
            'body': json.dumps(lista)
        }
        
        
    else: #nel caso in futuro implementeremo altri metodi, al momento non dovrebbe mai servire
        return{
            'statusCode': 200,
            'body': json.dumps("cribbio metodo sbagliato")
        }
        

        