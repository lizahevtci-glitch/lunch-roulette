from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Meal, CreateMealRequest, OrderItem, OrderResponse

router = APIRouter()


meals_db = [
    Meal(id=1, name="Борщ", category="soup", price=45.0, description="Класичний український борщ"),
    Meal(id=2, name="Гречка з котлетою", category="main", price=65.0),
    Meal(id=3, name="Чізкейк", category="dessert", price=35.0, description="Ніжний десерт"),
    Meal(id=4, name="Компот", category="drink", price=15.0),
    Meal(id=5, name="Піца Маргарита", category="main", price=85.0),
    Meal(id=6, name="Салат Цезар", category="main", price=55.0),
]


@router.get("/meals", response_model=List[Meal])
async def get_all_meals():
    """Повертає список всіх страв"""
    return meals_db


@router.get("/meals/{meal_id}", response_model=Meal)
async def get_meal_by_id(meal_id: int):
    """Повертає страву за ID"""
    for meal in meals_db:
        if meal.id == meal_id:
            return meal
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Страву з ID {meal_id} не знайдено"
    )


@router.get("/random-meal")
async def get_random_meal():
    """Повертає випадкову страву"""
    import random
    return random.choice(meals_db)

@router.post("/meals", status_code=status.HTTP_201_CREATED)
async def create_meal(meal: CreateMealRequest):
    """Додає нову страву в меню"""
    new_id = max([m.id for m in meals_db]) + 1 if meals_db else 1
    new_meal = Meal(id=new_id, **meal.model_dump())
    meals_db.append(new_meal)
    return new_meal


@router.delete("/meals/{meal_id}")
async def delete_meal(meal_id: int):
    """Видаляє страву з меню"""
    for i, meal in enumerate(meals_db):
        if meal.id == meal_id:
            deleted = meals_db.pop(i)
            return {"message": f"Страву '{deleted.name}' видалено", "deleted_id": meal_id}
    raise HTTPException(status_code=404, detail="Страву не знайдено")


@router.post("/calculate-order", response_model=OrderResponse)
async def calculate_order(order_items: List[OrderItem]):
    """Розраховує загальну вартість замовлення"""
    total = 0
    items_detail = []
    
    for item in order_items:
        meal = await get_meal_by_id(item.meal_id)
        total += meal.price * item.quantity
        items_detail.append(f"{meal.name} x{item.quantity}")
    
    return OrderResponse(
        items=order_items,
        total_price=round(total, 2),
        message=f"Ви замовили: {', '.join(items_detail)}. Загальна сума: {total} грн"
    )