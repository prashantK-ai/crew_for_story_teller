import os
from os.path import join, dirname
from dotenv import load_dotenv
from cfenv import AppEnv
import json
import logging

logger = logging.getLogger(__name__)

class AppConfig:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.print_env()
        logger.info("ENV: %s", os.getenv("ENV", "PROD").upper())
        self.LOCAL_ENV = os.getenv("ENV", "LOCAL").upper() == "LOCAL"

        if self.LOCAL_ENV:
            self.load_local_env()
        else:
            self.load_production_env()

    def load_local_env(self) -> None:
        """Load local environment variables."""
        self.DB_CONN_URL = os.getenv("DB_CONN_URL")
        self.SAP_PROVIDER_URL = os.getenv("SAP_PROVIDER_URL")
        self.SAP_CLIENT_ID = os.getenv("SAP_CLIENT_ID")
        self.SAP_CLIENT_SECRET = os.getenv("SAP_CLIENT_SECRET")
        self.SAP_ENDPOINT_URL_GPT35 = os.getenv("SAP_ENDPOINT_URL_GPT35")
        self.SAP_ENDPOINT_URL_GPT4 = os.getenv("SAP_ENDPOINT_URL_GPT4")
        self.SAP_ENDPOINT_URL_GPT4O = os.getenv("SAP_ENDPOINT_URL_GPT4O")

        self.SAP_EMBEDDING_ENDPOINT_URL = os.getenv("SAP_EMBEDDING_ENDPOINT_URL")
        self.SAP_GPT35_MODEL = os.getenv("SAP_GPT35_MODEL")
        self.SAP_GPT4_MODEL = os.getenv("SAP_GPT4_MODEL")
        self.SAP_GPT4O_MODEL = os.getenv("SAP_GPT4O_MODEL")

        self.SAP_ADA_MODEL = os.getenv("SAP_ADA_MODEL")
        self.SAP_GPT35_MAX_TOKENS = os.getenv("SAP_GPT35_MAX_TOKENS")
        self.SAP_API_VERSION = "2023-05-15"
        self.LEEWAY = 100
        self.CHAT_PROMPT_TEMPLATE = os.getenv('CHAT_PROMPT_TEMPLATE')

    def load_production_env(self) -> None:
        """Load production environment variables."""
        env = AppEnv()

        self.FRONTEND_AUTH_SECRET = os.getenv('FRONTEND_AUTH_SECRET')
        postgresql = env.get_service(name='postgresql')
        self.DB_USER = postgresql.credentials["username"]
        self.DB_PWD = postgresql.credentials["password"]
        self.DB_URL = postgresql.credentials["hostname"]
        self.DB_PORT = postgresql.credentials["port"]
        self.DB_NAME = postgresql.credentials["dbname"]
        self.DB_CONN_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_URL}:{self.DB_PORT}/{self.DB_NAME}"

        genai = env.get_service(name='aicore')
        self.SAP_PROVIDER_URL = f"{genai.credentials['url']}/oauth/token"
        self.SAP_CLIENT_ID = genai.credentials["clientid"]
        self.SAP_CLIENT_SECRET = genai.credentials["clientsecret"]
        self.SAP_ENDPOINT_URL_GPT35 = f"{genai.credentials['serviceurls']['AI_API_URL']}/v2/inference/deployments/{os.getenv('AZURE_DEPLOYMENT_ID')}/chat/completions?api-version={os.getenv('API_VERSION')}"
        self.SAP_GPT35_MODEL = os.getenv("SAP_GPT35_MODEL")
        self.SAP_GPT4_MODEL = os.getenv("SAP_GPT4_MODEL")
        self.SAP_GPT35_MAX_TOKENS = os.getenv("SAP_GPT35_MAX_TOKENS")
        self.CHAT_PROMPT_TEMPLATE = os.getenv('CHAT_PROMPT_TEMPLATE')
        self.LEEWAY = 100
        self.SAP_API_VERSION = os.getenv('API_VERSION')
        self.SAP_EMBEDDING_ENDPOINT_URL = f"{genai.credentials['serviceurls']['AI_API_URL']}/v2/inference/deployments/d4d75b978bd654bd/embeddings?api-version={os.getenv('API_VERSION')}"

    def to_json(self) -> str:
        """Convert configuration to JSON string."""
        data = self.__dict__.copy()
        return json.dumps(data, indent=4)

    def print_env(self) -> None:
        """Print environment variables for debugging purposes."""
        for key, value in os.environ.items():
            logger.debug(f"{key}={value}")
