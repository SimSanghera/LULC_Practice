#----- Data Preparation -----#

"""
This function will handle local zip files and automatically download and unzip files from a URL.

"""

# Load libraries
import os
import zipfile
import requests
from typing import Optional
from pathlib import Path
import pyhere

# Set pyhere
here = pyhere.here()


def prepare_dataset(
        source: str,
        dest: Optional[str] = None,
        force_download: bool = False
):
    """
    Prepare the dataset by either using a local zip file or downloading from a URL.

    Args:
        source (str): The URL or local path to the zip file.
        dest (str): The destination folder to save the files. If None, use pyhere.here('data', 'raw')
        force_download (bool): Whether to force download the files. If True, always download even if the files exist.

    Returns:
        Path: The path to the folder containing the files.

    """

    if dest is None:
        dest = Path(here, 'data', 'raw')
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)


    if is_url:
        filename = os.path.basename(source)
        local_path = dest_path / filename
        if not local_path.exists() or force_download:
            print(f"Downloading {source} to {local_path}")
            response = requests.get(source)
            response.raise_for_status() # Raise an exception if the response is not successful
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Using existing file at {local_path}")
    
    else:
        local_path = Path(source)
        if not local_path.exists():
            raise FileNotFoundError(f"File not found at {local_path}")
    

    # Extract the zip file
    extract_path = dest_path / local_path.stem
    if not extract_path.exists() or force_download:
        print(f"Extracting {local_path} to {extract_path}...")
        with zipfile.ZipFile(local_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    else:
        print(f"Files already extracted at {extract_path}")
    
    return extract_path


# Example Usage 
url = 'http://madm.dfki.de/files/sentinel/EuroSAT.zip'
local_file = '/path/to/local/EuroSAT.zip'

# Download from URL
path = prepare_dataset(url)

# Use local file
path = prepare_dataset(local_file)