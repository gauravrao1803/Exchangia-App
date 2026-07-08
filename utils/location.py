from geopy.distance import geodesic


def nearby(lat1, lon1, lat2, lon2):

    if None in [
        lat1,
        lon1,
        lat2,
        lon2
    ]:

        return False

    distance = geodesic(
        (lat1, lon1),
        (lat2, lon2)
    ).km

    return distance <= 10