import sys
import os
from unittest import result
import pika
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.ingestion_service import ingest_events

from pythonjsonlogger import jsonlogger

logger = logging.getLogger("event_consumer")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "store_events"
BATCH_SIZE = 500

class EventConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
        self.channel.basic_qos(prefetch_count=BATCH_SIZE)
        self.batch = []
        self.delivery_tags = []

    def process_message(self, method, body):
        try:
            event = json.loads(body)
            self.batch.append(event)
            self.delivery_tags.append(method.delivery_tag)

            if len(self.batch) >= BATCH_SIZE:
                self.process_batch()
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def process_batch(self):
        if not self.batch:
            return

        try:
            logger.info(f"Ingesting batch of {len(self.batch)} events...")
            result = ingest_events(self.batch)
            logger.info(f"Ingestion result: {result}")

            if result.get(
                "accepted",
                0
            ) == 0:

                logger.error(
                    "No events accepted!"
                )
            
            # Ack all successfully processed messages
            for tag in self.delivery_tags:
                self.channel.basic_ack(delivery_tag=tag)
        except Exception as e:
            logger.exception("Failed to ingest batch")
            # Nack all messages in the batch so they get requeued
            for tag in self.delivery_tags:
                self.channel.basic_nack(delivery_tag=tag, requeue=True)
                
        self.batch.clear()
        self.delivery_tags.clear()

    def start_consuming(self):
        logger.info(f"Starting consumer on {QUEUE_NAME} at {RABBITMQ_HOST}...")
        try:
            for method, properties, body in self.channel.consume(queue=QUEUE_NAME, inactivity_timeout=2):
                if body is None:
                    # Timeout reached, flush the batch
                    self.process_batch()
                else:
                    self.process_message(method, body)
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.process_batch() # flush any remaining
            self.channel.cancel()
        finally:
            self.connection.close()

if __name__ == "__main__":
    consumer = EventConsumer()
    consumer.start_consuming()
