from celery.messaging import establish_connection, get_consumer_set
from celery.worker.job import TaskWrapper
from celery.worker import process_initializer
from celery.worker.pool import TaskPool

"""
This code was from Ask in #celery at freenode.
"""

def process_n_messages(n=1):

    def callback(message, message_data):
        task = TaskWrapper.from_message(message, message_data)
        task.execute()

    conn = establish_connection()
    consumer = get_consumer_set(conn)
    consumer.register_callback(callback)
    it = consumer.iterconsume(limit=n)

    for message in it:
        pass

    consumer.close()
    connection.close()


def process_n_messages_pool(n=10):

    p = TaskPool(n, process_initializer)
    p.start()

    def callback(message, message_data):
        task = TaskWrapper.from_message(message, message_data)
        task.execute_using_pool(pool)

    conn = establish_connection()
    consumer = get_consumer_set(conn)
    consumer.register_callback(callback)
    it = consumer.iterconsume(limit=n)

    try:
        for message in it:
            pass
    finally:
        consumer.close()
        conn.close()
        p.stop()

