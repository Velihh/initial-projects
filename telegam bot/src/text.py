
text = '''
Zipcode Employees       Longitude Latitude
0   02021   174 -71.131057  42.228065
1   02026   193 -71.143038  42.237719
3   02109   45  -71.054027  42.363498
4   02110   14  -71.053642  42.357649
5   02111   30  -71.060280  42.350586
6   02113   77  -71.054618  42.365215
8   02115   116 -71.095106  42.343330
10  02118   318 -71.072103  42.339342
11  02119   804 -71.085268  42.323002
12  02120   168 -71.097569  42.332539
13  02121   781 -71.086649  42.305792
15  02124   1938    -71.066702  42.281721
16  02125   859 -71.053049  42.310813
17  02126   882 -71.090424  42.272444
19  02128   786 -71.016037  42.375254
21  02130   886 -71.114080  42.309087
22  02131   1222    -71.121464  42.285216
23  02132   1348    -71.168150  42.280316
24  02134   230 -71.123323  42.355355
25  02135   584 -71.147046  42.357537
26  02136   1712    -71.125550  42.255064
28  02152   119 -70.960324  42.351129
29  02163   1   -71.120420  42.367263
30  02186   361 -71.113223  42.258883
31  02199   4   -71.082279  42.346991
32  02210   35  -71.044281  42.347148
33  02215   83  -71.103877  42.348709
34  02459   27  -71.187563  42.286356
35  02467   66  -71.157691  42.314277
'''
import pandas as pd
import io
import folium
import folium.plugins

boston = pd.read_csv(io.StringIO(text), sep='\s+')

boston_map = folium.Map([boston.Latitude.mean(), boston.Longitude.mean(), ], zoom_start=12)

incidents2 = folium.plugins.MarkerCluster().add_to(boston_map)

for latitude, longitude, employees in zip(boston.Latitude, boston.Longitude, boston.Employees):
	print(latitude, longitude, employees)
	folium.vector_layers.CircleMarker(
		location=[latitude, longitude],
		tooltip=str(employees),
		radius=employees / 10,
		color='#3186cc',
		fill=True,
		fill_color='#3186cc'
	).add_to(incidents2)

boston_map.add_child(incidents2)
# display in web browser
import webbrowser
boston_map.save('map.html')
webbrowser.open('map.html')