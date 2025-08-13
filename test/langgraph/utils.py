import math

def get_location_metres(original_latitude, original_longitude, d_north, d_east):
    """
    Calculates a new GPS coordinate by moving a specified distance in meters
    from an original coordinate.

    Args:
        original_latitude (float): The starting latitude.
        original_longitude (float): The starting longitude.
        d_north (float): The distance to move north in meters.
        d_east (float): The distance to move east in meters.

    Returns:
        A tuple of (new_latitude, new_longitude).
    """
    earth_radius = 6378137.0  # Radius of "spherical" earth
    # if d_north/d_east are strings, convert to float
    if isinstance(d_north, str):
        d_north = float(d_north)
    if isinstance(d_east, str):
        d_east = float(d_east)
    # Coordinate offsets in radians
    d_lat = d_north / earth_radius
    d_lon = d_east / (earth_radius * math.cos(math.pi * original_latitude / 180))

    # New position in decimal degrees
    new_lat = original_latitude + (d_lat * 180 / math.pi)
    new_lon = original_longitude + (d_lon * 180 / math.pi)

    return new_lat, new_lon

def get_bearing_and_move(current_lat, current_lon, current_heading, relative_direction, distance_m):
    """
    Calculates a new GPS coordinate based on the drone's current heading and a relative direction.
    """
    direction_angles = {
        "forward": 0,
        "forward_right": 45,
        "right": 90,
        "back_right": 135,
        "back": 180,
        "back_left": 225,
        "left": 270,
        "forward_left": 315,
    }

    # if distance_m is a string, convert to float
    if isinstance(distance_m, str):
        distance_m = float(distance_m)
    
    relative_angle_deg = direction_angles.get(relative_direction, 0)
    
    # Calculate the absolute bearing in degrees
    absolute_bearing_deg = (current_heading + relative_angle_deg) % 360
    absolute_bearing_rad = math.radians(absolute_bearing_deg)

    # Calculate movement in North and East directions
    d_north = distance_m * math.cos(absolute_bearing_rad)
    d_east = distance_m * math.sin(absolute_bearing_rad)

    return get_location_metres(current_lat, current_lon, d_north, d_east)

def get_cardinal_and_move(current_lat, current_lon, cardinal_direction, distance_m):
    """
    Calculates a new GPS coordinate based on a cardinal direction.
    """
    cardinal_angles = {
        "N": 0,
        "NE": 45,
        "E": 90,
        "SE": 135,
        "S": 180,
        "SW": 225,
        "W": 270,
        "NW": 315,
    }
    
    bearing_deg = cardinal_angles.get(cardinal_direction, 0)
    bearing_rad = math.radians(bearing_deg)

    # Calculate movement in North and East directions
    d_north = distance_m * math.cos(bearing_rad)
    d_east = distance_m * math.sin(bearing_rad)

    return get_location_metres(current_lat, current_lon, d_north, d_east)

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance in meters between two points
    on the earth, specified in decimal degrees.
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000  # Radius of earth in meters
    return c * r
