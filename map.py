import folium
import pandas

map = folium.Map(location=[44.07,-116.12], zoom_start=6)
fgv = folium.FeatureGroup(name="Volcanoes USA")
volcanoes_data = pandas.read_csv("Volcanoes.txt")
lat = list(volcanoes_data["LAT"])
lon = list(volcanoes_data["LON"])
elev = list(volcanoes_data["ELEV"])
volcano_names = list(volcanoes_data["NAME"])
html_marker = """ <h4>Volcano: %s</h4>
<p>Height: %s m</p>
 """
def elevation_color(elevation):
    if elevation < 1000:
        return "green"
    elif  1000 <= elevation < 3000:
        return "orange"
    else:
        return "red" 


fgp = folium.FeatureGroup(name="Population")

for (lt, ln, el, name) in zip(lat, lon, elev, volcano_names):
    iframe = folium.IFrame(html=html_marker % (name, str(el)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), color="black", fill=True, fill_opacity=0.7, fill_color=elevation_color(el)))

fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor': 'black' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
