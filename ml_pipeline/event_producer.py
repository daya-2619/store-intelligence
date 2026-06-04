import pika
import json
import logging
import sqlite3
import os

logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "store_events"
SPOOL_DB = os.getenv("SPOOL_DB", "spooler.db")

class EventProducer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._init_spool()
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
            self.flush_spool()
        except Exception as e:
            logger.warning(f"Could not connect to RabbitMQ, events will be spooled: {e}")

    def _init_spool(self):
        with sqlite3.connect(SPOOL_DB) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS spooled_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payload TEXT
                )
            ''')
            conn.commit()

    def spool_events(self, events: list):
        with sqlite3.connect(SPOOL_DB) as conn:
            for event in events:
                conn.execute("INSERT INTO spooled_events (payload) VALUES (?)", (json.dumps(event),))
            conn.commit()

    def flush_spool(self):
        if not self.channel:
            return
        
        with sqlite3.connect(SPOOL_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, payload FROM spooled_events")
            rows = cursor.fetchall()
            
            for row_id, payload in rows:
                try:
                    self.channel.basic_publish(
                        exchange='',
                        routing_key=QUEUE_NAME,
                        body=payload,
                        properties=pika.BasicProperties(delivery_mode=2)
                    )
                    cursor.execute("DELETE FROM spooled_events WHERE id = ?", (row_id,))
                except Exception as e:
                    logger.error(f"Failed to flush spooled event: {e}")
                    break
            conn.commit()

    def publish_events(self, events: list):
        if not events:
            return
            
        if not self.channel:
            self.spool_events(events)
            return

        try:
            for event in events:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=json.dumps(event),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    )
                )
        except Exception as e:
            logger.error(f"Failed to publish to RabbitMQ, spooling events: {e}")
            self.spool_events(events)

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

def push_events_to_queue(events: list):
    try:
        p = EventProducer()
        p.publish_events(events)
        p.close()
        return True
    except Exception as e:
        logger.error(f"Failed in push_events_to_queue: {e}")
        return False
