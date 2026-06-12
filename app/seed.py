from app.database import SessionLocal
from app.models import Flower

db = SessionLocal()

if db.query(Flower).count() == 0:
    flowers = [
        Flower(name="Red Rose Bouquet", price=29.99, image="rose.png"),
        Flower(name="Sunflower Delight", price=24.99, image="sunflower.png"),
        Flower(name="White Lily", price=34.99, image="lily.png"),
        Flower(name="Pink Bouquet", price=39.99, image="bouquet.png"),
        Flower(name="Elegant Roses", price=44.99, image="hero.png"),
        Flower(name="Spring Blossom", price=27.99, image="bouquet.jpg"),
    ]

    db.add_all(flowers)
    db.commit()

db.close()