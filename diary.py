#!/usr/bin/env python3

from collections import OrderedDict
import datetime as dt
import os
import sys
import time

from peewee import *

db = SqliteDatabase('fordiary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateField(default=dt.datetime.now)

    class Meta:
        database = db


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the Menu."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add Entry."""
    print("Start writing. Press 'CTRL + D' on a new line when finished")
    data = sys.stdin.read().strip()

    if data:
        clear()
        if input("Save? [Y][N] > ").lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully")
            time.sleep(2)
            clear()

def view_entries(search_query = None):
    """View Entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        if search_query:
            if len(entries) >= 1:
                clear()
                timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%m%p')
                print(timestamp)
                print('='*len(timestamp))
                print(entry.content)
                print('\n\n' + '='*len(timestamp)
                print("[N] for next entry, [Q] to quit to main menu, [D] to delete entry.")

                next_action = input("Action >[Q,D,N] ".lower().strip())
                if next_action == 'q':
                    break
                elif next_action == 'd':
                    delete_entry(entry)
            elif len(entries) == 1:
                clear()
                timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%m%p')
                print('Only one entry matched that search.')
                print(timestamp)
                print('='*len(timestamp))
                print(entry.content)
                print('\n\n' + '='*len(timestamp)
                print("[Q] to quit to main menu, [D] to delete entry.")

                next_action = input("Action > [Q,D] ".lower().strip())
                if next_action != 'd':
                    break
                else:
                    delete_entry(entry)
                    break
            else:
                print('\n\n' + '='*len(timestamp)
                print('No results found')
                time.sleep(2.5)
                clear()
                break
        else:
            timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%m%p')
            print(timestamp)
            print('='*len(timestamp))
            print(entry.content)
            print('\n\n' + '='*len(timestamp)
            print("[N] for next entry, [Q] to quit to main menu, [D] to delete entry.")

            next_action = input("Action >[Q,D,N] ".lower().strip())
            if next_action == 'q':
                time.sleep(.2)
                break
            elif next_action == 'd':
                delete_entry(entry)

def search_entries():
    """Search your Diary for a word or phrase"""
    view_entries(input("Search for >___"))

def delete_entry(entry):
    """Delete An Entry."""
    if input("Are you sure? [Y or N]".lower().strip()) == 'y':
        entry.delete_instance()
        print("Deleted")
        time.sleep(2)
        clear()

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ('d', delete_entry)
])

if __name__ == "__main__":
    initialize()
    menu_loop()
