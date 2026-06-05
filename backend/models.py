from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class MealCategory(str, Enum):
    SOUP = "soup"
    MAIN = "main"
    DESSERT = "dessert"
    DRINK = "drink"


class Meal(BaseModel):
    id: int
    name: str
    category: MealCategory
    price: float = Field(ge=0, description="Ціна не може бути від'ємною")
    description: Optional[str] = None


class CreateMealRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: MealCategory
    price: float = Field(ge=0, le=1000)
    description: Optional[str] = None


class OrderItem(BaseModel):
    meal_id: int
    quantity: int = Field(ge=1, le=10)


class OrderResponse(BaseModel):
    items: list[OrderItem]
    total_price: float
    message: str