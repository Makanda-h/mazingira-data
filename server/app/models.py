from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum('donor', 'admin', 'organization', name='user_roles'), nullable=False)
    
    donations = relationship('Donation', back_populates='user')
    organizations = relationship('Organization', back_populates='admin')

    def __init__(self, username, password, email, role):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return f'<User {self.username}>' 

class Organization(db.Model, SerializerMixin):
    __tablename__ = 'organizations'
    
    serialize_rules = ('-donations.organization', '-stories.organization')
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    approved = Column(Boolean, default=False)
    status = Column(Enum('pending', 'approved', 'rejected', name='organization_status'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    
    donations = relationship('Donation', back_populates='organization')
    stories = relationship('Story', back_populates='organization')

    def __repr__(self):
        return f'<Organization {self.name}>'

class Donation(db.Model, SerializerMixin):
    __tablename__ = 'donations'
    
    serialize_rules = ('-user.donations', '-organization.donations')
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    amount = Column(Float, nullable=False)
    recurring = Column(Boolean, default=False)
    recurrence_interval = Column(Enum('weekly', 'monthly', 'yearly', name='recurrence_intervals'), nullable=True)
    next_payment_date = Column(DateTime, nullable=True)
    payment_method = Column(Enum('paypal', 'stripe', 'mpesa', 'credit_card', 'bank_transfer', name='payment_methods'), nullable=False)
    is_anonymous = Column(Boolean, default=False)
    
    user = relationship('User', back_populates='donations')
    organization = relationship('Organization', back_populates='donations')

    def __repr__(self):
        return f'<Donation {self.amount}>'

class Story(db.Model, SerializerMixin):
    __tablename__ = 'stories'
    
    serialize_rules = ('-organization.stories',)
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    
    organization = relationship('Organization', back_populates='stories')

    def __repr__(self):
        return f'<Story {self.title}>'