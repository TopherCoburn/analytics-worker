# utils.py
import json
import logging
import os
import time
from typing import Dict, List

logging.basicConfig(level=logging.INFO)

def load_json(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to load JSON from file {file_path}: {e}")
        return {}
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found")
        return {}

def save_json(data: Dict, file_path: str):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.error(f"Failed to save JSON to file {file_path}: {e}")

def get_timestamp() -> int:
    return int(time.time())

def get_current_directory() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def get_current_script_path() -> str:
    return os.path.abspath(__file__)

def flatten_list(nested_list: List[List]) -> List:
    return [item for sublist in nested_list for item in sublist]