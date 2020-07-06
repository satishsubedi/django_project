from geopy.distance import great_circle


def calculate_distance_using_lat_long(lat1,lng1,lat2,lng2):
    point1=(lat1,lng1)
    point2=(lat2,lng2)
    distance = great_circle(point1,point2).kilometers
    return distance

    #fetch nearest hospital with location
def fetch_nearest_hospital_with_location(hospitals,latitude,longitude,allowed_km_for_hospital=9):
    nearest_hospital_with_location = []
    for hospital in hospitals:
        hospital_distance = calculate_distance_using_lat_long(latitude,longitude,hospital.latitude,hospital.longitude)
        if hospital_distance<=allowed_km_for_hospital:
            hospital_object = {
                "name":hospital.name,
                "distance":hospital_distance
            }
            nearest_hospital_with_location.append(hospital_object)
    return nearest_hospital_with_location
