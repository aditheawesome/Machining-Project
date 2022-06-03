import sqlite3
from SQLStatements import *
import random

from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect("database.db", check_same_thread=False)


def open_database():
    conn = sqlite3.connect("database.db", check_same_thread=False)


# Utility functions
def delete_builder(builder_email):
    open_database()
    conn.execute("DELETE FROM builder WHERE email_address = ?", (builder_email, ))
    conn.execute("DELETE FROM User WHERE email = ?", (builder_email, ))
    conn.commit()
    conn.close()


def delete_all_builders():  # uh... don't put self-destruct buttons in code
    open_database()
    conn.execute("DELETE FROM builder")
    conn.execute("DELETE FROM User")
    conn.commit()


def delete_all_builders_except_ben():
    open_database()
    conn.execute("DELETE FROM builder WHERE email != \"25benjaminli@gmail.com\"")
    conn.commit()


def print_all_builders():
    open_database()
    thing = conn.execute("SELECT * FROM builder")
    for i in thing:
        print("--- starting new builder ---")
        for g in i:
            print(g)


def get_builder_id(builder_email):
    open_database()
    thing = conn.execute("SELECT builder_id FROM builder WHERE email_address = ?", (builder_email, ))
    returned_email = ""

    for i in thing:
        for g in i:
            returned_email = g

    return returned_email


def check_builder(builder_email):
    open_database()
    print(builder_email)
    builder_isapproved = conn.execute(
        "SELECT isapproved, builder_id FROM builder WHERE email_address = ?", (builder_email, ))
    otherthinglist = []
    print_all_builders()
    print("it is.. " + str(builder_isapproved))

    for i in builder_isapproved:
        print(i)
        for g in i:
            otherthinglist.append(g)

    if not otherthinglist:
        print("no builder found")
        otherthinglist = [False, None]  # no builder is found

    other_thing = otherthinglist[0]

    print("isapproved: " + str(other_thing))

    if (other_thing == 1):
        return [True, otherthinglist[1]]
    else:
        return [False, otherthinglist[1]]


"""
Modification functions (insert, delete, update, etc.)
"""


def getunapproved():
    open_database()
    builderarr = conn.execute("SELECT name_, email_address from builder WHERE isapproved = 0")
    return builderarr


def find(builder_email):
    open_database()

    thing = conn.execute("SELECT COUNT(builder_id) FROM builder WHERE email_address = ?", (builder_email, ))

    numofoccurrences = 0
    for i in thing:
        for g in i:
            numofoccurrences = g

    # print("occurrences: " + str(numofoccurrences))
    if (numofoccurrences == 0):  # make sure no pre-existing builders with the same email
        return False

    print("occurrences: " + str(numofoccurrences))
    return True


def add_builder(builder_email, builder_name, password):
    open_database()

    params = (builder_name, builder_email, password, 0)
    thing = conn.execute("SELECT COUNT(builder_id) FROM builder WHERE email_address = ?", (builder_email, ))
    print("brobro")
    print(params)

    numofoccurrences = 0
    for i in thing:
        for g in i:
            numofoccurrences = g

    print("occurrences: " + str(numofoccurrences))
    if (numofoccurrences == 0):  # make sure no pre-existing builders with the same email
        conn.execute("INSERT INTO builder VALUES (NULL, ?, ?, ?, ?)", params)

    conn.commit()


def approve_builder(builder_email):
    open_database()
    print("approving!")
    conn.execute("UPDATE builder SET isapproved = 1 WHERE builder_id = ?", ((get_builder_id(builder_email)), ))
    conn.commit()


def unapprove_builder(builder_email):
    open_database()
    print("unapproving!")
    conn.execute("UPDATE builder SET isapproved = 0 WHERE builder_id = ?", (get_builder_id(builder_email), ))
    conn.commit()


def add_and_approve(builder_email, builder_name, password):
    open_database()

    ps = generate_password_hash(password, method="sha256")

    add_builder(builder_email, builder_name, ps)

    approve_builder(builder_email)


def get_hashed_pass(id):
    open_database()

    thing = conn.execute("SELECT pswd FROM builder WHERE builder_id = ?", (id, ))
    returned = ""
    for i in thing:
        for g in i:
            returned = g

    print("returned: " + returned)

    return returned


def finish_task(request_id):
    open_database()
    conn.execute("UPDATE request SET is_completed = 1 WHERE request_id = ?", (request_id, ))
    conn.commit()


def close_database():
    conn.commit()
    conn.close()