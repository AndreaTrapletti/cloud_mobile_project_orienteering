import json
import boto3,botocore.exceptions
from datetime import datetime
from xml.dom import minidom
bucket_name="garetgv"
table = 'GareOrienteering' 

class function: 
    def getcat(self, classres):
        categoria = classres.getElementsByTagName('Name')
        return categoria[0].firstChild.data
            
    def caricamentobuck (self,content,idgara):
        
        global bucket_name,table
        xmldoc = minidom.parseString(content)
        gare=  xmldoc.getElementsByTagName('ClassResult')
        
        for i in gare:
            a = True    
            file_name = idgara+ self.getcat(i)+ ".xml"
            s3 = boto3.resource("s3")
            try:
                s3_client = boto3.client("s3")
                s3_client.get_object(Bucket=bucket_name, Key=file_name)
                
            except botocore.exceptions.ClientError as error:
                a = False
                if error.response['Error']['Code']=="NoSuchKey":
                    self.caricamentoDB(idgara, self.getcat(i), file_name) 
                    s3.Bucket(bucket_name).put_object(Key=file_name, Body = i.toxml())
                else: 
                     return {
                        'statusCode': 400,
                        'body': "errore non specificato"
                        }
            if a == True : 
                s3_client.delete_object(Bucket=bucket_name, Key=file_name)
                s3.Bucket(bucket_name).put_object(Key=file_name, Body = i.toxml())
            
        
    def caricamentoDB(self,race_id,categoria,file_name) : 
        global table
        sess= boto3.Session(region_name='us-east-1')
        ddb= sess.client('dynamodb')
        item = {
                    "race_id": {
                        "S": race_id
                        },
                    "oraCaricamento":{
                      "S": datetime.now().time().strftime('%H:%M:%S')
                    },
                    "Categoria": {
                        "S": categoria
                        },    
                    "nome_file": {
                        "S": file_name
                        }
                } 
        ddb.put_item(TableName=table, Item=item)
