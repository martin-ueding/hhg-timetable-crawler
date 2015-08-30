#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

import argparse
import itertools
import os
import re
import sys

import requests
import lxml.etree
from sqlalchemy.orm import sessionmaker

from model import *

Session = sessionmaker(bind=engine)
session = Session()

base = 'http://stundenplan.hhg-bonn.de/klassen/'

url_forms = 'http://stundenplan.hhg-bonn.de/klassen/stundenplanklassen.htm'
url_teachers = 'http://stundenplan.hhg-bonn.de/lehrer/stundenplanlehrer.htm'


def get_url(url, user, password):
    cache = os.path.basename(url)
    if not os.path.isfile(cache):
        r = requests.get(url, auth=(user, password))
        with open(cache, 'w') as f:
            f.write(r.text)

    with open(cache) as f:
        text = f.read()

    return text

def parse_form(form_str, text):
    form = session.query(Form).filter(Form.name == form_str).scalar()
    if form is None:
        form = Form(name=form_str)
        session.add(form)

    parser = lxml.etree.HTMLParser()
    root = lxml.etree.fromstring(text, parser)

    table = root.findall('.//table')[1]
    rows = table.findall('tr')

    hour = 0

    #print(rows)

    for row in rows:
        cells = row.findall('td')
        #print(cells)

        if len(cells) == 0:
            print('Skip empty row')
            continue

        for day, cell in zip(itertools.count(), cells):
            subtable = cell.find('table')
            #print(subtable)

            sub_rows = subtable.findall('tr')
            #print(sub_rows)
            for sub_row in sub_rows:
                sub_words = [x.text for x in sub_row.findall('.//b')]

                if day == 0:
                    if len(sub_words) == 1:
                        hour = sub_words[0]
                else:
                    print(day, hour, sub_words)

                    if len(sub_words) == 3:
                        subject_str, teacher_str, room_str = sub_words

                        subject = session.query(Subject).filter(Subject.name == subject_str).scalar()
                        if subject is None:
                            subject = Subject(name=subject_str)
                            session.add(subject)

                        teacher = session.query(Teacher).filter(Teacher.name == teacher_str).scalar()
                        if teacher is None:
                            teacher = Teacher(name=teacher_str)
                            session.add(teacher)

                        room = session.query(Room).filter(Room.name == room_str).scalar()
                        if room is None:
                            room = Room(name=room_str)
                            session.add(room)

                        lesson = Lesson(hour=hour, weekday=day, room=room, subject=subject, teacher=teacher, form=form)


                        session.commit()


    #print(lxml.etree.tostring(table, pretty_print=True, method='html').decode())

    sys.exit(0)

def main():
    options = _parse_args()

    text = get_url(url_forms, options.user, options.password)

    parser = lxml.etree.HTMLParser()
    root = lxml.etree.fromstring(text, parser)

    form_pattern = re.compile(r'stundenplanklassen_0?(\d+\w?).htm')

    table = root.findall('.//table')[1]
    urls = table.findall('.//a')

    for url in urls:
        href = url.get('href')

        full_url = base + href
        print(full_url)

        m = form_pattern.match(href)

        text = get_url(full_url, options.user, options.password)
        parse_form(m.group(1), text)




def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('user')
    parser.add_argument('password')
    options = parser.parse_args()

    return options

if __name__ == '__main__':
    main()
