import json, boto3, botocore.exceptions
import re
from xml.dom import minidom
from lib import func
from boto3.dynamodb.conditions import Key
f1 = func.func()
bucket_name = "garetgv"
def lambda_handler(event, context):
    
    global bucket_name
    path = event["path"].split("/")
    path = path[len(path)-1]
    
    if path == "list_races":
        sess= boto3.Session(region_name='us-east-1')
        ddb= sess.client('dynamodb')
        table = "TokenTable"
        TableItems = ddb.scan(TableName = table)["Items"]
        item ={}
        y = '{ "evento": ['
        for x in range(len(TableItems)): 
            gara = {
                
                "race_name" : TableItems[x]["raceName"]["S"],
                "race_date" : TableItems[x]["raceDate"]["S"],
                "race_id"   : TableItems[x]["race_id"]["S"]
            }
            print(gara)
            if x != len(TableItems) -1 :
                y = y + str(gara) + ","
            else:
                y = y + str(gara) 
            
        y = y + "]}"
        y = re.sub('[\']', '\"', y)
        return {
            'statusCode': 200,
            'body': y
        }
    elif path.split("?")[0]=="list_classes":
        sess= boto3.Session(region_name='us-east-1')
        ddb= sess.client('dynamodb')
        table = "GareOrienteering"
        id = event["queryStringParameters"]["id"]
        TableItems = ddb.scan(TableName = table)["Items"]
        
        item ={}
        for x in range(len(TableItems)):
            
            if id == TableItems[x]["race_id"]["S"]:
                evento = "evento"+ str(x+1)
                gara = {
                        
                    "race_id"   : id,
                    "categoria" : TableItems[x]["Categoria"]["S"]
                }
                item[evento]=gara
    
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
                
            
    elif path.split("?")[0]=="results":
        
        if len(event["queryStringParameters"]) == 2:
            filename = event["queryStringParameters"]["id"]+event["queryStringParameters"]["Categoria"]+".xml"
            s3 = boto3.resource("s3")
            
            try:
                s3_client = boto3.client("s3")
                file = s3_client.get_object(Bucket=bucket_name, Key=filename)["Body"].read()
                
                xmldoc = minidom.parseString(file)
                result = f1.simulator(xmldoc)
                
            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code']=="NoSuchKey":
                    return {
                        'statusCode': 403,
                        'body': "id o classe non trovato"
                    }
                else: 
                    return {
                        'statusCode': 400,
                        'body': "errore non specificato"
                    }
                        
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            
            organizzazione = event["queryStringParameters"]["organization"]
            
            filename = event["queryStringParameters"]["id"]+event["queryStringParameters"]["Categoria"]+".xml"
            s3 = boto3.resource("s3")
        
            s3_client = boto3.client("s3")
            file = s3_client.get_object(Bucket=bucket_name, Key=filename)["Body"].read()
            
            xmldoc = minidom.parseString(file)
            lista  = xmldoc.getElementsByTagName("ClassResult")
            atleti = []
            
                   
            for k in range(len(lista[0].getElementsByTagName("PersonResult"))):
                if lista[0].getElementsByTagName("Organisation")[k].getElementsByTagName("Name")[0].firstChild.data == organizzazione: 
                    atleta = str(lista[0].getElementsByTagName("PersonResult")[k].getElementsByTagName("Family")[0].firstChild.data) + " " + str(lista[0].getElementsByTagName("PersonResult")[k].getElementsByTagName("Given")[0].firstChild.data)
                    atleti.append(atleta)
                    
            atleti = sorted(atleti, key=lambda x:(x[0]))        
            return {
                'statusCode': 200,
                'body': json.dumps(atleti)
            }
    
    else :
       return { 
            'statusCode': 300,
            'body': json.dumps("ERRORE: Ricontrollare endpoint inserito")
                }





