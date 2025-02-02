import requests
import time

# Replace with your actual API token
API_TOKEN = "YOUR_API_KEY"
BASE_URL = "https://torbox.net/api/v1"

def get_torrents():
    """Fetch the list of torrents."""
    url = f"{BASE_URL}/torrents?api_token={API_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of torrents
    else:
        print("Error fetching torrents:", response.text)
        return []

def delete_torrent(torrent_id):
    """Delete a torrent by its ID."""
    url = f"{BASE_URL}/torrents/{torrent_id}?api_token={API_TOKEN}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Deleted torrent ID: {torrent_id}")
    else:
        print("Error deleting torrent:", response.text)

def auto_delete_oldest():
    """Deletes the oldest torrent if more than 10 are 'Download Ready'."""
    torrents = get_torrents()
    
    # Filter torrents that are in "Download Ready" state
    download_ready_torrents = [t for t in torrents if t.get("status") == "Download Ready"]

    if len(download_ready_torrents) > 5:
        # Ensure the latest updated torrent is not deleted
        # Sort torrents by last updated time (oldest first)
        download_ready_torrents.sort(key=lambda t: t["last_updated_at"])
        
        # Get the most recently updated torrent
        latest_torrent = download_ready_torrents[-1]
        
        # If there's only one torrent, don't delete it
        if len(download_ready_torrents) == 1:
            print("Only one torrent available, nothing to delete.")
            return
        
        # Delete the oldest torrent that is not the latest updated one
        oldest_torrent = download_ready_torrents[0]
        
        # Make sure the oldest isn't the latest updated torrent
        if oldest_torrent["id"] != latest_torrent["id"]:
            print(f"Deleting oldest torrent: {oldest_torrent['name']}")
            delete_torrent(oldest_torrent["id"])
        else:
            print("Skipping deletion, the latest torrent is the oldest one.")
    else:
        print("No need to delete, under 10 torrents.")

# Run the script
auto_delete_oldest()
