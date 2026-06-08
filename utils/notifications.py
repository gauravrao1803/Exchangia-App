from datetime import datetime

from database import notification_collection

def create_notification(
    username,
    message
):

    notification_collection.insert_one(
        {
            "username": username,

            "message": message,

            "read": False,

            "timestamp": datetime.now()
        }
    )