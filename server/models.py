from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Enum


db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<Donor {self.name}>'
    
class Organization(db.Model):
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    description = db.Column(db.String, nullable=False)
    website_url = db.Column(db.String, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    beneficiaries = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<Organization {self.name}>'
    
class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    transaction_id = db.Column(db.String(20), nullable=False)
    
    
    donor = db.relationship('Donor', backref='donations')
    organization = db.relationship('Organization', backref='donations')
    
    def __repr__(self):
        return f'<Donation {self.amount}>'
    
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.email}>'
    
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum('approved', 'rejected', 'pending', name='status'), nullable=False)
    
    def __repr__(self):
        return f'<Review {self.status}>'