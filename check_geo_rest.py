import googlemaps
import redis

def connection_redis():
    host_redis = '127.0.0.1'
    connection = redis.StrictRedis(host=host_redis)
    return connection

def connection_api_google_maps():
    connection_gmaps = googlemaps.Client(key='AIzaSyCzZl5o6V0R0QtvqbrfMDeRTGR2nIsQrhE')
    return connection_gmaps

def get_keys_redis(connect):
    list_members = []
    restaurant_key = connect.keys('Restaurantes')
    members_restaurants = connect.execute_command('ZRANGE ' + restaurant_key[0] + ' 0' + ' -1')
    for member in members_restaurants:
        list_members.append(member)
    return list_members

def check_if_member_exist(member, members_of_restaurants):
    member_exist = False
    for members in members_of_restaurants:
        if members == member:
            member_exist = True
    return member_exist

def get_position_in_google_maps(member, connection):
    if member == 'Yo':
        geocode_result_my_position = connection.geocode("""Carrer de Granollers, 8, Barcelona""")
        return geocode_result_my_position
    if member == 'Txetxu':
        geocode_result_txetxu_taberna = connection.geocode("""Calle del Tajo, 29, 08032 Barcelona""")
        return geocode_result_txetxu_taberna
    if member == 'Quimet':
        geocode_result_kimet = connection.geocode("""Quimet d'Horta, Plaza Ibiza, Horta, Barcelona""")
        return geocode_result_kimet
    if member == 'Ali':
        geocode_result_ali = connection.geocode("""Ali Baba, Carrer del Tajo, Barcelona""")
        return geocode_result_ali

def add_geo_position_in_redis(connection, geo, member):
    connection.execute_command('GEOADD Restaurantes ' + str(geo[0]['geometry']['location']['lat']) + ' ' + str(geo[0]['geometry']['location']['lng']) + ' ' + member)

def nearest_restaurant(connect, my_position, distance):
    print connect.execute_command('GEORADIUSBYMEMBER Restaurantes ' + my_position + ' ' + distance + ' m')

def get_key_redis_my_position(keys):
    for key in keys:
        if key == 'Yo':
            return key

if __name__ == '__main__':
    name_member_restaurant = 'Quimet'
    name_member_my = 'Yo'
    distance = '400'
    connect_redis = connection_redis()
    connect_api_google_maps = connection_api_google_maps()
    my_geo_position = get_position_in_google_maps(name_member_my, connect_api_google_maps)
    add_geo_position_in_redis(connect_redis, my_geo_position, name_member_my)
    members_of_restaurants = get_keys_redis(connect_redis)
    member_status = check_if_member_exist(name_member_restaurant, members_of_restaurants)
    if False == member_status:
        restaurant_geo_position = get_position_in_google_maps(name_member_restaurant, connect_api_google_maps)
        add_geo_position_in_redis(connect_redis, restaurant_geo_position, name_member_restaurant)
    nearest_restaurant(connect_redis, name_member_my, distance)






