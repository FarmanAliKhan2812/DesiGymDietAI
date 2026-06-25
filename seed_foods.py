from database.database import engine, SessionLocal
from models.food import Base, Food
from models.daily_log import DailyLog

Base.metadata.create_all(bind=engine)

db = SessionLocal()

foods = [
    ("Egg", "1 piece", 6),
    ("Milk", "1 glass", 8),
    ("Chicken", "100g", 27),
    ("Beef", "100g", 26),
    ("Fish", "100g", 22),
    ("Daal", "1 bowl", 9),
    ("Yogurt", "1 cup", 10),
    ("Chana", "1 bowl", 15),
    ("Chapati", "1 piece", 3),
    ("Rice", "1 cup", 4),
    ("Paneer", "100g", 18),
    ("Peanut Butter", "2 tbsp", 8),
    ("Banana Shake", "1 glass", 10),
    ("Mango Shake", "1 glass", 10),
    ("Oats", "1 bowl", 13)
]

for name, unit, protein in foods:
    food = Food(
        name=name,
        unit=unit,
        protein=protein
    )
    db.add(food)

db.commit()

print("Foods added successfully!")