#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import sqlalchemy
import sqlalchemy.ext.declarative

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

engine = sqlalchemy.create_engine('sqlite:///hhg.sqlite')

Base = sqlalchemy.ext.declarative.declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Form(Base):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    hour = Column(Integer)
    weekday = Column(Integer)

    form_id = Column(Integer, ForeignKey('forms.id'))
    form = relationship("Form", backref=backref('lessons', order_by=id))

    room_id = Column(Integer, ForeignKey('rooms.id'))
    room = relationship("Room", backref=backref('lessons', order_by=id))

    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship("Subject", backref=backref('lessons', order_by=id))

    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", backref=backref('lessons', order_by=id))

Base.metadata.create_all(engine)
