import folium
from flask import Flask, render_template_string, jsonify, request
import requests
import pandas as pd
import graph

app = Flask(__name__)

# Global variable to hold the results DataFrame and graph
results = requests.get('https://data.ny.gov/resource/5f5g-n3cz.json?').json()
results_df = pd.DataFrame.from_records(results)
results_graph = graph.Network(results_df)
station_color = '#0039A6'
subway_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12,
                            width=800, height=500)



@app.route("/")
def home():
    global results, results_df, results_graph, subway_map
    #results = requests.get('https://data.ny.gov/resource/5f5g-n3cz.json?$$app_token=5cNQYqwwGoXLCZfec7e7kJXEk').json()
    #results_df = pd.DataFrame.from_records(results)
    #results_graph = graph.Network(results_df)
    shortest_paths = results_graph.dijkstra(55)

    

    markers = []
    click_event_script = "<script>\n"
    for i in range(len(shortest_paths)):
        station_color = get_station_color(shortest_paths[i])
        stop_name = results_df.iloc[i, 4]
        marker = folium_circle_marker(results_df.iloc[i, 12],
                                      results_df.iloc[i, 13],
                                      station_color,
                                      stop_name)
        markers.append(marker)
        marker.add_to(subway_map)

      
       
    

    subway_map.get_root().render()

    header = subway_map.get_root().header.render()
    body_html = subway_map.get_root().html.render()
    script = subway_map.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Embed folium map in HTML page</h1>
                    {{ body_html|safe }}
                    <h3>This map is embeded in a flask server web page !</h3>
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )



 
def folium_circle_marker(lat, long, color, name):
    return folium.CircleMarker(
            location=(lat, long),
            radius=6,
            color= color,
            fill=True,
            fill_opacity=0.7,
            tooltip=f"Display Name: {name}"
        )



def get_station_color(distance):
    if distance == 0:
        return 'black'
    elif distance == 1:
        return 'green'
    elif distance == 2:
        return 'yellow'
    elif distance == 3:
        return 'red'
    return '#0039A6'  # Default color

if __name__ == "__main__":
    app.run(debug=True)