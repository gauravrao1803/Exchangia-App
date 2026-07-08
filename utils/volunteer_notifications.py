from database import users_collection
from database import notification_collection

from utils.location import nearby


def notify_nearby_volunteers(item):

    volunteers = users_collection.find(
        {
            "role": "Volunteer"
        }
    )

    for volunteer in volunteers:

        if nearby(

            item["latitude"],
            item["longitude"],

            volunteer.get("latitude"),
            volunteer.get("longitude")

        ):

            notification_collection.insert_one(
                {
                    "username":
                    volunteer["username"],

                    "message":
                    f"Donation pickup available near you ({item['category']})",

                    "read":
                    False
                }
            )