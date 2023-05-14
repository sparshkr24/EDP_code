import boto3
import io
from PIL import Image

def face_rec(image_inp):
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    # print(rekognition, "\n", dynamodb)

    image_path = image_inp

    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()

    try:
        response = rekognition.search_faces_by_image(
                CollectionId='edpfaces',
                Image={'Bytes':image_binary}                                       
                )
    except Exception as e:
        return False

    found = False
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])
            
        face = dynamodb.get_item(
            TableName='facerecognition',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face:
            print ("Found Person: ",face['Item']['FullName']['S'])
            found = True

    return found

