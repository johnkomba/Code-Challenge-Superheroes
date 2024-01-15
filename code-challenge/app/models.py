# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

class Power(db.Model):
    __tablename__ = 'power'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')

    # Validation for the description attribute
    @validates("description")
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_power'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    
    # Validation for the strength attribute
    @validates("strength")
    def validate_strength(self, key, strength):
        strengths = ["Strong", "Weak", "Average"]
        
        if not any(substr in strength for substr in strengths):
            raise ValueError("Strength must be one of the following values: Strong, Weak, Average")
        return strength
