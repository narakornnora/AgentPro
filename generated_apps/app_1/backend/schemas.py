from pydantic import BaseModel
from typing import Optional

class CoffeeIn(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None

class CoffeeOut(CoffeeIn):
    id: int

class OrderIn(BaseModel):
    user_id: Optional[int] = None
    coffee_ids: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None

class OrderOut(OrderIn):
    id: int

class LocationIn(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    coordinates: Optional[str] = None

class LocationOut(LocationIn):
    id: int

