from dotenv import load_dotenv
import os

load_dotenv()
class Settings:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
    QDRANT_URL =  os.getenv('QDRANT_URL')
    RETRIVAL_CHUNKS = int(os.getenv("RETRIVAL_CHUNKS"))
    TEXT_FOLDER_PATH = os.getenv('TEXT_FOLDER_PATH')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    SPARSE_MODEL = os.getenv("SPARSE_MODEL")
    BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
    CROSS_ENCDER_MODEL = os.getenv("CROSS_ENCDER_MODEL")
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP'))
    EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL')
    PROCESSED_FILES = os.getenv('PROCESSED_FILES', './processed_files.txt')
    SQL_SERVER_HOST = os.getenv("SQL_SERVER_HOST")
    SQL_SERVER_DATABASE = os.getenv("SQL_SERVER_DATABASE")
    SQL_SERVER_USERNAME = os.getenv("SQL_SERVER_USERNAME")
    SQL_SERVER_PASSWORD =os.getenv("SQL_SERVER_PASSWORD")
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    TOKEN_EXPIRE_IN_DAYS = os.getenv('TOKEN_EXPIRE_IN_DAYS')
    

settings = Settings()