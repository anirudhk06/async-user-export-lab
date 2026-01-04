import json
import pika
from pathlib import Path

from app.export_service import export_users_to_excel

QUEUE_NAME = "excel_exports"
EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def callback(ch, method, properties, body) -> None:
    message = json.loads(body)
    print("Received job:", message)

    file_path = EXPORT_DIR / message["file_name"]

    try:
        export_users_to_excel(str(file_path))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Job completed")

    except Exception as e:
        print("Job failed:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_worker() -> None:
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
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("Worker waiting for export jobs...")
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
