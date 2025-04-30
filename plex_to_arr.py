from time import sleep
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
SONARR_API_KEY = os.getenv("SONARR_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
RADARR_URL = os.getenv("RADARR_URL")
SONARR_URL = os.getenv("SONARR_URL")
QUALITY_PROFILE_NAME = os.getenv("QUALITY_PROFILE_NAME")

def get_quality_profile_id(URL, API_KEY):
    quality_profiles_url = f"{URL}/api/v3/qualityProfile?apikey={API_KEY}"
    response = requests.get(quality_profiles_url)
    if response.status_code == 200:
        quality_profiles = response.json()
        for profile in quality_profiles:
            if profile["name"] == QUALITY_PROFILE_NAME:
                return profile["id"]
    else:
        print(f"Failed to retrieve quality profiles. Status Code: {response.status_code}", flush=True )
    return None

RADARR_QUALITY_PROFILE = get_quality_profile_id(RADARR_URL, RADARR_API_KEY)
SONARR_QUALITY_PROFILE = get_quality_profile_id(SONARR_URL, SONARR_API_KEY)

def get_root_folder(URL, API_KEY):
    root_folder_url = f"{URL}/api/v3/rootfolder?apikey={API_KEY}"
    response = requests.get(root_folder_url)
    if response.status_code == 200:
        root_data = response.json()
        return root_data[0]['path']
    else:
        print(f'Failed to get root path for {URL}. Status Code: {response.status_code}', flush=True )
    return none

RADARR_ROOT_FOLDER = get_root_folder(RADARR_URL, RADARR_API_KEY)
SONARR_ROOT_FOLDER = get_root_folder(SONARR_URL, SONARR_API_KEY)

def get_language(URL, API_KEY):
    language_url = f"{URL}/api/v3/config/ui?apikey={API_KEY}"
    response = requests.get(language_url)
    if response.status_code == 200:
        language_data = response.json()
        print(language_url['uiLanguage'])
        return language_url['uiLanguage']
    else:
        print(f'Failed to language for {URL}. Status Code: {response.status_code}', flush=True )
    return none    

SONARR_LANGUAGE_PROFILE = int(get_language(SONARR_URL, SONARR_API_KEY))

def fetch_plex_watchlist():
    print("Fetching Plex watchlist...", flush=True)
    plex_url = f"https://metadata.provider.plex.tv/library/sections/watchlist/all?X-Plex-Token={PLEX_TOKEN}"
    response = requests.get(plex_url)
    root = ET.fromstring(response.content)
    return root.findall('Directory') + root.findall('Video')

def remove_from_plex_watchlist(item_guid):
    ratingKey = item_guid.rsplit('/', 1)[-1]
    plex_url = f"https://metadata.provider.plex.tv/actions/removeFromWatchlist?ratingKey={ratingKey}&X-Plex-Token={PLEX_TOKEN}"
    response = requests.put(plex_url)
    if response.status_code != 200:
        print(f"Failed to remove item from watchlist. Status Code: {response.status_code}", flush=True)
    return None

def fetch_tmdb_id(title, media_type, year):
    if media_type == "show":
        search_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&year={year}&query={title}"
    else:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&year={year}&query={title}"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            # Assuming the first result is the most relevant one
            return results[0]['id']
        else:
            print(f"No TMDB ID found for {media_type} '{title}'", flush=True)
            return None
    else:
        print(f"Failed to retrieve TMDB ID for {media_type} '{title}'", flush=True)
        return None

def add_to_radarr(tmdb_id, title, year):
    print(f"Adding movie '{title}' to Radarr...", flush=True)
    payload = {
        "title": title,
        "year": year,
        "qualityProfileId": int(RADARR_QUALITY_PROFILE),
        "tmdbId": tmdb_id,
        "rootFolderPath": RADARR_ROOT_FOLDER,
        "monitored": True,
        "addOptions": {
            "searchForMovie": True
        }
    }
    radarr_add_url = f"{RADARR_URL}/api/v3/movie?apikey={RADARR_API_KEY}"
    response = requests.post(radarr_add_url, json=payload)
    if response.status_code == 201:
        print(f"Added movie '{title} ({year})' to Radarr successfully.", flush=True)
    else:
        try:
            error_message = response.json()[0]['errorMessage']
            print(f"Failed to add movie '{title} ({year})' to Radarr. Error: {error_message}", flush=True)
        except (KeyError, IndexError):
            print(f"Failed to add movie '{title} ({year})' to Radarr. Status Code: {response.status_code}", flush=True)

def add_to_sonarr(tmdb_id, title, year):
    print(f"Adding series '{title} ({year})' to Sonarr...", flush=True)
    payload = {
        "title": title,
        "year": year,
        "qualityProfileId": int(SONARR_QUALITY_PROFILE),
        "languageProfileId": int(SONARR_LANGUAGE_PROFILE),
        "tvdbId": tmdb_id,
        "rootFolderPath": SONARR_ROOT_FOLDER,
        "monitored": True,
        "addOptions": {
            "searchForMissingEpisodes": True
        }
    }
    sonarr_add_url = f"{SONARR_URL}/api/v3/series?apikey={SONARR_API_KEY}"
    response = requests.post(sonarr_add_url, json=payload)
    if response.status_code == 201:
        print(f"Added series '{title}' to Sonarr successfully.", flush=True)
    else:
        try:
            error_message = response.json()[0]['errorMessage']
            print(f"Failed to add series '{title} ({year})' to Sonarr. Error: {error_message}", flush=True)
        except (KeyError, IndexError):
            print(f"Failed to add series '{title} ({year})' to Sonarr. Status Code: {response.status_code}", flush=True)

def search_and_add_series(search_term, year):
    search_url = f"{SONARR_URL}/api/v3/series/lookup"
    headers = {"X-Api-Key": SONARR_API_KEY}
    params = {"term": search_term}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            series = results[0]  # Assuming the first search result is the desired series
            series_id = series["tvdbId"]
            add_series_url = f"{SONARR_URL}/api/v3/series"
            payload = {
                "title": series["title"],
                "qualityProfileId": int(SONARR_QUALITY_PROFILE),
                "languageProfileId": int(SONARR_LANGUAGE_PROFILE),
                "tvdbId": series_id,
                "rootFolderPath": SONARR_ROOT_FOLDER,
                "monitored": True,
                "addOptions": {
                    "searchForMissingEpisodes": True
                }
            }
            
            response = requests.post(add_series_url, headers=headers, json=payload)
            if response.status_code == 201:
                print(f"Added series '{series['title']}' to Sonarr successfully.", flush=True)
            else:
                try:
                    error_message = response.json()[0]['errorMessage']
                    print(f"Failed to add series '{series['title']} ({year})' to Sonarr. Error: {error_message}", flush=True)
                except (KeyError, IndexError):
                    print(f"Failed to add series '{series['title']} ({year})' to Sonarr. Status Code: {response.status_code}", flush=True)
        else:
            print("No series found for the search term.", flush=True)
    else:
        print("Failed to perform series search.", flush=True)

def main():
    print("Starting script...", flush=True)
    while (True):
        watchlist = fetch_plex_watchlist()
        print(f"Found {len(watchlist)} items in Plex watchlist", flush=True)
        if len(watchlist) > 0:
            print("Processing Plex watchlist...", flush=True)
            for item in watchlist:
                title = item.get('title')
                title_without_year = re.sub("[\(\[].*?[\)\]]", "", item.get('title')) # Workaround for shows with the (YEAR) embedded in the actual title not matching on TMDB
                year = item.get('year')
                guid = item.get('guid')
                media_type = item.get('type')
                if media_type == "movie":
                    tmdb_id = fetch_tmdb_id(title_without_year, media_type, year)
                    if tmdb_id is not None:
                        add_to_radarr(tmdb_id, title, year)
                        remove_from_plex_watchlist(guid)
                elif media_type == "show":
                    tmdb_id = fetch_tmdb_id(title_without_year, media_type, year)
                    if tmdb_id is not None:
                        search_and_add_series(title, year)
                        remove_from_plex_watchlist(guid)
                else:
                    print(f"Unknown media type found: {media_type}",flush=True)
        sleep(120)

if __name__ == "__main__":
    main()
