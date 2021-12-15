export RABBITMQ_DEFAULT_USER = []
export RABBITMQ_DEFAULT_PASS = []
export RABBITMQ_HOST = []

export DB_HOST = []
export DB_USER = []
export DB_PASS = []
export DB_NAME = []

celery -A predict_worker.app worker
