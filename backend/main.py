from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="Lunch Roulette API",
    description="API для вибору обіду з випадковим вибором страви",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Lunch Roulette API", "docs": "/docs"}


@app.get("/api/v1/stats")
async def get_stats():
    from routes import meals_db
    categories = {}
    for meal in meals_db:
        cat = meal.category.value
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_meals": len(meals_db),
        "categories": categories,
        "price_range": {
            "min": min(m.price for m in meals_db),
            "max": max(m.price for m in meals_db)
        }
    }