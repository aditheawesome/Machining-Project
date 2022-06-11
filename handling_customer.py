import re
import sqlite3
import smtplib
import os
from email.mime.multipart import MIMEMultipart
import datetime
import main
from werkzeug.utils import secure_filename
import handling_builder
import handling_machines
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

conn = sqlite3.connect("database.db", check_same_thread = False)

def open_database():
  conn = sqlite3.connect("database.db", check_same_thread = False)


def print_all_customers():
  open_database()
  thing = conn.execute("SELECT * from customer")
  for i in thing:
    print("--- starting new customer ---")
    for g in i:
      print(g)

def delete_all_customers():
  open_database()
  conn.execute("DELETE FROM customer")
  conn.commit()

def customerCreate(customer_email, customer_name):
  open_database()
  
  numofoccurrences = conn.execute("SELECT COUNT(customer_id) FROM customer WHERE email_address = ?", (customer_email, )).fetchone()[0] 
  
  print("thing::" + str(numofoccurrences))


  if (numofoccurrences == 0): #make sure no pre-existing
    conn.execute("INSERT INTO customer (name_, email_address) values(?, ?)", (customer_name, customer_email))
  else:
    print("customer already exists what are you doing lmao. Updated name to " + customer_name)
    conn.execute("UPDATE customer SET name_ = ? WHERE email_address = ?", (customer_name, customer_email))
  conn.commit()


def print_all_requests():
  open_database()
  thing = conn.execute("SELECT * FROM request")
  for i in thing:
    print("--- starting new request ---")
    for g in i:
      print(g)

def customer_make_request_deprecated_2(customer_id, due_date, description):
  open_database()
  request_ids = conn.execute("SELECT request_id FROM request_archived") #gets all ARCHIVED request ids so it is consistent. 
  request_ids_orig = conn.execute("SELECT request_id FROM request")

  request_id_list = []
  request_ids_orig_list = []
  for i in request_ids:
    for g in i:
      request_id_list.append(g)
  
  for i in request_ids_orig:
    for g in i:
      request_ids_orig_list.append(g)

  if len(request_ids_orig_list) == 0:
    # make it match up with archived
    try:
      curr_request = max(request_id_list) # get the current request number
    except:
      curr_request = 0
  else:
    try:
      curr_request = max(request_ids_orig_list)
    except:
      curr_request = 0

  curr_request += 1

  params = (curr_request, customer_id, due_date, description, 0)
  
  conn.execute("INSERT INTO request values (?, ?, ?, ?, ?)", params)

  conn.commit()

  return curr_request #get the request id that was just inserted


# includes adding machines.
def customer_make_request(customer_id, due_date, description):
  open_database()
  request_ids = conn.execute("SELECT request_id FROM request_archived") #gets all ARCHIVED request ids so it is consistent. 

  request_ids_orig = conn.execute("SELECT request_id FROM request")
  request_id_list = []
  request_ids_orig_list = []

  # get all request ids, which are ARCHIVED
  for i in request_ids:
    for g in i:
      request_id_list.append(g)

  # get all request ids, which are REGULAR
  for i in request_ids_orig:
    for g in i:
      request_ids_orig_list.append(g)
  
  
  if len(request_ids_orig_list) == 0:
    # make it match up with archived
    try:
      curr_request = max(request_id_list) # get the current request number
    except:
      curr_request = 0
  else:
    try:
      curr_request = max(request_ids_orig_list)
    except:
      curr_request = 0

  curr_request += 1

  
  params = (curr_request, customer_id, due_date, description, 0, 0)

  
  conn.execute("INSERT INTO request values (?, ?, ?, ?, ?, ?)", params)

  conn.commit()

  return curr_request #get the request id that was just inserted

def get_customer_id(customer_email):
  open_database()
  thing = conn.execute("SELECT customer_id FROM customer WHERE email_address = ?", (customer_email, ))
  for i in thing:
    for g in i:
      return g

def delete_request(id):
  open_database()
  conn.execute("DELETE FROM request WHERE request_id = ?", (id, ))
  conn.commit()

def close_database():
  conn.commit()
  conn.close()

def delete_all_requests():
  open_database()
  conn.execute("DELETE FROM request")
  conn.commit()

def get_all_requests():
  open_database()
  # without if they are completed.
  thing = conn.execute("SELECT request_id, due_date, description_ FROM request")

  return thing

def get_emails_from_request():
  open_database()
  emails = []

  ids_sql = conn.execute("SELECT customer_id_ FROM request")
  ids = []
  for i in ids_sql:
    for g in i:
      ids.append(g)

  for i in ids:
    thing_sql = conn.execute("SELECT email_address FROM customer WHERE customer_id = ?", (i, ))
    for i in thing_sql:
      for g in i:
        emails.append(g)

  return emails

def get_request_ids():
  open_database()
  ids = conn.execute("SELECT request_id FROM request") 
  ids_returned = []
  for i in ids:
    for g in i:
      ids_returned.append(g)
  return ids_returned

def get_email_from_request(request_id):
  open_database()
  print("req id: " + str(request_id))
  # email_sql = conn.execute("SELECT c.email_address FROM customer c, request r WHERE r.customer_id_ = c.customer_id AND r.request_id = " + str(request_id)).fetchall()[0]
  cust_id = conn.execute("SELECT r.customer_id_ from request r, customer c WHERE r.customer_id_ = c.customer_id and r.request_id = ?", (request_id, )).fetchall()[0][0]
  print("cust id: " + str(cust_id))
  email_sql = conn.execute("SELECT email_address FROM customer WHERE customer_id = ?", (cust_id, )).fetchall()[0][0] 
  
  print("email sql: " + email_sql)

  return email_sql

def message(subject="Python Notification", 
            text="", img=None,
            attachment=None):
    
    # build message contents
    msg = MIMEMultipart()
      
    msg['Subject'] = subject  
    body = text + "\nThanks for using our service!"
    msg.attach(MIMEText(body))  
  

    if img is not None:
          
        # Check whether we have the lists of images or not!
        if type(img) is not list:  
            img = [img] 
  
        # Now iterate through our list
        for one_img in img:
            
              # read the image binary data
            img_data = open(one_img, 'rb').read()  
            # Attach the image data to MIMEMultipart
            # using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data,
                                 name=os.path.basename(one_img)))
  
    if attachment is not None:
          
        # lists of attachments or not!
        if type(attachment) is not list:
            attachment = [attachment]  
  
        for one_attachment in attachment:
  
            with open(one_attachment, 'rb') as f:
                
                # Read in the attachment
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            file['Content-Disposition'] = f'attachment;\
            filename="{os.path.basename(one_attachment)}"'
              
            msg.attach(file)
    return msg
  
def send_email(receiving_email, subject, body):
  open_database()
  #id, mFrom ('machining.millburn.org') <-- not configed yet!, mTo, mSubject, mBody, email_sent (if it has been sent)
  sender_email = "mhsmachining@gmail.com" #email that is the sender
  password = "eybrmybwvmhyuvbq"

  open_database()
  print('asdf')
  
  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    print('logging in')
    server.login(sender_email, password)
    msg = message(subject, body)
    print("body: " + body)
    # print("message: " + msg)
    server.sendmail(from_addr="mhsmachining@gmail.com",
              to_addrs=receiving_email, msg=msg.as_string())
    # delete_emails() #use datetime to track individual send times
    server.quit() 

  return 0

# send_email("25benjaminli@gmail.com", "tester", "body")
def delete_emails():
  #delete emails, not in use rn
  open_database()
  emails_to_be_deleted = conn.execute("DELETE FROM emails WHERE email_sent = 1") #if the email that is sent is finished.
  conn.commit()

def get_description(id):
  #get description associated with a request
  open_database()
  desc_sql = conn.execute("SELECT description_ FROM request WHERE request_id = ?", (id, ))
  desc_returned = ""
  for i in desc_sql:
    for g in i:
      desc_returned = g
  return desc_returned

def print_all_archived_machine_reqs():
  open_database()
  thing_sql = conn.execute("SELECT * FROM machine_request_archived")
  thing = []
  for i in desc_sql:
    for g in i:
      thing.append(g)
  return thing

def finish_request(request_id):
  #delete the request when finished.
  open_database()
  # delete_all_archived_requests()
  conn.execute("UPDATE request SET is_completed = 1 WHERE request_id = ?", (request_id, ))
  conn.commit()
  idk = conn.execute("SELECT customer_id_, due_date, description_, is_completed FROM request WHERE request_id = ?", (request_id, ))

  thing = []

  for i in idk:
    for g in i:
      thing.append(g)

  
  stuff = conn.execute("INSERT INTO request_archived values (NULL, ?, ?, ?, ?)", thing)

  # tbd: delete all associated machines, insert into machine_request_archived
  what = handling_machines.get_machineNames_used_by_id(request_id)

  machine_ids = []

  print("----------PRINTING INFO first --------------")
  handling_machines.print_all_machine_info()

  # deleting machine request, put machine request into archived table.

  for i in what:
    mach_id = handling_machines.get_machine_id_from_name(i)
    conn.execute("INSERT INTO machine_request_archived values (NULL, ?, ?)", (request_id, mach_id))

    conn.execute("DELETE FROM machine_request WHERE request_id_ = ?", (request_id, ))
    
    conn.commit()

  # print("----------PRINTING INFO--------------")
  # print_all_machine_info()
  delete_file(request_id)

  conn.execute("DELETE FROM request WHERE request_id = ?", (request_id, ))

  conn.commit()

def reset_id_counter():
  open_database()  
  conn.execute("UPDATE `sqlite_sequence` SET `seq` = 0 WHERE `name` = 'machine_request'")
  conn.commit()


def delete_file(request_id):
  # remove associated files.
  for filename in os.listdir(main.app.config['UPLOAD_FOLDER']):
    if filename != "donotdelete.txt":
      split_tup = os.path.splitext(filename)
      file_name = split_tup[0] # this is the file_name of the ORIGINAL
      file_ending = split_tup[1] #file ending of the ORIGINAL
      num = get_file_num(filename)
      print("num: " + str(num))
      if int(num) == int(request_id):
        os.remove(os.path.join(main.app.config['UPLOAD_FOLDER'], filename))

    
def update_desc(request_id, new_desc):
  open_database()
  conn.execute("UPDATE request SET description_ = ? WHERE request_id = ?", (new_desc, request_id))
  conn.commit()
  
def delete_all_archived_requests():
  open_database()
  conn.execute("DELETE FROM request_archived")
  conn.commit()

# def create_archived_request(request_id):
#   open_database()
  
#   stuff = conn.execute("INSERT INTO request_archived values (NULL, ?, ?, ?, ?)", thing)
def print_archived_requests():
  open_database()
  why_am_i_still_here = conn.execute("SELECT * FROM request_archived")
  thing = []
  for i in why_am_i_still_here:
    print("---- starting new archived request ----")
    for g in i:
      print(g)
  # return thing 
def get_customer_id_by_request(request_id):
  #get the customer id that is associated with a request
  open_database()
  id_thing = conn.execute("SELECT customer_id_ FROM request where request_id = ?", (request_id, )).fetchone()[0]

  print("customer id is " + str(id_thing))
  return id_thing

def get_name_from_request(request_id): #NOT included in request table
  open_database()
  customer_id = get_customer_id_by_request(request_id)
  name = conn.execute("SELECT name_ from customer WHERE customer_id = ?", (customer_id, )).fetchone()[0]
  
  return name

def get_desc_from_request(request_id): #included in request table
  open_database()
  desc = conn.execute("SELECT description_ from request WHERE request_id = ?", (request_id, )).fetchone()[0]

  return desc

def get_date_from_request(request_id): #included in request table
  open_database()
  date_sql = conn.execute("SELECT due_date from request WHERE request_id = ?", (request_id, )).fetchone()[0]

  return date_sql

def submit_file(uploaded_file, request_id):
  filename = secure_filename(uploaded_file.filename)

  split_tup = os.path.splitext(filename)
  file_name = split_tup[0] # this is the file_name of the ORIGINAL
  file_ending = split_tup[1] #file ending of the ORIGINAL

  user_name = get_name_from_request(request_id)

  print("user_name: ", user_name)
  print("File Name: ", file_name)
  print("File Extension: ", file_ending)

  file_name_stored = user_name + "-" + str(request_id)

  # need to get the request id that it relates to.

  numofoccurrence = 0
  thingy = ""
  if not file_ending in main.ALLOWED_EXTENSIONS:
    print("-------------")
    print("File ending not accepted!!")
    print("-------------")

  finished_filename = secure_filename(file_name_stored + file_ending)
  
  uploaded_file.save(os.path.join(main.app.config['UPLOAD_FOLDER'], finished_filename))

def get_file_num(filename):
  indexofperiod = filename.rindex('.')
  indexofdash = filename.rindex('-')

  finished_string = filename[indexofdash + 1:indexofperiod]

  return int(finished_string)


def get_archived_request_ids():
  open_database()

  request_ids_sql = conn.execute("SELECT request_id FROM request_archived")
  returned = []
  for i in request_ids_sql:
    for g in i:
      returned.append(g)

  return returned
  


def get_all_archived_requests():
  open_database()
  thing = conn.execute("SELECT request_id, due_date,  description_ FROM request_archived")

  returned = []

  for i in thing:
    for g in i:
      returned.append(g)

  return returned

def get_emails_from_archived_request():
  open_database()
  emails = []

  ids_sql = conn.execute("SELECT customer_id_ FROM request_archived")
  ids = []
  for i in ids_sql:
    for g in i:
      ids.append(g)

  for i in ids:
    thing_sql = conn.execute("SELECT email_address FROM customer WHERE customer_id = ?", (i, ))
    for i in thing_sql:
      for g in i:
        emails.append(g)

  return emails