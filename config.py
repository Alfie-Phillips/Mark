import os
import dotenv

dotenv.load_dotenv()

# Global Vars
TOKEN = os.environ["TOKEN"]
MONGO_URI = os.environ["MONGO_URI"]

# Game Vars
INTERMISSION_TIME = 20
BETTING_TIME = 50
PLAYING_TIME = 120
MESSAGE_GAP = 10
