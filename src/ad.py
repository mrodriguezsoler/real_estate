from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Ad:
    id: str

    property_type: Optional[str]
    description: Optional[str]
    agency: Optional[str]
    price: Optional[int]

    surface: Optional[int]
    rooms: Optional[int]
    baths: Optional[int]
    extra_features: Optional[List[str]]

    city: Optional[str]
    city_zone: Optional[str]
    street: Optional[str]
    zip_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    url: Optional[str]