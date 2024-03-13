#!/usr/bin/env python3
from . import db
from datetime import datetime

class Recepten(db.Model):
    __tablename__ = "Recepten"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(8), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    titel = db.Column(db.String(200), nullable=False)        
    recept = db.Column(db.String(2000), nullable=False)
    tags = db.Column(db.String(150))
    time_created = db.Column(db.DateTime, nullable=False)
    last_edit = db.Column(db.DateTime, index=False)