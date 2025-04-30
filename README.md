# Plex to Radarr/Sonarr Integration

This repository provides a script for integrating Plex watchlist with Radarr. It allows users to automatically add movies from their Plex watchlist to Radarr for automated downloading and management.

## Features

- Fetch Plex watchlist and process movies
- Retrieve TMDB ID for each movie
- Add movies to Radarr using specified quality profile
- Error handling for failed requests

## Prerequisites

Before using this script, make sure you have the following:

- Basic understanding of Docker
- Radarr/Sonarr installed and configured with an API key.
- Plex server with a valid Plex token.

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
         - PLEX_TOKEN=
         - RADARR_API_KEY=
         - SONARR_API_KEY=
         - TMDB_API_KEY=
         - RADARR_URL=
         - SONARR_URL=
         - RADARR_ROOT_FOLDER=
         - SONARR_ROOT_FOLDER=
       image: ghcr.io/legionofone/plex2arr:main
   ```
