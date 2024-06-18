import os
import requests
import shutil
import uuid

# Configuration
API_URL = "http://your-immich-instance/api"  # Replace with your Immich API URL
API_KEY = "your-api-key"  # Replace with your Immich API key
PERSON_ID = "your-person-id"  # Replace with the person's ID
START_DATE = "2000-01-01T00:00:00Z"  # Start date for the search
END_DATE = "2022-12-31T23:59:59Z"  # End date for the search
DOWNLOAD_PATH = "/path/to/your/download/directory"  # Directory to save downloaded photos

# Headers for the API requests
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def get_assets():
    """
    Fetches the list of assets (photos) for the specified person within the date range.
    Handles pagination to ensure all assets are retrieved.
    """
    page = 1
    all_assets = []
    while True:
        print(f"Fetching asset list, page {page}...")
        url = f"{API_URL}/search/metadata"
        payload = {
            "personIds": [PERSON_ID],
            "takenAfter": START_DATE,
            "takenBefore": END_DATE,
            "type": "IMAGE",
            "page": page,
            "size": 100
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        response.raise_for_status()
        data = response.json()["assets"]
        assets = data["items"]
        if not assets:
            break
        all_assets.extend(assets)
        page += 1
    print(f"Found {len(all_assets)} assets.")
    return all_assets

def get_download_info(asset_ids):
    """
    Gets the download information for the specified asset IDs.
    """
    url = f"{API_URL}/download/info"
    payload = {
        "albumId": str(uuid.uuid4()),  # Generate a random UUID for albumId
        "archiveSize": 1,  # Set a positive number for archiveSize
        "assetIds": asset_ids,
        "userId": str(uuid.uuid4())  # Generate a random UUID for userId if required
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"Download Info Status Code: {response.status_code}")
    if response.status_code != 201:
        print(f"Error details: {response.json()}")
    response.raise_for_status()
    return response.json()

def download_archive(asset_ids):
    """
    Downloads the archive of the specified asset IDs.
    """
    url = f"{API_URL}/download/archive"
    payload = {
        "assetIds": asset_ids
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    print(f"Download Archive Status Code: {response.status_code}")
    if response.status_code == 200:
        zip_path = os.path.join(DOWNLOAD_PATH, "assets.zip")
        with open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"Downloaded archive to {zip_path}")
    else:
        print(f"Failed to download archive - Status Code: {response.status_code}")

def main(copy_files):
    """
    Main function to fetch and either list or download assets based on the `copy_files` flag.
    """
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    assets = get_assets()
    asset_ids = [asset['id'] for asset in assets]
    if copy_files:
        download_info = get_download_info(asset_ids)
        download_archive(asset_ids)
    else:
        for asset in assets:
            print(f"Asset: {asset['originalFileName']} - Created at: {asset['fileCreatedAt']}")

if __name__ == "__main__":
    import sys
    copy_files = 'copy' in sys.argv
    main(copy_files)
