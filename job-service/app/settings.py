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

    fastapi_port: str = "8000"
    fastapi_host: str = "localhost"
    


settings = Settings()