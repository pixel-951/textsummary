from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    summarizer: model type, max length 
    notifier: address (port)
    queuehandler: address (name), queue name
    """
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    queue_name: str = "jobs"
    
    notification_url: str = "http://localhost:8001/api/notification"

    model_name: str = "facebook/bart-large-cnn"
    summary_max_length: int = 130
    summary_min_length: int = 30


