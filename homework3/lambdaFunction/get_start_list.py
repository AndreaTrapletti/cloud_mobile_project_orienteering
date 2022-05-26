import json, boto3, botocore.exceptions
import re
from xml.dom import minidom


bucket_name = "garetgv"

def lambda_handler(event, context):
    
    global bucket_name
    sess= boto3.Session(region_name='us-east-1')
    
    #ddb= sess.client('dynamodb')
    #table = "GareOrienteering"
    id = event["queryStringParameters"]["id"]
    categoria = event["queryStringParameters"]["Categoria"]
    #TableItems = ddb.scan(TableName = table)["Items"]
    filename = "GRIGLIA_"+event["queryStringParameters"]["id"]+event["queryStringParameters"]["Categoria"]+".xml"
    s3 = boto3.resource("s3")
    
    try:
        s3_client = boto3.client("s3")
        file = s3_client.get_object(Bucket=bucket_name, Key="start_list/"+filename)["Body"].read()
        
        xmldoc = minidom.parseString(file)
        
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code']=="NoSuchKey":
            return {
                'statusCode': 403,
                'body': "la start list non è presente nel cloud"
            }
        else: 
            return {
                'statusCode': 400,
                'body': "errore non specificato"
            }
                        
    
    risultato  = xmldoc.getElementsByTagName("PersonStart")
    y = '{ "griglia_di_partenza": ['
    for k in range(len(risultato)):
        nome = str(risultato[k].getElementsByTagName("Given")[0].firstChild.data)
        nome = re.sub('[\']', '', nome)
        cognome = str(risultato[k].getElementsByTagName("Family")[0].firstChild.data)
        cognome = re.sub('[\']', '', cognome)
        organizzazione = str(risultato[k].getElementsByTagName("Organisation")[0].getElementsByTagName("Name")[0].firstChild.data)
        tempo = str(risultato[k].getElementsByTagName("StartTime")[0].firstChild.data)
        tempo = tempo.split("+")
        tempo =  tempo[0]
        
        atleta = {
                "nome": nome,
                "cognome": cognome,
                "organizzazione" : organizzazione,
                "tempo" : tempo
                
            }
        y = y + str(atleta) + ","
    
    y = y + "]}"
    
    y = re.sub('[\']', '\"', y)
    y = y.rsplit(',', 1)
    y = y[0] + y[1]
    return {
        'statusCode': 200,
        'body': y 
    }
