import boto3
import pymysql

# RDS bağlantı bilgileri
RDS_HOST = "kanbagisdb.clwamwmci9vk.eu-central-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "sdsd"
RDS_DATABASE = "kanbagisdb"
RDS_PORT = 63306

# AWS SES ayarları
AWS_REGION = 'eu-central-1'
SES_SENDER = 'kanproje@sdsds.com.tr'  # SES'te doğrulanmış e-posta adresi

# SES Client
ses_client = boto3.client('ses', region_name=AWS_REGION)

def lambda_handler(event, context):
    # API'den gelen user_id parametresini al
    user_id = event.get('queryStringParameters', {}).get('user_id')

    if not user_id:
        return {"statusCode": 400, "body": "user_id parameter is missing."}

    try:
        user_id = int(user_id)  # user_id'yi integer olarak kontrol et
    except ValueError:
        return {"statusCode": 400, "body": "Invalid user_id. It must be an integer."}

    # RDS'ye bağlan
    try:
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE,
            port=RDS_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        return {"statusCode": 500, "body": f"Database connection failed: {e}"}

    try:
        with conn.cursor() as cursor:
            # user_id'ye ait location ve blood_type_id bilgilerini al
            user_query = """
            SELECT location, blood_type_id 
            FROM Blood_Donation_Publication 
            WHERE user_id = %s AND email_service < 1
            """
            cursor.execute(user_query, (user_id,))
            user_info = cursor.fetchone()

            if not user_info:
                return {"statusCode": 404, "body": "User not found for the given user_id."}

            location = user_info['location']
            blood_type_id = user_info['blood_type_id']

            # location ve blood_type_id eşleşen diğer kullanıcıları al
            matching_users_query = """
            SELECT email, name 
            FROM User 
            WHERE location = %s AND blood_type_id = %s AND id != %s
            """
            cursor.execute(matching_users_query, (location, blood_type_id, user_id))
            matching_users = cursor.fetchall()

            if not matching_users:
                return {"statusCode": 200, "body": "No matching users found for the specified user_id."}

            # Her eşleşen kullanıcıya e-posta gönder
            for user in matching_users:
                send_email(user['email'], user['name'], location)

        return {"statusCode": 200, "body": "Emails sent successfully to matching users."}
    except Exception as e:
        return {"statusCode": 500, "body": f"Query execution failed: {e}"}
    finally:
        conn.close()


def send_email(to_email, user_name, location):
    subject = "Kan Bağışı Eşleşmesi Bulundu"
    body = (
        f"Merhaba {user_name},\n\n"
        f"Bölgende senin ile eşleşen kan bağış ihtiyacı olan biri var: {location}. "
        "Lütfen hesabını kontrol et ve bir hayat kurtar! \n\n"
        "En iyi dileklerimiz ile,\n Kan Bağış Ekibi"
    )

    try:
        # SES üzerinden e-posta gönder
        response = ses_client.send_email(
            Source=SES_SENDER,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': body,
                    }
                }
            }
        )
        print(f"Email sent to {to_email}. Response: {response}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
