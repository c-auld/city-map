import folium
import pandas as pd
import math

data = pd.read_csv('worldcities.csv')

cities = list(data['city'])
lats = list(data['lat'])
lons = list(data['lng'])
countries = list(data['country'])
states = list(data['admin_name'])
populations = list(data['population'])

info = """<h4>%s</h4>
Country: %s<br>
State: %s<br>
Population: %s<br>"""

#Some populations are stated as NaN 
def check_population(population):
    if math.isnan(population):
        return 'Unkown'
    else:
        return population

#Map object with initial position set to London
map = folium.Map(location = [51.507351, -0.127758], tiles = "OpenStreetMap")
fg_maj = folium.FeatureGroup(name="Major Cities")
fg_min = folium.FeatureGroup(name="Minor Cities")

#Add children to fg_maj feature group
for city, lat, lon, country, state, population in zip(cities, lats, lons, countries, states, populations):    
    
    iframe = folium.IFrame(html= info % (city, country, state, check_population(population)), width=200, height=100)
    
    if population > 1000000:
        fg_maj.add_child(folium.CircleMarker(
            radius=6,
            location=[lat,lon],
            popup= folium.Popup(iframe),
            fill_color='red',
            color='red',
            fill=True
            ))
        
    else:
        fg_min.add_child(folium.CircleMarker(
            radius=6,
            location=[lat,lon],
            popup= folium.Popup(iframe),
            fill_color='green',
            fill=True
            ))

map.add_child(fg_maj)
map.add_child(fg_min)
map.add_child(folium.LayerControl())
map.save("Cities.html")