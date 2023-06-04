import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    SENDGRID_API_KEY = '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'

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    conn = psycopg2.connect(host="techconf37.postgres.database.azure.com", user="quyetnt7@techconf37", password="A123456@", database="techconfdb")
    try:
        cur = conn.cursor()
        sendGrid = SendGridAPIClient(SENDGRID_API_KEY)

        # TODO: Get notification message and subject from database using the notification_id
        cur.execute("SELECT message,subject FROM notification WHERE id=%s;",(notification_id,))
        messagePlain, subject = cur.fetchone()

        # TODO: Get attendees email and name
        cur.execute("SELECT email,first_name FROM attendee;")
        attendees = cur.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        for item in attendees:
            message = Mail(
                from_email='ntrongquyet73@gmail.com',
                to_emails=item[0],
                subject='{}: {}'.format(item[1], subject),
                html_content=messagePlain
            ) 

            res = sendGrid.send(message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        status = "Notified {} attendees".format(len(attendees))
        cur.execute("Update notification set status = '{}', completed_date = '{}' where id = {}".format(status, datetime.utcnow(), notification_id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection
        cur.close()
        conn.close()