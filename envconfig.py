import os
import dotenv

dotenv.load_dotenv()

# Global Vars
TOKEN = os.environ["TOKEN"]
MONGO_URI = os.environ["MONGO_URI"]
SERVER_ID = os.environ["SERVER_ID"]
VERIFICATION_CHANNEL = os.environ["VERIFICATION_CHANNEL"]
WELCOME_CHANNEL = os.environ["WELCOME_CHANNEL"]
SUGGESTION_CHANNEL = os.environ["SUGGESTION_CHANNEL"]
MODERATOR_CHANNEL = os.environ["MODERATOR_CHANNEL"]
MEMBER_ROLE_ID = os.environ["MEMBER_ROLE_ID"]
