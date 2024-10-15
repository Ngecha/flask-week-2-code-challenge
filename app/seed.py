from faker import Faker
import random

from app import app

from models import Episode,Appearance,Guest,db

with app.app_context():
    faker=Faker()
    
    Episode.query.delete()
    Appearance.query.delete()
    Guest.query.delete()
    
    episodes=[]
    appearances=[]
    guests=[]

    
    for n in range(10):
        episode=Episode(date=faker.date(), number=random.randint(1,10))
        episodes.append(episode)
        
        guest=Guest(name=faker.name(), occupation=faker.job())
        guests.append(guest)
        
        appearance=Appearance(rating=random.randint(1, 5),episode_id=random.randint(1,10), guest_id=random.randint(1,10))
        appearances.append(appearance)
        
        
        
        
        
    db.session.add_all(episodes)
    db.session.add_all(guests)
    db.session.add_all(appearances)
    
    db.session.commit()
    
    
    