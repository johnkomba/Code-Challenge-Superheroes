from models import db, Hero, Power, HeroPower
import random
from app import app
def seed_data():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    
    print("🦸‍♀️ Seeding powers...")
    
    powers = [
        { "name": "super strength", "description": "gives the wielder super-human strengths" },
        { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
        { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
        { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
    ]
    
    for power_dict in powers:
        power = Power(**power_dict)
        power.hero_id = random.randint(1,10)
        db.session.add(power)
        db.session.commit()

    print("🦸‍♀️ Seeding heroes...")
    
    heroes = [
        { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
        { "name": "Doreen Green", "super_name": "Squirrel Girl" },
        { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
        { "name": "Janet Van Dyne", "super_name": "The Wasp" },
        { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
        { "name": "Carol Danvers", "super_name": "Captain Marvel" },
        { "name": "Jean Grey", "super_name": "Dark Phoenix" },
        { "name": "Ororo Munroe", "super_name": "Storm" },
        { "name": "Kitty Pryde", "super_name": "Shadowcat" },
        { "name": "Elektra Natchios", "super_name": "Elektra" }
    ]
    
    for hero_dict in heroes:
        hero = Hero(**hero_dict)
        db.session.add(hero)
        db.session.commit()

    print("🦸‍♀️ Adding powers to heroes...")

    strengths = ["Strong", "Weak", "Average"]
    
    for _ in range(30):
        hero_power = HeroPower(
            strength = random.choice(strengths),
            hero_id = random.randint(1, 10),
            power_id = random.randint(1,4)
        )
        db.session.add(hero_power)
        db.session.commit()
    
    
    print("🦸‍♀️ Done seeding!")
    

if __name__ == "__main__":
    with app.app_context():
        seed_data()