import uuid
import json
import boto3
from datetime import date
from xml.dom import minidom
nomiGare=["roma","napoli"]
contGare=[1,2]
bucket_name= "xmlverdi" #controllare nome 

class func: 
    def pulizia(self, contenuto):
        x =-1
        y =-1
        for i in range(len(contenuto)):
            if contenuto[i]=="<":
                x=i
                break
        for i in range(len(contenuto)):
            if contenuto[i] == ">":
                y = i
        contenuto = contenuto[x:y+1]
        return contenuto
    
    def get_nome(self,xml):
        nome =xml.getElementsByTagName("Name")
        return nome[0].firstChild.data     
    
    def get_numb(self,nome):
        global nomiGare,contGare
        if nome in nomiGare:
            for x in range(len(nomiGare)):
                if nomiGare[x]==nome :
                    contGare[x] = contGare[x]+1
                    return contGare[x]
        else:
            nomiGare.append(nome)
            contGare.append(1)
            print (contGare)
            return 1
            
    def caricamentoDB (self,content):
        
        global bucket_name
        xmldoc = minidom.parseString(content)
        nome = self.get_nome(xmldoc)
        gare=  xmldoc.getElementsByTagName('ClassResult')
        sess= boto3.Session(region_name='us-east-1')
        ddb= sess.client('dynamodb')
        table = 'GareOrienteering' 
        for i in gare:
            nome_gara= nome + str(self.get_numb(nome))
            file_name = nome_gara + ".xml"
            s3 = boto3.resource("s3")
            s3.Bucket(bucket_name).put_object(Key=file_name, Body = i.toxml())
                    
            item = {
                "idGara": {
                    "S": nome_gara
                    },
                "data": {
                    "S": str(date.today())
                    },
                "nome_file": {
                    "S": file_name
                    }
            } 
            ddb.put_item(TableName=table, Item=item)