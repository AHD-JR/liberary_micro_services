import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client['bookstore']


def check_db_connection():
    try:
        client.server_info()
        print("Connected to MongoDB 🚀")
    except:
        print('Could not connect to MongoDB!')

#Collections
books_collection = db['books']      
borrow_data_collection = db['borrow_data']