from datetime import datetime

from database import (
    users_collection,
    points_collection
)


def add_points(username, points, reason):

    user = users_collection.find_one(
        {
            "username": username
        }
    )

    if not user:
        return

    current = user.get(
        "points",
        0
    )

    users_collection.update_one(
        {
            "username": username
        },
        {
            "$set":
            {
                "points": current + points
            }
        }
    )

    points_collection.insert_one(
        {
            "username": username,
            "points": points,
            "reason": reason,
            "date": datetime.now()
        }
    )