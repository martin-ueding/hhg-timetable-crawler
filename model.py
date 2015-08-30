#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import sqlalchemy
import sqlalchemy.ext.declarative

from sqlalchemy import Column, Integer, String

engine = sqlalchemy.create_engine('sqlite:///hhg.sqlite', echo=True)

Base = sqlalchemy.ext.declarative.declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    room = relationship("Room", backref=backref('lessons', order_by=id))
    subject = relationship("Subject", backref=backref('lessons', order_by=id))
    teacher = relationship("Teacher", backref=backref('lessons', order_by=id))
