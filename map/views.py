from django.shortcuts import render
import folium
import geocoder
import pika, sys, os
import re
import threading
from pymongo import MongoClient
from django.contrib.auth.models import User


# Create your views here.

# m = folium.Map(location=[19, -12], zoom_start=2)
from map.models import Customer, Cars


usernamee = "bugra"

userrname = "ali"

cid = 2

carsid = 4



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
        id = int(id)

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
    username = request.user.username
    print(username)

    if username == usernamee:
        id_car = cid


    # name = Customer.objects.all()
    cars = Cars.objects.all()



    cluster = MongoClient("mongodb://bugra:bugra@cluster0-shard-00-00.1foqp.mongodb.net:27017,"
                          "cluster0-shard-00-01.1foqp.mongodb.net:27017,"
                          "cluster0-shard-00-02.1foqp.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-hpmscs"
                          "-shard-0&authSource=admin&retryWrites=true&w=majority")
    print("after cluster")
    db = cluster["test_db"]
    collection = db["csv_info"]

    if username == userrname:
        id_car = carsid

    def parse_date(date):
        no_space = date.split()
        ymd = no_space[0].split('-')
        time = no_space[1].split(':')

        month = ymd[1]
        day = ymd[2]
        hour = time[0]
        minute = time[1]

        date_dict = {
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute
        }

        # print(f"* month: {month}, day: {day}, hour: {hour}, minute: {minute}")

        return date_dict

    def send_to_mongo(data):
        i = 0
        for i in range(0, len(data)):
            collection.insert_one(data[i])
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
        count_cars = 0

        thread_mongo = threading.Thread(target=send_to_mongo, args=(data,), )
        location = receive()
        if location is not None:
            data.append(location)
        if location is not None:
            print("location is not none!")
            if location['id'] == id_car:
                data.append(location)
                count_cars += 1
                date_dict = parse_date(location['date'])
                # print(f"added{count_cars}st car. id:{location['id']}, lat: {location['lat']}, date: {location['date']}")
                # print(f"*month {date_dict['month']}, day: {date_dict['day']}, hour: {date_dict['hour']}, minute:{date_dict['minute']}")

        if data:
            while True:
                location = receive()
                if location is not None:
                    if location['id'] == id_car:
                        data.append(location)
                        count_cars += 1
                        date_dict = parse_date(location['date'])
                        # print(f"added{count_cars}st car. id:{location['id']}, lat: {location['lat']}, date {location['date']}")
                        # print(f"* month {date_dict['month']}, day: {date_dict['day']}, hour: {date_dict['hour']}, minute:{date_dict['minute']}")

                else:
                    break
        if data:
            if data[0]['id'] != id_car:
                data.pop(0)

        if data:
            i = 0
            last_data = parse_date(data[-1]['date'])
            last_hour = int(last_data['hour'])
            last_minute = int(last_data['minute'])
            last_day = int(last_data['day'])
            thirty_min_ago = last_minute - 30

            if thirty_min_ago < 0:
                thirty_min_ago = 60 + thirty_min_ago
                last_hour -= 1

            for i in range(len(data)-1, 0, -1):
                curr = parse_date(data[i]['date'])
                curr_hour = int(curr['hour'])
                curr_min = int(curr['minute'])
                curr_day = int(curr['day'])
                #curr: 13.49    last: 16.52
                if curr_day == last_day:
                    if curr_min > thirty_min_ago and curr_hour == last_hour or curr_hour > last_hour and curr_min < thirty_min_ago:
                        print(f"selam --->>> {data[i]['date']}")
                        folium.Marker(location=[data[i]['lat'], data[i]['lng']]).add_to(m)
            thread_mongo.start()  # Thread başlar

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
