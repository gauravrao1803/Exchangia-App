from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- USERNAME ----------------
username = "gauravrao1803"

# ---------------- PASSWORD ----------------
password = quote_plus("hello@1144")

# ---------------- MONGO URI ----------------
MONGO_URI = (
    f"mongodb+srv://{username}:{password}"
    f"@exchangia.alueqyw.mongodb.net/"
    f"?retryWrites=true&w=majority&appName=Exchangia"
)

# ---------------- CONNECT DATABASE ----------------
client = MongoClient(MONGO_URI)

# ---------------- DATABASE ----------------
db = client["ExchangiaDB"]

# ---------------- COLLECTIONS ----------------
# Existing collections

users_collection = db["users"]

exchange_collection = db["exchange_items"]

charity_collection = db["charity_items"]

volunteer_collection = db["volunteer_requests"]

notification_collection = db["notifications"]

exchange_requests_collection = db["exchange_requests"]

charity_requests_collection = db["charity_requests"]

# ==========================
# NEW COLLECTIONS
# ==========================

points_collection = db["reward_points"]

badges_collection = db["badges"]

leaderboard_collection = db["leaderboard"]

reward_history_collection = db["reward_history"]