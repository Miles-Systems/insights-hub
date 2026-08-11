from dataclasses import dataclass


@dataclass
class ExtractedPage:
    page_number: int
    text: str
