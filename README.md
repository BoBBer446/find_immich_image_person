### README.md

# Immich API Photo Downloader

This script allows you to fetch and download all photos associated with a specific person from the Immich API over a given date range. It is particularly useful for users who need to download more than the 5000 photo limit imposed by the Immich web interface.

## Features

- **Fetch Photos**: Retrieve a list of photos associated with a specific person within a specified date range.
- **Download Photos**: Download the photos to a local directory as a single archive.
- **Pagination Handling**: Automatically handles pagination to ensure all photos are fetched.

## Requirements

- Python 3.x
- `requests` library

You can install the required library using pip:
```sh
pip3 install requests
```

## Configuration

Before using the script, configure the following parameters in the `find_immich_image_person.py` file:

- `API_URL`: The base URL of your Immich API (e.g., `"http://your-immich-instance/api"`).
- `API_KEY`: Your API key for accessing the Immich API.
- `PERSON_ID`: The ID of the person whose photos you want to fetch.
- `START_DATE`: The start date for the photo search in ISO format (e.g., `"2000-01-01T00:00:00Z"`).
- `END_DATE`: The end date for the photo search in ISO format (e.g., `"2022-12-31T23:59:59Z"`).
- `DOWNLOAD_PATH`: The local directory where photos will be saved if the `copy` parameter is used.

## Usage

### List Photos
To list all photos of the specified person within the date range:
```sh
python3 find_immich_image_person.py
```

### Download Photos
To download all photos of the specified person within the date range:
```sh
python3 find_immich_image_person.py copy
```

## Suitable For

This script is ideal for users of the Immich platform who need to download a large number of photos quickly and efficiently. It overcomes the 5000 photo download limit of the web interface, making it perfect for users who need to manage and backup extensive photo collections.

## Script Details

### find_immich_image_person

See find_immich_image_person.py

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments

- The Immich team for providing the API and documentation.
