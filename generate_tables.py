from settings import settings
import pyodbc


def get_connection():
    try:
        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={settings.SQL_SERVER_HOST};"
            f"DATABASE={settings.SQL_SERVER_DATABASE};"
            f"UID={settings.SQL_SERVER_USERNAME};"
            f"PWD={settings.SQL_SERVER_PASSWORD};"
        )
        
        if connection:
            print("Connected to SQL Server database.")
            return connection
    except Exception as e:
        print(f"Error connecting to SQL Server database: {e}")
        return None

connection = get_connection()


def create_tables():
    try:
        cursor = connection.cursor()
        # Create chat_history table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='chat_history' AND xtype='U')
            CREATE TABLE chat_history (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id NVARCHAR(255) NOT NULL,
                email NVARCHAR(MAX) NOT NULL,
                query NVARCHAR(MAX) NOT NULL,
                response NVARCHAR(MAX) NOT NULL,
                timestamp DATETIME NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

        
def userproflie_list():
        try:
            cursor = connection.cursor()
            sql = """MERGE INTO userprofilelist AS target
        USING (VALUES 
            ('esg_reporter', 'esg_reporter@ideaentity.com', 'esg_reporter', '1', GETUTCDATE(), 'admin', GETUTCDATE(),'Entity@123')
            ) AS source (user_name, user_email, first_name, last_name, createdon, modifiedby, modifiedon,password)
        ON target.user_name = source.user_name
    WHEN MATCHED THEN 
            UPDATE SET 
                modifiedon = source.modifiedon,
                createdon = source.createdon
    WHEN NOT MATCHED THEN
            INSERT (user_id, user_name, user_email, first_name, last_name,createdon, modifiedby, modifiedon,password)
            VALUES (NEWID(), source.user_name, source.user_email, source.first_name, source.last_name, source.createdon, source.modifiedby, source.modifiedon,source.password);"""
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            print("userprofilelist updated successfully")
        except Exception as e:
            print(f"Error updating user profile list: {e}")


if __name__ == "__main__":
    create_tables()
    # userproflie_list()
