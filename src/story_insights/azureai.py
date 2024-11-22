import logging
from datetime import datetime
from langchain_openai import AzureChatOpenAI
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from appconfig import AppConfig
from langchain_openai import AzureOpenAIEmbeddings

logger = logging.getLogger(__name__)

class AzureAI:
    def __init__(self, config: AppConfig):
        self.config = config
        self._token = None
        self._token_expires_at = 0
        self._oauth2_session = self.create_oauth2_session()

    def create_oauth2_session(self) -> OAuth2Session:
        """Create an OAuth2 session."""
        client = BackendApplicationClient(client_id=self.config.SAP_CLIENT_ID)
        return OAuth2Session(client=client)

    def get_token(self) -> str:
        """Get an OAuth2 token."""
        if self._token and self._token_expires_at + self.config.LEEWAY > datetime.now().timestamp():
            return self._token
        logger.info(f"Creating a new token for {self.config.SAP_PROVIDER_URL}")
        token = self._oauth2_session.fetch_token(
            token_url=self.config.SAP_PROVIDER_URL,
            client_secret=self.config.SAP_CLIENT_SECRET,
        )
        self._token = token["access_token"]
        self._token_expires_at = token["expires_at"]
        return self._token

    def get_embedding_client(self) -> AzureOpenAIEmbeddings:
        """Get an Azure OpenAI Embeddings client."""
        token = self.get_token()
        embedding_client = AzureOpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_version=self.config.SAP_API_VERSION,
            api_key=token,
            azure_endpoint=self.config.SAP_EMBEDDING_ENDPOINT_URL,
            default_headers={"AI-Resource-Group": "default"}
        )
        return embedding_client

    def get_client(self) -> AzureChatOpenAI:
        """Get an Azure Chat OpenAI client."""
        token = self.get_token()
        client = AzureChatOpenAI(
            api_version=self.config.SAP_API_VERSION,
            api_key=token,
            azure_deployment="gpt-4o",
            azure_endpoint=self.config.SAP_ENDPOINT_URL_GPT4O,
            default_headers={"AI-Resource-Group": "default"}
        )
        return client
