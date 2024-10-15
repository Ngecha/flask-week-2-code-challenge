from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData()
# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes' 
    
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column(db.String)  
    number = db.Column(db.Integer)  
    
    # Relationship to the Appearance model (One-to-many relationship)
    appearance = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    
    # Prevent circular serialization
    serialize_rules = ('-appearance.episode',)
    
    # Representation
    def __repr__(self):
        return f'<Episode {self.id}, number {self.number} of {self.date}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'  
    
    serialize_rules = ('-guest.appearance', '-episode.appearance')

    id = db.Column(db.Integer, primary_key=True)  
    rating = db.Column(db.Integer) 
    
    # Relationships
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    # Validator for the rating column to ensure ratings are between 1 and 5
    @validates('rating')
    def validate_rating(self, key, value):
        ratings = range(0, 6)
        if value not in ratings:
            raise ValueError('Must be from 1 to 5')
        return value

    # Representation
    def __repr__(self):
        return f'<{self.id} appearance of {self.rating} rating on {self.episode_id}, with {self.guest_id}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'  
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String)  
    occupation = db.Column(db.String)  
    
    # Relationship to the Appearance model (One-to-many relationship)
    appearance = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')
    
    # Prevent circular serialization
    serialize_rules = ('-appearance.guest',)
    
    # Representation
    def __repr__(self):
        return f'<guest {self.id}, name: {self.name}, occupation: {self.occupation}>'
