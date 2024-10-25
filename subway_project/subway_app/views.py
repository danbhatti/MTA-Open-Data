from django.http import JsonResponse
from django.shortcuts import render
from .graph import Network, load_station_data

# View for rendering the initial map page
def subway_map(request):
    # Load data and initialize the map with default colors
    network_data = load_station_data('data/MTA_Subway_Stations_and_Complexes_20241018.csv')
    # Create initial GeoDataFrame without running Dijkstra yet
    network = Network(network_data)
    # Send the map to the template to be displayed
    return render(request, 'map_template.html', {'map_data': network})

# View for handling Dijkstra calculation and updating map dynamically
def update_map(request):
    if request.method == 'POST':
        # Parse the new origin station from the POST request
        import json
        data = json.loads(request.body)
        origin_station = data.get('origin_station', '33 St')  # Default to '33 St' if not provided
        # Load data and create network
        network_data = load_station_data('data/MTA_Subway_Stations_and_Complexes_20241018.csv')
        network = Network(network_data)
        # Run Dijkstra's algorithm with the new origin station
        dijkstra_result = network.dijkstra(origin_station)
        # Create GeoDataFrame for updated map
        updated_map = network.plot_interactive_map(network_data, dijkstra_result)
        # Return updated map data as JSON to the frontend
        return JsonResponse({'map_data': updated_map})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
