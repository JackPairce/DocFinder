import os
import pandas as pd
from tqdm import tqdm
import requests


def download_file(url: str, path: str) -> None:
    """
    Downloads a file from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the file to download.
        path (str): The local file path where the downloaded file will be saved.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    CHUNK_SIZE = 4096
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(path, "wb") as file:

            total_length = int(response.headers.get("content-length")) / CHUNK_SIZE  # type: ignore
            for data in tqdm(
                response.iter_content(chunk_size=CHUNK_SIZE),
                desc="Downloading",
                total=total_length,
                unit="B",
                unit_scale=True,
            ):
                file.write(data)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")


def read_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file from the specified path and returns it as a pandas DataFrame.

    Args:
        path (str): The path to the CSV file to read.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    return pd.read_csv(path)  # type: ignore


def remove_file(path: str) -> None:
    """
    Removes a file from the specified path.

    Args:
        path (str): The path to the file to be removed.

    Raises:
        FileNotFoundError: If the file does not exist at the specified path.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    os.remove(path)
