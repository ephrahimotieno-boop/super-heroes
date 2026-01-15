from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Episode model represents a TV episode
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship: An Episode has many Appearances. 
    # 'cascade' ensures that if an episode is deleted, all its appearances are also deleted.
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    
    # SerializerMixin Rules:
    # We exclude 'episode' from the nested appearances to prevent infinite recursion
    # when an Episode is serialized.
    serialize_rules = ('-appearances.episode',)

# Guest model represents a person appearing on the show
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # Relationship: A Guest has many Appearances.
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    
    # Similarly, exclude the 'guest' field from nested appearances to prevent recursion.
    serialize_rules = ('-appearances.guest',)

# Appearance represents the join table between Guest and Episode
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    # Foreign keys link this appearance to a specific episode and guest
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Relationships linking back to the major models
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Rules to prevent recursion when serializing an Appearance object
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    
    # Validation: Ensures the rating is always between 1 and 5.
    # This is triggered automatically whenever a rating is set.
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating