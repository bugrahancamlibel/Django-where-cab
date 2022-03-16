from django.shortcuts import render
import folium
import geocoder


# Create your views here.

def view_map(request):
    # location = geocoder.osm('tokat')
    # lat = location.lat
    # lng = location.lng
    # country = location.country

    # Create Map Object
    m = folium.Map(location=[19, -12], zoom_start=2)
    # folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
    folium.Marker([12.594, -0.219]).add_to(m)
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, "map/main.html", context)


