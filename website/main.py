from flask import Flask, render_template, request, redirect, url_for, flash

import handling_builder
import handling_customer 
import handling_machines

import sqlite3
import os
from werkzeug.utils import secure_filename

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
db.init_app(app)
db.app = app
app.secret_key = "secret"
UPLOAD_FOLDER = 'website/static/files' 

ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.docx', '.stl']) #configure later
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ARCHIVED_FOLDER'] = "website/static/archived_files"

# project does not run from within website folder (you will need to do something like python website/main.py)

# folder where uploads go to
# db.drop_all()
# db.drop_all()

alldocs = []
# user class for user sessions
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    def __repr__(self):
        return '<User %r>' % self.id



login_manager = LoginManager()

# page to redirect to if login fails
login_manager.login_view = 'builder_homepage'

login_manager.init_app(app) 

# load in the user with their user id
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


# resetting functions
def reset_everything_customers():
  handling_customer.delete_all_customers()
  handling_customer.delete_all_requests()
  handling_customer.reset_id_counter()
  handling_machines.delete_all_machine_requests()
  handling_customer.delete_all_archived_requests()
  for filename in os.listdir(app.config['UPLOAD_FOLDER']):
    print(filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def reset_everything_builders():
  handling_builder.delete_all_builders()

def reset_everything_machines():
  handling_machines.delete_all_machine_requests()
  handling_machines.delete_machine_request_archived()


def nuke():
  # why would you do this, I'm warning you
  reset_everything_customers()
  reset_everything_machines()
  print("nuked!")

def extraNuke():
  reset_everything_builders()
  nuke()
  print("extra nuked!")


@app.route('/', methods = ['GET'])
def index():
  # extraNuke()
  # nuke()
  handling_builder.print_all_builders()
  return render_template('index.html')
  
@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash("Logged out!", "info")
  return redirect('/builder_homepage')

@app.route('/make_request', methods = ['POST', 'GET'])
# for machines
def make_request():
  # resetEVERYTHING()
  # handling_builder.add_machine("lmao", "yo")
  # handling_builder.remove_machine("lmao")

  
  if request.method == "POST":
    # take information using flask's library w/ request
    
    machineListInfo = [] # holds machines
    customer_email = request.form['email']
    customer_desc = request.form['task_details']
    customer_name = request.form['name']
    dueDate = request.form['due_date']
    
    all_machines_names = handling_machines.get_all_machine_names()

    print("--- taking machine names ----")
    
    # iterates through all possible machine names, if it is possible to grab form data, do it and store it in the list. 

    for i in all_machines_names:
      try:
        machineListInfo.append(request.form[i])
      except:
        machineListInfo.append("off")


    # take the file from the form
    uploaded_file = request.files['file']
    
    # create the customer. 
    handling_customer.customerCreate(customer_email, customer_name)
    
    # handling_customer.print_all_customers()

    # make the request with information received.
    request_id = handling_customer.customer_make_request(handling_customer.get_customer_id(customer_email), dueDate, customer_desc)

    num = 1 #representing machine number

    for i in machineListInfo:
      if i == "on":
        handling_machines.make_machine_request(request_id, num)
        print("successfully made request with machine " + str(num))
      num += 1
    
    
    if uploaded_file.filename != '':
      # submit the file, passing in the uploaded file object and the request id.
      handling_customer.submit_file(uploaded_file, request_id) #file type
    
    # handling_customer.print_all_requests()

    return redirect('/make_another')

  elif request.method == "GET":
    # get all existing machine names.
    m = handling_machines.get_all_machine_names()
    
    machine_names = []

    # uhh, note to self: what is happening here lol.
    for i in m:
      machine_names.append(''.join(i))

    # get all machine descriptions from all existing machines.
    m = handling_machines.get_all_machine_descriptions()
    machine_descriptions = []

    for i in m:
      machine_descriptions.append(''.join(i))
    
    # render the page w/ machine names and descriptions
    
    return render_template("make_request.html", machine_names = machine_names, machine_descriptions = machine_descriptions)

@app.route('/builder_homepage', methods = ['POST', 'GET'])
def builder_homepage():
  # handling_builder.approve_builder("asdf@gmail.com")
  # handling_builder.print_all_builders()
  # handling_builder.delete_all_builders()
  handling_builder.print_all_builders()

  if request.method == "POST":
    # receive information
    builder_email = request.form['builder_email']
    passw = request.form['password']
    # confirm if builder approved, their builder id 
    things = handling_builder.check_builder(builder_email)

    thing = things[0] # if it exists
    thing2 = things[1] # builder id
    print("Thing: " + str(thing))
    
    if thing:
      hashpass = handling_builder.get_hashed_pass(handling_builder.get_builder_id(builder_email))  
      print("hashpass outside: " + hashpass)
      matchpasses = check_password_hash(hashpass, passw)
      # matchpasses = check_password_hash(generate_password_hash("password", method = 'sha256'), "password")
      print("hi: " + str(matchpasses))
      if matchpasses:
        print("hashpass: " + hashpass)
        print("-------------------")
        print("--- successful! ---")
        print("-------------------")
        # the builder should exist, find it and log it in
        user = User.query.filter_by(id=thing2).first()
        print(user)
        login_user(user, remember = True)
        print('hhiii')
        return redirect('/builder_signed_in')
      flash("Invalid username or password.", "error")      
    else:
      print("--------------")
      print("--- failed ---")
      print("--------------")
      flash("Invalid username or password.", "error")
  return render_template('builder_homepage.html')

@app.route('/finish/<int:id>') #need to make this work for taking request stuff.
@login_required
def finish_task(id):
  # request = handling_customer.get_request_by_id(id)
  email_address = handling_customer.get_email_from_request(id)
  customer_name = handling_customer.get_name_from_request(id)
  desc = handling_customer.get_desc_from_request(id)
  DATE = handling_customer.get_date_from_request(id)


  machines_sql = handling_machines.get_machineNames_used_by_id(id)
  machines = ""

  for i in machines_sql:
    machines += (i + ", ")

  
  thing = handling_customer.send_email(email_address, "Your machining task has been finished", "Hello " + customer_name + ",\n\nYour product with the description of: " + desc + ", using machine(s): " + machines + "\nhas been finished. Come by the mill to pick it up. \n " ) # works 


  handling_customer.finish_request(id)
  handling_machines.finish_machines(id)
  return redirect('/builder_signed_in')


@app.route('/builder_signed_in', methods = ['POST', 'GET']) # confirm email shows up properly.
@login_required
def builder_login():
  request_ids = handling_customer.get_request_ids()

  stuff = handling_customer.get_all_requests() #get all the request info
  emails = handling_customer.get_emails_from_request() #grab emails
  print('hihi')
  stuff_list = [] #holds all request info

  alldocs = []
  for filename in os.listdir(app.config['UPLOAD_FOLDER']):
    if not os.path.join(app.config['UPLOAD_FOLDER'], filename) in alldocs and not filename.endswith(".css"): # need to make it check if it is a folder, in which you don't want it to append.
        alldocs.append(os.path.join("/static/files/", filename)) 
  
  print('hihiagain')
  
  x = 0 #iterator
  for i in stuff:
    new_stuff = []

    for g in i:
      new_stuff.append(g)
    try:
      new_stuff.insert(0, emails[x])
    except:
      pass
    stuff_list.append(new_stuff)
    x += 1
  
  machineNames = [] # stores names of each machine for each request, diff machines separated by commas
  

  for r in request_ids:
    # get machine names by the id.
    machineNameList = handling_machines.get_machineNames_used_by_id(r)
    
    for i in range(len(machineNameList)):
      if (i != len(machineNameList) - 1):
        machineNameList[i] = machineNameList[i] + ", "
      else:
        machineNameList[i] = machineNameList[i]

    machineNames.append(machineNameList)
  
  # for i in machineNames:
  #   print("---- starting new machines for request ---- ")

  #   for g in i:
  #     print(g)
      
  return render_template("builder_logged_in.html", stuff_list = stuff_list, request_ids = request_ids, alldocs = alldocs, machineNames = machineNames)

  
@app.route('/make_another', methods = ['GET'])
def another():
  return render_template('make.html')

  
@app.route('/edit/<int:request_id>', methods = ['POST', 'GET']) # Allow builders to make edits to part of the request (i.e. description, start request)
@login_required
def edit(request_id):
  
  # 1. description
  # 2. machines required
  # 3. builder name assigned
  if request.method == 'POST':
    if "edit_stuff" in request.form:
      # updating new info
      machineListInfo = []
      all_machines_names = handling_machines.get_all_machine_names()

      print("--- taking machine names ----")
      # iterates through all possible machine names, if it is possible to grab form data, do it and store it in the list. 
      machine_id_list = []
      machine_used_list = []
      for i in all_machines_names:
        print("looped")
        mac_id = handling_machines.get_machine_id_from_name(i)
        machine_id_list.append(mac_id)
        try:
          info = request.form[i] # the machine is on.
          machineListInfo.append(True)
        except:
          info = "nonexistent"
          machineListInfo.append(False)
        print("info: " + info)
      
      desc = request.form['desc']
      handling_customer.update_desc(request_id, desc)

      handling_machines.alter_machines(request_id, machine_id_list, machineListInfo)

      machines_sql = handling_machines.get_machineNames_used_by_id(request_id)
      
      macs = ""
      for i in machines_sql:
        macs += (i + ", ")

      cust_email = handling_customer.get_email_from_request(request_id)
      
      # handling_customer.send_email(cust_email, "Updated Request", "Hi, we have updated your request's machines to..." + macs + " and/or the description to..." + desc)

      return redirect('/builder_signed_in')
      

    elif "delete_req" in request.form:
      print("posting to delete req")
      if request.form['delete_text'] == "DELETE":
        # give a reason for rejection later?? Integrate into a new sql table??
        print("hi")
        x = request.form.get('should_email')

        if not x:
          x = "off"
        print(type(x))
        
        if (x == 'on'):
          print("asdf")
          msg = "Hi, sorry to inform you that your request has been rejected for reason(s), " + request.form["reason"] + ". Please contact us for more info. \n"
  
          
          ehh = handling_customer.send_email(handling_customer.get_email_from_request(request_id), "MHS machining request rejected", msg) # send email only works without colons??
          print("asdf")
          
        handling_customer.delete_request(request_id)
        handling_machines.finish_machines(request_id) 
        handling_customer.delete_file(request_id)
        return redirect('/builder_signed_in')

      else:
        flash("try retyping.", "error")
        return redirect('/edit/' + str(request_id))
    
  elif request.method == 'GET':
    machines_used = handling_machines.get_machineNames_used_by_id(request_id)
    all_machines_names = handling_machines.get_all_machine_names()
    task_desc = handling_customer.get_description(request_id)
    return render_template("edit_request.html", request_id = request_id, machines_used = machines_used, task_desc = task_desc, all_machines_names = all_machines_names)
  
  return redirect('/edit/' + str(request_id))

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return render_template('error.html')


@app.route('/builder_signup', methods = ['POST', 'GET'])
def builder_signup():
  # handling_builder.delete_all_builders()
  # handling_customer.delete_all_customers()
  # handling_customer.delete_all_requests()
  print("printing builders")
  handling_builder.print_all_builders()
  
  if request.method == "POST":
    builder_name = request.form['builder_name']
    builder_email = request.form['builder_email']
    psswd = request.form['psswd']

    # generate the password hash for security, create add the builder (not approved yet).
    hash_psswd =  generate_password_hash(psswd, method = 'sha256')
    
    print("hello: " + hash_psswd)
    if handling_builder.find(builder_email):
      flash("Builder already exists!", "error")
      return redirect("/builder_signup")
    
    handling_builder.add_builder(builder_email, builder_name, hash_psswd) #add the builder. 
    # handling_builder.print_all_builders() #it works, retest tmmr
    # handling_customer.print_all_customers()
    # handling_customer.print_all_requests()
    # handling_builder.close_database()
  return render_template('builder_signup.html')
@app.route('/test')
@login_required
def testing():
  print("why")
  print(handling_builder.getunapproved())
  builderarrraw = handling_builder.getunapproved()
  builderarr = []
  for j in builderarrraw:
    builderarr.append(j)
  print(builderarr)
  return render_template("test.html", builderarr = builderarr)
@app.route("/approve/<builder_email>")
def approve(builder_email):
  handling_builder.approve_builder(builder_email)
  flash("Buidler Approved!", "info")
  return redirect("/test")
@app.route("/deny/<builder_email>")
def deny(builder_email):
  print("we here?")
  print(builder_email)
  handling_builder.delete_builder(builder_email)
  print("e")
  User.query.filter_by(email=builder_email).delete()
  db.session.commit()
  return redirect("/builder_signed_in")
@app.route("/approve_builder_page", methods = ['POST', 'GET'])
@login_required
def approve_builder_func():
  if request.method == "POST":
    builder_email = request.form['email_to_be_approved']
    tings = handling_builder.check_builder(builder_email)
    if not tings:
      flash("Invalid email", 'error')
      return redirect("/approve_builder_page")
    handling_builder.approve_builder(builder_email) #add the builder. 
    otherid  = handling_builder.get_builder_id(builder_email)
    newbuilder = User(email = builder_email, id = otherid)
    db.session.add(newbuilder)
    db.session.commit()
    flash("Email approved", "info")
  return render_template("approve_builder.html")

@app.route("/archived_requests", methods = ['POST', 'GET'])
@login_required
def arch_requests():
  # work in progress.
  # if it says implement, it means you need to make the function (most likely).
  
  request_ids = handling_customer.get_archived_request_ids() 

  stuff = handling_customer.get_all_archived_requests()
  emails = handling_customer.get_emails_from_archived_request() # implement

  stuff_list = [] #holds all request info

  alldocs = []
  for filename in os.listdir(app.config['ARCHIVED_FOLDER']):
    if not os.path.join(app.config['ARCHIVED_FOLDER'], filename) in alldocs and not filename.endswith(".css"): # need to make it check if it is a folder, in which you don't want it to append.
        alldocs.append(os.path.join("/static/archived_files/", filename))
    
  
  
  x = 0 #iterator
  for i in stuff:
    new_stuff = []
    new_stuff.append(i)
    try:
      new_stuff.insert(0, emails[x])
    except:
      pass
    stuff_list.append(new_stuff)
    x += 1
  
  # todo: make list storing machines? Pass this thru render
  machineNames = [] # stores names of each machine for each request, diff machines separated by commas
  
  for r in request_ids:
    machineNameList = handling_machines.get_machineNames_used_by_archived_id(r) # implement
    
    for i in range(len(machineNameList)):
      # print("request: " + str(r) + " used: " + machineNameList[i])
      if (i != len(machineNameList) - 1):
        machineNameList[i] = machineNameList[i] + ", "
      else:
        machineNameList[i] = machineNameList[i]

    machineNames.append(machineNameList)
      
  return render_template("archived_requests.html", stuff_list = stuff_list, request_ids = request_ids, alldocs = alldocs, machineNames = machineNames)


if __name__ == "__main__":
  app.jinja_env.cache = {} # random thing found online that supposedly boosts loading time lmao
  app.run(host = "0.0.0.0") 

