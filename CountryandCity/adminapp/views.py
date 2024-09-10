from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

from django.http import JsonResponse
import requests

# countries_data = None

# def get_countries_data():
#     global countries_data
#     url = "https://countriesnow.space/api/v0.1/countries"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         countries_data = response.json()['data']  
#         print("Countries data loaded successfully") 
#     except (requests.exceptions.HTTPError, 
#             requests.exceptions.ConnectionError, 
#             requests.exceptions.Timeout, 
#             requests.exceptions.RequestException) as err:
#         print(f"An error occurred: {err}")  
#         countries_data = [] 

# def get_country_by_city(request):
#     global countries_data
#     city_name = request.GET.get('city_name')
    
#     if not city_name:
#         return JsonResponse({'message': "City name parameter 'city_name' is required."}, status=400)
    
#     if countries_data is None:
#         get_countries_data() 
    
#     matching_entries = []

#     city_name_lower = city_name.lower()
#     for country in countries_data:
#         country_name_lower = country['country'].lower()
#         cities = country.get('cities', [])

#         # Check if city_name_lower matches country_name_lower from the start
#         if country_name_lower.startswith(city_name_lower):
#             matching_entries.append({'country': country['country']})

#         # Check if city_name_lower matches any city name from the start
#         matched_cities = [city for city in cities if city.lower().startswith(city_name_lower)]
#         if matched_cities:
#             matching_entries.append({'country': country['country'], 'cities': matched_cities})

#     if matching_entries:
#         print(f"Matching entries found: {matching_entries}") 
#         return JsonResponse({'matching_entries': matching_entries})
    
#     return JsonResponse({'message': f"No matches found for city: {city_name}"}, status=404)

###########################################################################################3333
# from django.shortcuts import render
# from django.http import JsonResponse
# import requests

# # Initialize global variable
# countries_data = None

# def get_countries_data():
#     """
#     Fetches and caches countries data from the external API.
#     """
#     global countries_data
#     url = "https://countriesnow.space/api/v0.1/countries"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         countries_data = response.json()['data']  
#         print("Countries data loaded successfully") 
#     except (requests.exceptions.HTTPError, 
#             requests.exceptions.ConnectionError, 
#             requests.exceptions.Timeout, 
#             requests.exceptions.RequestException) as err:
#         print(f"An error occurred: {err}")  
#         countries_data = [] 

# def get_country_by_city(request):
#     """
#     Handles the request to get country information by city name, including
#     comparison with country ISO2 and ISO3 codes.
#     """
#     global countries_data
#     searchparam = request.GET.get('searchparam')
    
#     if not searchparam:
#         return JsonResponse({'message': "City name parameter 'searchparam' is required."}, status=400)
    
#     if countries_data is None:
#         get_countries_data() 
    
#     matching_entries = []
#     city_name_lower = searchparam.lower()

#     for country in countries_data:
#         country_name_lower = country['country'].lower()
#         iso2_lower = country.get('iso2', '').lower()
#         iso3_lower = country.get('iso3', '').lower()
#         cities = country.get('cities', [])

#         # Check if city_name_lower matches country_name_lower, iso2, or iso3 from the start
#         if (country_name_lower.startswith(city_name_lower) or 
#             iso2_lower.startswith(city_name_lower) or 
#             iso3_lower.startswith(city_name_lower)):
#             matching_entries.append({'country': country['country'], 'iso2': iso2_lower, 'iso3': iso3_lower})

#         # Check if city_name_lower matches any city name from the start
#         matched_cities = [city for city in cities if city.lower().startswith(city_name_lower)]
#         if matched_cities:
#             matching_entries.append({'country': country['country'], 'cities': matched_cities})

#     if matching_entries:
#         print(f"Matching entries found: {matching_entries}") 
#         return JsonResponse({'matching_entries': matching_entries})
    
#     return JsonResponse({'message': f"No matches found for city: {searchparam}"}, status=404)
##########################################################################################
from django.http import JsonResponse
import os
import pandas as pd
import requests

# File path to your Excel file
EXCEL_FILE_PATH = '/home/python/Music/ContriesandCities/CountryandCity/countries_abbeservations.xlsx'

# Initialize global variables
countries_data = None
abbreviations_df = None  

def load_data():
    global countries_data, abbreviations_df
    # Load countries data from API
    url = "https://countriesnow.space/api/v0.1/countries"
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries_data = response.json()['data']
    except requests.RequestException as err:
        countries_data = []
    
    # Load abbreviations data from Excel
    if os.path.exists(EXCEL_FILE_PATH):
        try:
            abbreviations_df = pd.read_excel(EXCEL_FILE_PATH)
            abbreviations_df.columns = abbreviations_df.columns.str.strip().str.lower() 
        except Exception as e:
            pass  
    else:
        pass  

def search_country_by_city(searchparam):
    global countries_data, abbreviations_df

    if not searchparam:
        return []

    matching_entries = []
    seen_countries = set()
    searchparam_lower = searchparam.lower()

    # Search in API data
    for country in countries_data:
        country_name_lower = country['country'].lower()
        iso2_lower = country.get('iso2', '').lower()
        iso3_lower = country.get('iso3', '').lower()
        cities = country.get('cities', [])

        # Match against country name, iso2, or iso3
        if (country_name_lower.startswith(searchparam_lower) or 
            iso2_lower.startswith(searchparam_lower) or 
            iso3_lower.startswith(searchparam_lower)):
            entry = {'country': country['country'], 'iso2': country.get('iso2', ''), 'iso3': country.get('iso3', '')}
            if entry['country'].strip().lower() not in seen_countries:
                seen_countries.add(entry['country'].strip().lower())
                matching_entries.append(entry)

        # Match against city names
        matched_cities = [city for city in cities if city.lower().startswith(searchparam_lower)]
        if matched_cities:
            entry = {'country': country['country'], 'cities': matched_cities}
            if entry['country'].strip().lower() not in seen_countries:
                seen_countries.add(entry['country'].strip().lower())
                matching_entries.append(entry)
    
    # Search in Excel data
    if abbreviations_df is not None:
        for _, row in abbreviations_df.iterrows():
            abbreviation_lower = row['abbreviation'].lower()
            if abbreviation_lower.startswith(searchparam_lower):
                entry = {'country': row['country name']}
                if entry['country'].strip().lower() not in seen_countries:
                    seen_countries.add(entry['country'].strip().lower())
                    matching_entries.append(entry)

    return matching_entries

def get_country_by_city(request):
    load_data()

    searchparam = request.GET.get('searchparam')
    if not searchparam:
        return JsonResponse({'message': "City name parameter 'searchparam' is required."}, status=400)

    matching_entries = search_country_by_city(searchparam)
    if matching_entries:
        return JsonResponse({'matching_entries': matching_entries})
    return JsonResponse({'message': f"No matches found for city: {searchparam}"}, status=404)


from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
