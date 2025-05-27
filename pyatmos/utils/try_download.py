import requests
from urllib.parse import urlparse
import os
from tqdm import tqdm
import time


def wget_download(url, save_path, msg1=None, msg2=None, timeout=30, chunk_size=8192):
    """
    Downloads a file from a URL to a specified location, retrying indefinitely until successful.

    Args:
        url (str): The URL of the file to download.
        save_path (str): The local path where the file will be saved.
        timeout (int): Timeout for each request attempt in seconds (default: 10).
        chunk_size (int): Size of chunks for streaming download (default: 8192 bytes).

    Returns:
        bool: True when download is successful (always returns True as it never gives up).
    """
    # Ensure the save directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Extract filename from URL if save_path is a directory
    if os.path.isdir(save_path):
        filename = os.path.basename(urlparse(url).path) or "downloaded_file"
        save_path = os.path.join(save_path, filename)

    attempt = 1
    while True:
        try:
            # Make a HEAD request to get file size for progress bar
            response = requests.head(url, timeout=timeout)
            total_size = int(response.headers.get("content-length", 0))

            # Start the download
            with requests.get(url, stream=True, timeout=timeout) as r:
                r.raise_for_status()  # Raise exception for bad status codes

                # Initialize progress bar
                progress_bar = tqdm(
                    total=total_size,
                    unit="iB",
                    unit_scale=True,
                    desc=f"Downloading (Attempt {attempt})",
                )

                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
                            progress_bar.update(len(chunk))

                progress_bar.close()
                print(f"File successfully downloaded to {save_path}")
                return True  # Download successful

        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"Attempt {attempt} failed: {e}. Retrying in 5 seconds...")
            attempt += 1
            time.sleep(5)  # Wait before retrying
