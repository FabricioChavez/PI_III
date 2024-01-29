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
    object_name = event['queryStringParameters']['objectKey']

    image_bytes = s3.get_object(Bucket=bucketName, Key=object_name)['Body'].read()
    response = rekognition.search_faces_by_image(
        CollectionId='empleados',
        Image={'Bytes': image_bytes})
    # extraer el tenant_id
    container = object_name.split('_')

    EntranceMode = container[1]

    tenant_id = container[-1].split('.')[0]

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
            print('PERSONA ENCONTRADA', face['Item'])
            return buildResponse(200, {
                'Message': "EXITO",
                'firstname': face['Item']['firstname'],
                'lastname': face['Item']['lastname']
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


