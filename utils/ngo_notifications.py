from database import users_collection
from database import notification_collection

from utils.location import nearby


def notify_nearby_ngos(item):

    ngos = users_collection.find(
        {
            "role": "NGO"
        }
    )

    for ngo in ngos:

        if nearby(

            item["latitude"],
            item["longitude"],

            ngo.get("latitude"),
            ngo.get("longitude")

        ):

            notification_collection.insert_one(
                {

                    "username":
                    ngo["username"],

                    "message":
                    f"New donation available near you ({item['category']})",

                    "read":
                    False
                }
            )