import smtplib
import json,boto3
from random import randint
counter = 0

def lambda_handler(event, context):
    global counter
    uniquecode = uniquecodegen()
    nome_gara = event["queryStringParameters"]["race_name"]
    date = event["queryStringParameters"]["race_date"]
    email = event["queryStringParameters"]["email"]
    date = date.split("/")
    id = nome_gara[0]+nome_gara[1] + nome_gara[2]+ date[1]+date[2]
    token = nome_gara+'_'+uniquecode
    sess= boto3.Session(region_name='us-east-1')
    ddb= sess.client('dynamodb')
    table = 'TokenTable'
    item = {
          "race_id": {
                "S": id
          },
          "raceDate": {
                "S": str(date)
          },
          "email": {
                "S": email
          },
          "raceName": {
                "S": nome_gara
          },
          "SecretToken": {
                "S": token
          },
    }
    try:
        ddb.get_item(TableName=table, Key={
            "race_id" : {
                "S" : id
            }
        },
        )
        id = id + str(counter)
        counter = counter + 1
    except KeyError:
        print("race id non in conflitto")
    ddb.put_item(TableName=table, Item=item)
    item = {
        "race_id" : id,
        "secret_token" : token
    }
    
    sender = "orienteering.infopoint@gmail.com"
    receiver = email
    password = "pass_tg5"
    subject = "Subject: Credenziali accesso gara\n\n"
    body = "Ecco le sue credenziali: \n\n" + str(item) +"\n\n" + "Grazie e arrivederci"
    message = subject + body
    host = "smtp.gmail.com"
    server = smtplib.SMTP(host, 587)
    print("ciao")
    server.ehlo()
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,receiver, message)
    
    return {
        
        'statusCode': 200,
        'body':json.dumps(item)
    }
def uniquecodegen():
    code = ""
    for x in range(5):
        a = randint(0,9) 
        code = code + str(a)
    return code
