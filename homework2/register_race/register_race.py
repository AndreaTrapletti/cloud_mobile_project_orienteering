import json,boto3
from random import randint
correttore = 0

def lambda_handler(event, context):
    global correttore
    sess= boto3.Session(region_name='us-east-1')
    ddb= sess.client('dynamodb')
    table = 'TokenTable'
    nome_gara = event["queryStringParameters"]["race_name"]
    date = event["queryStringParameters"]["race_date"]
    email = event["queryStringParameters"]["email"]
    date = date.split("/")
    uniquecode = uniquecodegen()
    token = nome_gara+'_'+uniquecode
    id = nome_gara[0]+nome_gara[1] + nome_gara[2]+ date[1]+date[2]
    try:
        ddb.get_item(TableName=table, Key={
                'race_id': {
                  'S': id
                        }
                    },
                    )
        id = id+str(correttore)
        correttore = correttore+1
    except KeyError :
        print("race id non in conflitto")
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

    ddb.put_item(TableName=table, Item=item)
    item = {
        "race_id" : id,
        "secret_token" : token
    }
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
