from database import users_collection


def update_badge(username):

    user = users_collection.find_one(
        {
            "username": username
        }
    )

    if not user:
        return

    points = user.get(
        "points",
        0
    )

    if points >= 2000:

        badge = "🏆 Legend"

    elif points >= 1000:

        badge = "🥇 Gold"

    elif points >= 500:

        badge = "🥈 Silver"

    elif points >= 200:

        badge = "🥉 Bronze"

    else:

        badge = "🌱 Beginner"

    users_collection.update_one(
        {
            "username": username
        },
        {
            "$set":
            {
                "badge": badge
            }
        }
    )