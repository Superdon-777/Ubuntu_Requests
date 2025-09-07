import os
import requests
from urllib.parse import urlparse
import hashlib


def fetch_images(urls):
    folder = "Collected_Images"

    # Make sure the folder exists - create if missing
    os.makedirs(folder, exist_ok=True)

    # Keep track of images we have saved (by hash) to skip duplicates
    downloaded_hashes = set()

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Let's ask politely for the image
            headers = {'User-Agent': 'Ubuntu Image Fetcher - good bot'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Check if what we got is actually an image
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image'):
                print(f"! Skipped: content at {url} is not an image (Content-Type: {content_type})")
                continue

            # Create a fingerprint of this image so we do not save duplicates
            content_hash = hashlib.md5(response.content).hexdigest()
            if content_hash in downloaded_hashes:
                print(f"!! Skipped duplicate image at {url}")
                continue
            downloaded_hashes.add(content_hash)

            # Try to extract the file name from the URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                # If no file name, create one using part of the hash
                filename = f"image_{content_hash[:8]}.jpg"

            # Full path where image will be saved
            filepath = os.path.join(folder, filename)

            # Save the image file in binary mode
            with open(filepath, 'wb') as file:
                file.write(response.content)

            # Confirm success to the user
            print(f"** Successfully fetched: {filename}")
            print(f"** Image saved to {filepath}\n")

        except requests.exceptions.RequestException as e:
            print(f"!!! Connection error for {url}: {e}")
        except Exception as e:
            print(f"!!! Oops, something went wrong with {url}: {e}")


def main():
    print("Welcome to the Ubuntu Image Collector")
    print("A tool for mindfully collecting images from the web\n")

    # Ask user for one or more URLs separated by commas
    urls_input = input("Please enter image URLs separated by commas:\n")
    urls = urls_input.split(',')

    # Fetch all images one by one
    fetch_images(urls)

    print("Connection strengthened & community enriched!")


if __name__ == "__main__":
    main()
