from django.shortcuts import render
import folium
import geocoder
import pika, sys, os
import re
import threading
from pymongo import MongoClient


# Create your views here.

# m = folium.Map(location=[19, -12], zoom_start=2)


def receive():
    def body_to_dict(body):
        s = body.decode('UTF-8')
        res = re.findall(r'\'.*?\'', s)
        str(res[0])
        str(res[1])
        str(res[2])
        str(res[3])
        date = res[0].replace("'", "")
        lat = res[1].replace("'", "")
        lng = res[2].replace("'", "")
        id = res[3].replace("'", "")

        # date = float(date)
        lat = float(lat)
        lng = float(lng)
        # id = float(id)

        # lat=> enlem
        # lng=> boylam
        body_dict = {
            "date": date,
            "lat": lat,
            "lng": lng,
            "id": id
        }
        return body_dict

    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    method_frame, header_frame, body = channel.basic_get(queue='hello')
    if method_frame is None:
        connection.close()
        return None
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        dict_body = body_to_dict(body)
        return dict_body


def view_map(request):
    cluster = MongoClient("mongodb://bugra:bugra@cluster0-shard-00-00.1foqp.mongodb.net:27017,"
                          "cluster0-shard-00-01.1foqp.mongodb.net:27017,"
                          "cluster0-shard-00-02.1foqp.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-hpmscs"
                          "-shard-0&authSource=admin&retryWrites=true&w=majority")
    print("after cluster")
    db = cluster["test_db"]
    collection = db["csv_info_test"]

    def send_to_mongo(locations):
        i = 0
        for i in range(0, 1774):
            collection.insert_one(locations[i])
            print(f"posted!{i}")
        print("they are all gone")

    data = list()

    # location = geocoder.osm('tokat')
    # lat = location.lat
    # lng = location.lng
    # country = location.country

    # Create Map Object
    m = folium.Map(location=[19, -12], zoom_start=2)
    # folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
    # folium.Marker([12.594, -0.219]).add_to(m)
    # folium.Marker([37.593, 42.212]).add_to(m)
    # Get HTML Representation of Map Object

    # Receive things starts here:
    try:
        # mongo thread burda tanımlansın
        thread_mongo = threading.Thread(target=send_to_mongo, args=(data,), )
        location = receive()
        if location is not None:
            data.append(location)

        if data:
            while True:
                location = receive()
                if location is not None:
                    data.append(location)
                else:
                    break

        if data:
            i = 0
            for i in range(0, len(data)):
                folium.Marker(location=[data[i]['lat'], data[i]['lng']]).add_to(m)
            thread_mongo.start()# Thread başlar

        m = m._repr_html_()

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    context = {
        'm': m,
    }
    return render(request, "map/main.html", context)
