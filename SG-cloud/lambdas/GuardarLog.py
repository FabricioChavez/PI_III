import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
dynamodbTableName = 'empleados_2k'
empleado = dynamodb.Table(dynamodbTableName)
bucketName = 'visitantes-temporales'
logTable = dynamodb.Table('EntryExitMonitorLog_f')


def lambda_handler(event, context):
    print("COSAS DE EVENTO :\n")
    print(event)
    #   object_name = event['queryStringParameters']['objectKey']

    # Entrada (json)
    body = json.loads(event['Records'][0]['body'])
    Log_mensaje = json.loads(body['Message'])

    tenant_id = Log_mensaje['tenant_id']
    EntranceMode = Log_mensaje['EntranceMode']
    bucketName = Log_mensaje['bucket']
    object_name = Log_mensaje['key']

    image_bytes = s3.get_object(Bucket=bucketName, Key=object_name)['Body'].read()
    response = rekognition.search_faces_by_image(
        CollectionId='empleados',
        Image={'Bytes': image_bytes})

    print(tenant_id + ' ' + EntranceMode)

    print("COSAS DE CARAS :\n")
    print(response)

    for match in response['FaceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])

        face = empleado.get_item(
            Key={
                'tenant_id': tenant_id,
                'faceId': match['Face']['FaceId']
            }
        )

        if 'Item' in face:
            # Registro de log con fecha y hora
            log_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()

            logTable.put_item(
                Item={
                    'tenant_id': tenant_id,
                    'log_id': log_id,  # UUID como clave primaria
                    'faceId': match['Face']['FaceId'],
                    'firstname': face['Item']['firstname'],
                    'lastname': face['Item']['lastname'],
                    'timestamp': timestamp,
                    'event': EntranceMode
                }
            )

            print('PERSONA ENCONTRADA', face['Item'])
            return buildResponse(200, {
                'Message': "EXITO",
            }
                                 )
    print('NO SE RECONOCE A ESTA PERSONA')
    return buildResponse(403, {'Message': 'No se encontro a la persona'})


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response

