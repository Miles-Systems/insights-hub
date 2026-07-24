from dataclasses import dataclass


@dataclass
class StoredFile:
    storage_path: str
    original_filename: str
    stored_filename: str
    file_size: int
    mime_type: str
