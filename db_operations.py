import os
from venv import logger
from dotenv import load_dotenv
import pyodbc
from datetime import datetime
from uuid import uuid4
from settings import settings

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
        
    def connect(self):  # Ensure correct indentation level for connect method
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={settings.SQL_SERVER_HOST};"
                f"DATABASE={settings.SQL_SERVER_DATABASE};"
                f"UID={settings.SQL_SERVER_USERNAME};"
                f"PWD={settings.SQL_SERVER_PASSWORD};"
            )
            
            if self.connection:
                logger.info("Connected to SQL Server database.")
        except Exception as e:
            logger.error(f"Error connecting to SQL Server database: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logger.info("SQL Server connection closed")

    def create_user(self, first_name, last_name, username, email, hashed_password):
        try:
            user_id = str(uuid4())
            cursor = self.connection.cursor()
            sql = """
                INSERT INTO users (user_id, first_name, last_name, username, email, password, created_at,  modified_by, modified_on)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (user_id, first_name, last_name, username, email, hashed_password, datetime.now(),  None, None)
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False

    def check_user(self, userid):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT Email FROM users WHERE UserId = ?"""
            cursor.execute(sql, userid)
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None

    def save_chat_history(self, user_id, query, response, email):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO chat_history (user_id, query, response, timestamp, email)
                     VALUES (?, ?, ?, ?, ?)"""
            timestamp = datetime.now()
            values = (user_id, query, response, timestamp, email)
            logger.info(f"Saving chat history: user_id={user_id}, query={query}, response={response[:50]}...")
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            logger.info("Chat history saved successfully")
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
            raise

    def get_chat_history(self, user_id):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT id, query, response, timestamp, email FROM chat_history
                     WHERE user_id = ? ORDER BY timestamp DESC""" 
            cursor.execute(sql, (user_id,))
            history = cursor.fetchall()
            cursor.close()
            result = []
            for row in history:
                result.append({
                    'id': row.id,
                    'query': row.query,
                    'email' : row.email,
                    'response': row.response,
                    'timestamp': str(row.timestamp) 
                })
            return result
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []

    def update_faq_count(self, query,response,user_id,email):
        try:
            cursor = self.connection.cursor()
            # Check if the query exists first
            cursor.execute("SELECT count FROM faq_counts WHERE query = ? and user_id = ?", (query,user_id))
            result = cursor.fetchone()
            if result:
                # If query exists, update the count
                cursor.execute("UPDATE faq_counts SET count = count + 1, response = ?, timestamp = ?, email = ?  WHERE query = ? and user_id = ?", (response, datetime.now(), email, query, user_id))
            else:
                # If query does not exist, insert a new record
                timestamp = datetime.now() 
                cursor.execute("INSERT INTO faq_counts (query, response, timestamp, user_id, email, count) VALUES (?,?,?,?,?,1)", (query,response,timestamp,user_id,email))
            self.connection.commit()
            cursor.close()
            logger.info("FAQ count updated successfully")
        except Exception as e:
            logger.error(f"Error updating FAQ count: {e}")
            raise

    def get_top_faqs(self,user_id):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT id,query,response,timestamp,email,count FROM faq_counts Where user_id = ?
                     ORDER BY timestamp DESC """
            cursor.execute(sql,(user_id,))
            top_faqs = cursor.fetchall()
            cursor.close()
            # return top_faqs
            result = []
            for row in top_faqs:
                result.append({
                    'id': row.id,
                    'query': row.query,
                    'count': row.count,
                    'email' : row.email,
                    'response': row.response,
                    'timestamp': str(row.timestamp)
                })
            return result
        except Exception as e:
            logger.error(f"Error retrieving top FAQs: {e}")
            return []
        
    def get_userprofile_list(self):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT * from userprofilelist"""
            cursor.execute(sql)
            top_faqs = cursor.fetchall()
            cursor.close()
            result = []
            for row in top_faqs:
                result.append({
                    'id': row.id,
                    'user_id': row.user_id,
                    'user_name': row.user_name,
                    'user_email': row.user_email,
                    'first_name': row.first_name,
                    'last_name' : row.last_name,
                    'modifiedon': row.modifiedon,
                    'createdon': row.createdon,
                    'modifiedby': row.modifiedby
                })
            return result
        except Exception as e:
            logger.error(f"Error retrieving users profile list: {e}")
            return []

    def update_status(self, user_id, filename, state, status_detail):
        try:
            cursor = self.connection.cursor()
            sql = "Update upload_files SET state = ?, status_detail = ? Where user_id = ? AND file_name = ?"
            values = (state, status_detail,user_id,filename)
            cursor.execute(sql,values)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            return e
    
    def update_upload_files_details(self, user_id, file_name, state, status_detail):
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO upload_files (user_id, file_name, state, submitted_on, status_detail) VALUES (?,?,?,?,?)"
            values = (user_id, file_name, state, datetime.now(), status_detail)
            cursor.execute(sql, values)
            self.connection.commit()
            cursor.close()
            logger.info("file uploaded successfully")
            return ''
            
        except Exception as e:
            logger.error(f"Error uploading file : {str(e)}")
            return str(e)
        
    def get_upload_files_details(self, user_id):
        try:
            cursor = self.connection.cursor()
            sql = """SELECT * FROM upload_files WHERE user_id = ? ORDER BY submitted_on DESC"""
            cursor.execute(sql, (user_id,))
            files_details = cursor.fetchall()
            cursor.close()
            result = []
            for row in files_details:
                result.append({
                    'user_id': row.user_id,
                    'file_name': os.path.basename(row.file_name),
                    'state': row.state,
                    'status_detail': row.status_detail,
                    'submitted_on': row.submitted_on
                })
            return result
        except Exception as e:
            logger.error(f"Error retrieving uploaded files: {e}")
            return []

            