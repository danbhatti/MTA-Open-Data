from django.urls import path
from .views import subway_map, update_map

urlpatterns = [
    path('', subway_map, name='subway_map'),  # This serves the map at the base path of subway/
    path('update_map/', update_map, name='update_map'),  # URL for updating the map
]

