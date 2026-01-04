import json
import pika
from datetime import datetime

QUEUE_NAME = "excel_exports"


def send_export_job():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            credentials=pika.PlainCredentials("guest", "guest"),
            heartbeat=0,
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    message = {
        "export_type": "users",
        "file_name": f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print("Export job sent:", message["file_name"])
    connection.close()


if __name__ == "__main__":
    send_export_job()
