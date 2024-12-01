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
SES_SENDER = 'kanproje@sdsd.com.tr'  # Verified sender email address in SES

# SES Client
ses_client = boto3.client('ses', region_name=AWS_REGION)

def lambda_handler(event, context):
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
            # İlan ve eşleşme bilgilerini getir
            query = """
            SELECT bdp.id AS publication_id, bdp.location, bdp.blood_type_id, bdp.email_service,
                   u.email, u.name
            FROM Blood_Donation_Publication bdp
            LEFT JOIN User u ON bdp.location = u.location 
            AND bdp.blood_type_id = u.blood_type_id
            AND bdp.user_id != u.id
            AND bdp.location = u.location 
            WHERE bdp.email_service < 4
            """
            cursor.execute(query)
            publications = cursor.fetchall()
            
            if not publications:
                return {"statusCode": 200, "body": "No publications found."}
            
            # Her ilan için işlem yap
            for pub in publications:
                publication_id = pub['publication_id']
                email_service = pub['email_service']
                new_email_service = email_service + 1

                # `email_service` değerini artır
                update_query = """
                UPDATE Blood_Donation_Publication
                SET email_service = %s
                WHERE id = %s 
                """
                cursor.execute(update_query, (new_email_service, publication_id))

                # E-posta gönderme koşulu
                if pub['email']:
                    send_email(pub['email'], pub['name'], pub['location'])

            conn.commit()
        return {"statusCode": 200, "body": "Process completed successfully."}
    except Exception as e:
        return {"statusCode": 500, "body": f"Query execution failed: {e}"}
    finally:
        conn.close()

def send_email(to_email, user_name, location):
    subject = "Kan Bağışı Eşleşmesi Bulundu!"
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
