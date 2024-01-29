import boto3
import json

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
dynamodbTableName = 'empleados_2k'
empleado = dynamodb.Table(dynamodbTableName)


def lambda_handler(event, context):
    print(event)

    # Entrada (json)
    print(event)  # Revisar en CloudWatch
    Empleados_json = json.loads(event['Records'][0]['Sns']['Message'])
    tenant_id = Empleados_json['tenant_id']
    bucket = Empleados_json['bucket']
    firstname = Empleados_json['firstname']
    lastName = Empleados_json['lastname']
    key = Empleados_json['key']

    try:
        response = clave_unica(bucket, key)
        print(response)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            #    name = key.split('_')
            #    extension = name[-1].split('.')
            #    firstname = name[0]
            #    lastName = name[1]
            #    tenant_id = extension[0]
            print(faceId)
            print(firstname)
            print(lastName)
            print(tenant_id)
            Registrar_empleado(faceId, firstname, lastName, tenant_id)

    except Exception as e:
        print(e)
        print(
            "Hubo un error al procesar la imagen del empleado {} desde el bucket  {}. " + key + "en el bucket :" + bucket)
        raise e


def clave_unica(bucket, key):
    response = rekognition.index_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }

        },
        CollectionId='empleados'
    )
    return response


def Registrar_empleado(faceId, firstname, lastName, tenant_id):
    empleado.put_item(
        Item={
            'tenant_id': tenant_id,
            'faceId': faceId,
            'firstname': firstname,
            'lastname': lastName
        }
    )
