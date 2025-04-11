

import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)
redis_conn = None

def initialize_redis():
    global redis_conn
    if redis_conn is None:
        try:
            logger.info("Attempting to connect to Redis via AppConfig...")
            conn = get_redis_connection("default")
            conn.ping() # التحقق من الاتصال
            redis_conn = conn # قم بتعيين المتغير العام فقط عند النجاح
            logger.info("Successfully connected to Redis via AppConfig.")
        except Exception as e:
            logger.error(f"Could not connect to Redis via AppConfig: {e}")
            redis_conn = None
    return redis_conn 