import logging
import boto3
import pymysql

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS SES and RDS configuration
RDS_HOST = "kanbagisdb.clwamwmci9vk.eu-central-1.rds.amazonaws.com"
RDS_USER = "admin"
RDS_PASSWORD = "sdsd"
RDS_DATABASE = "kanbagisdb"
RDS_PORT = 63306  # Correct MySQL default port is 3306, not 63306

# SES client
ses_client = boto3.client('ses', region_name="eu-central-1")

def send_email(recipient_email):
    """
    Sends an email using AWS SES.
    """
    subject = "Kan Bağışı İlanı Hakkında"
    body = """
    Maksimum bağışçı arama sayısına ulaştık. Maalesef aradığınız kanı bulamadık.
    """
    response = ses_client.send_email(
        Source='kanproje@sdsd.com.tr',  # Replace with verified email
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response

def lambda_handler(event, context):
    """
    Lambda function entry point.
    """
    try:
        # Establish RDS connection
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DATABASE,
            port=RDS_PORT
        )
        cursor = connection.cursor()

        # Query to find announcements with email_service = 4
        select_query = """
            SELECT bdp.id AS publication_id, 
                   u.email, u.name
            FROM Blood_Donation_Publication bdp
            JOIN User u ON bdp.user_id = u.id
            WHERE bdp.email_service = 4;
        """
        cursor.execute(select_query)
        results = cursor.fetchall()

        for record in results:
            publication_id, email, name = record

            # Send email
            send_email(email)
            logger.info(f"Email sent to: {email}")

            # Update announcement status
            update_query = """
                UPDATE Blood_Donation_Publication
                SET email_service = 5
                WHERE id = %s;
            """
            cursor.execute(update_query, (publication_id,))

        # Commit changes
        connection.commit()

    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Close the database connection
        if connection:
            connection.close()
