import json
import boto3
from botocore.exceptions import ClientError

# AWS SES Client
ses_client = boto3.client('ses', region_name='eu-central-1')  # Bölgenizi ayarlayın

def lambda_handler(event, context):
    try:
        # API Gateway'den gelen sorgu parametresinden 'email' değerini alın
        email = event['queryStringParameters'].get('email')

        # Eğer email parametresi yoksa hata döndür
        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'E-posta adresi belirtilmedi.'})
            }

        # E-posta adresini doğrulamak için SES VerifyEmailIdentity çağrısı
        response = ses_client.verify_email_identity(
            EmailAddress=email
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"E-posta adresi doğrulama sürecine alındı: {email}"})
        }

    except ClientError as e:
        # AWS SES hatalarını yakala ve döndür
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        # Diğer hataları yakala
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
