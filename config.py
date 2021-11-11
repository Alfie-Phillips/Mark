import os
import dotenv

dotenv.load_dotenv()

# Global Vars
TOKEN = os.environ["TOKEN"]
MONGO_URI = os.environ["MONGO_URI"]
