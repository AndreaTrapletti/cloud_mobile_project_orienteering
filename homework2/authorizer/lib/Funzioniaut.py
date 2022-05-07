import boto3
class util: 
    def DBchecker(self, token) : 
        sess= boto3.Session(region_name='us-east-1')
        ddb= sess.client('dynamodb')
        id = token.split("-")[0]
        token = token.split("-")[1]
        try:
            table = 'TokenTable' 
             #bisognerà probabilemnte inserire un try catch
            data = ddb.get_item(TableName=table,
            Key={
            'race_id': {
              'S': id
                    }
                },
                )["Item"]["SecretToken"]["S"]
        except KeyError:
            return False 

        if data == token:
            return True 
        else: 
            return False
