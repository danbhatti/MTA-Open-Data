import folium
from flask import Flask, render_template_string, jsonify, request
import requests
import pandas as pd
import graph

app = Flask(__name__)

# Global variable to hold the results DataFrame and graph
results = requests.get('https://data.ny.gov/resource/5f5g-n3cz.json?cbd=TRUE').json()
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
    shortest_paths = results_graph.dijkstra(35)

    

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

        # Create a unique identifier for the marker
        click_event_script += f"""
        var circleMarker{i} = L.circleMarker([{results_df.iloc[i, 12]}, {results_df.iloc[i, 13]}], {{
            color: '{station_color}',
            fillOpacity: 0.7,
            radius: 6,
            tooltip: '{stop_name}'
        }}).add_to(subway_map);

        circleMarker{i}.on('click', function() {{
            onMarkerClick("{{ results_df.iloc[i]['Complex ID'] }}");  // Use Stop Name for the request
        }});
        """

    click_event_script += """
    function updateMarkers(data) {
        data.colors.forEach((color, index) => {
            if (circleMarker[index]) {
                circleMarker[index].setStyle({color: color});
            }
        });
        console.log("Markers updated with new colors:", data.colors);  // Debugging log
    }
    </script>"""
    
    click_event_script += "</script>"

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



  
@app.route('/recompute_paths')
def recompute_paths():
    #stop_name = request.args.get('23%20St')
    #print(f"Received request to recompute paths from station: {stop_name}")  # Log station name
    
    shortest_paths = results_graph.dijkstra(31)
    station_colors = [get_station_color(distance) for distance in shortest_paths]
    
    print(f"Calculated colors for each station: {station_colors}")  # Log the computed colors
    return jsonify(colors=station_colors)
    


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