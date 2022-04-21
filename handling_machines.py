import sqlite3
import smtplib
import os
from email.mime.multipart import MIMEMultipart
import datetime
import main
from werkzeug.utils import secure_filename
import handling_builder

conn = sqlite3.connect("database.db", check_same_thread = False)

def open_database():
  conn = sqlite3.connect("database.db", check_same_thread = False)


def print_all_machine_info():
  open_database()
  machine_info_orig = conn.execute("SELECT * FROM machine_request")

  for i in machine_info_orig:
    print("-- new machine thing --")
    for g in i:
      print(g)
      
def delete_machine_request_archived():
  open_database()
  conn.execute("DELETE FROM machine_request_archived")
  conn.commit()

def get_machineNames_used_by_id(request_id):
  open_database()
  # print_all_machine_info()

  machineNameOrig = conn.execute("SELECT m.machine_name FROM machine m, machine_request c WHERE c.request_id_ = " + str(request_id) + " and c.machine_id_ = m.machine_id").fetchall()

  returned = []
  for i in machineNameOrig:
    for g in i:
      print("yesss: " + i[0])
      returned.append(i[0])

  return returned

def finish_machines(request_id):
  open_database()

  conn.execute("DELETE FROM machine_request WHERE request_id_ = " + str(request_id))

  # put into archived.

  conn.commit()

  
def make_machine_request(request_id, machine_id):
  open_database()

  params = (request_id, machine_id)

  conn.execute("INSERT INTO machine_request (request_id_, machine_id_) values(?, ?)", params)

  conn.commit()

def get_machine_id_from_name(machine_name):
  # print("machine name: " + machine_name)
  open_database()
  returned = conn.execute("SELECT machine_id FROM machine WHERE machine_name = \"" + machine_name + "\"").fetchone()[0]


  return int(returned)

def add_machine(machine_name, machine_desc):
  open_database()
  # add a page for each machine created.
  params = (machine_name, machine_desc)

  conn.execute("INSERT INTO machine values (NULL, ?, ?)", params)

  conn.commit()

def remove_machine(machine_name):
  open_database()
  try:
    conn.execute("DELETE FROM machine WHERE machine_name = \"" + str(machine_name) + "\"")
    print("deleted: " + machine_name)
  except:
    print("this machine does not exist!")
  conn.commit()

def get_all_machine_info():
  open_database()

  thing = conn.execute("SELECT * FROM machine").fetchall()

  for i in thing:
    print(i)
  return thing

def get_all_machine_names():
  open_database()

  thing = conn.execute("SELECT machine_name FROM machine").fetchall()

  returned = []
  for i in thing:
    returned.append(''.join(i))
  return returned

def get_all_machine_descriptions():
  open_database()

  thing = conn.execute("SELECT machine_desc FROM machine").fetchall()
  returned = []
  for i in thing:
    returned.append(''.join(i))
  return returned
  
def get_all_used_machines(request_id):

  open_database()
  thing = conn.execute("SELECT machine_name FROM machine m, machine_request c, request r WHERE m.machine_id = c.machine_id_ and c.request_id_ = r.request_id and r.request_id = " + str(request_id))
  returned = []

  for i in thing:
    for g in i:
      returned.append(g)
  
  return returned

def delete_all_machine_requests():
  open_database()
  conn.execute("DELETE FROM machine_request")
  conn.commit()
  
def get_machineNames_used_by_archived_id(request_id):
  open_database()
  # print_all_machine_info()

  machineNameOrig = conn.execute("SELECT m.machine_name FROM machine m, machine_request_archived c WHERE c.request_id_ = " + str(request_id) + " and c.machine_id_ = m.machine_id").fetchall()

  returned = []
  for i in machineNameOrig:
    for g in i:
      print("yesss: " + i[0])
      returned.append(i[0])

  return returned


def alter_machines(request_id, machine_id_list, machineListInfo):
  open_database()
  # alter the machines for a specific request.
  conn.execute("DELETE FROM machine_request WHERE request_id_ = " + str(request_id))
  # conn.commit()

  open_database() # need to reopen database after commit

  print("yessa")
  print(machine_id_list)
  print(machineListInfo)

  for i in range(len(machine_id_list)):
    isUsed = machineListInfo[i]
    print("ISUSED: " + str(isUsed))
    machine_id = machine_id_list[i]
    # print("machine id: " + str(machine_id))
    if (isUsed):
      print("Inserted")
      params = (request_id, machine_id)
      print("params")
      print(params)
      conn.execute("INSERT INTO machine_request values(NULL, ?, ?)", params)
      conn.commit()

  conn.commit()

    