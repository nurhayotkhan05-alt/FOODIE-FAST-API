from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Foodie Backend")


class Profile(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str = ""
    age: int | None = Field(default=None, ge=1, le=120)
    weight: float | None = Field(default=None, gt=0, le=500)
    height: float | None = Field(default=None, gt=0, le=260)
    language: Literal["uz", "ru", "en"] = "uz"
    theme: Literal["light", "dark"] = "light"


class Meal(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    calories: int = Field(ge=0, le=10000)
    protein: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)
    fat: float = Field(default=0, ge=0)


profile = Profile(name="Foydalanuvchi")
meals = []


@app.get("/")
async def home():
    return {"message": "Foodie backend ishlayapti"}


@app.get("/profile")
async def get_profile():
    return profile


@app.put("/profile")
async def update_profile(data: Profile):
    global profile
    profile = data
    return profile

@app.post("/meals",status_code=201)
async def get_meals(data: Meal):
    meal = {'id': str(uuid4()), **data.model_dump()}
    meals.append(meal)
    return meal


@app.delete("/meals/{id}")
async def delete_meal(id: str):
    for index, meal in enumerate(meals):
        if meal['id'] == id:
            return {'message': 'Taom o\'chirildi'}

        raise HTTPException(status_code=404, detail="Taom topilmadi!")


@app.get("/stats")
async def get_stats():
    return {
        "meal_count": len(meals),
        "calories": sum(meal["calories"] for meal in meals),
        "protein": sum(meal["protein"] for meal in meals),
        "carbs": sum(meal["carbs"] for meal in meals),
        "fat": sum(meal["fat"] for meal in meals)
    }

