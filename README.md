# Plex to Radarr/Sonarr Integration

This repository provides a script for integrating Plex watchlist with Radarr and Sonarr. It allows users to automatically add movies or TV Shows from their Plex watchlist to Radarr or Sonarr for automated downloading and management.

### This script automatically removes added movies and TV shows from the watchlist. 

## Features

- Fetch Plex watchlist and process movies
- Retrieve TMDB ID for each movie
- Add movies to Radarr using specified quality profile
- Error handling for failed requests

## Prerequisites

Before using this script, make sure you have the following:

- Basic understanding of Docker
- Radarr and Sonarr installed and configured with API keys.
- Plex server with a valid Plex token.
- TMDB account with API Key

## Setup Instructions

### Docker Compose Example
   ```
   version: '3.3'
   services:
     plex2arr:
       restart: unless-stopped
       container_name: plex2arr
       network_mode: bridge
       environment:
         - PLEX_TOKEN= #Token retrieved from Plex URL
         - RADARR_API_KEY= #Token from the Settings > General > API Key field on Radarr
         - SONARR_API_KEY= #Token from the Settings > General > API Key field on Sonarr
         - TMDB_API_KEY= #Token you generate after creating a TMDB account
         - RADARR_URL= #Full URL including HTTP or HTTPS of your Radarr instance without a trailing forward slash (e.g. https://radarr.example.com)
         - SONARR_URL= #Full URL including HTTP or HTTPS of your Sonarr instance without a trailing forward slash (e.g. https://sonarr.example.com)
         - QUALITY_PROFILE_NAME= #Full name of whatever profile you want shows or movies to use (e.g. 1080p)
       image: ghcr.io/legionofone/plex2arr:main
   ```
### Unraid Template

1. Create a new container by going to the docker tab then clicking "Add Container" at the bottom left
2. Fill in the template with the following information, create VARIABLES for each of the shown fields. Reference the Docker Compose Example for what to put in each field.
   ![alt text](https://github.com/Legionofone/plex2arr/blob/main/markdown/plex2arrunraid.png "Unraid Example")
