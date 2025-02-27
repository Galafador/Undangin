import os
import shutil
import locale

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, send_from_directory, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from urllib.parse import quote

from helpers import apology, login_required, admin_required, convert_dateformat

# Configure application

app = Flask(__name__)

# Configuration for image upload functionality
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 48 * 1024 * 1024 #48MB Limit

# Utility function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///invitation.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    # Check if the user is not admin
    if session['role'] != 'admin':
        user_id = session['user_id']
        return redirect("/detail/" + str(user_id))
    
    return render_template("index.html")


@app.route("/detail/<int:user_id>")
@login_required
def detail(user_id):
    # Display the lists of events owned by the user
    # query database for all events owned by the user
    events = db.execute("SELECT namaevent, mempelaipria, mempelaiwanita, tanggalAkad FROM event WHERE user_id IS ?", user_id)
    for event in events:
        formatted_date = convert_dateformat(event['tanggalAkad'])
        event['tanggalAkad'] = formatted_date
    return render_template("detail.html", events=events)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["role"] = rows[0]["role"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

  
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and password confirmation is the same
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("Passwords do not match", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username doesn't exists
        if len(rows) != 0:
            return apology("Username already exists", 400)

        # Register user to database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password"), method='scrypt'))

        # Redirect user to home page
        flash('You are now registered!', 'success')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    

@app.route("/create", methods=["GET", "POST"])
@admin_required
def create():

    if request.method == "POST":
        namaevent = request.form.get("namaevent")
        mempelaipria = request.form.get("mempelaipria")
        panggilanpria = request.form.get("panggilanpria")
        putrake = request.form.get("putrake")
        mempelaiwanita = request.form.get("mempelaiwanita")
        panggilanwanita =  request.form.get("panggilanwanita")
        putrike = request.form.get("putrike")
        ayahmempelaipria = request.form.get("ayahmempelaipria")
        ibumempelaipria = request.form.get("ibumempelaipria")
        ayahmempelaiwanita = request.form.get("ayahmempelaiwanita")
        ibumempelaiwanita = request.form.get("ibumempelaiwanita")
        tanggalAkad = request.form.get("tanggalAkad")
        jamAkad = request.form.get("jamAkad")
        alamat1Akad = request.form.get("alamat1Akad")
        alamat2Akad = request.form.get("alamat2Akad")
        linkMapsAkad = request.form.get("linkMapsAkad")
        tanggalResepsi = request.form.get("tanggalResepsi")
        jamResepsi = request.form.get("jamResepsi")
        alamat1Resepsi = request.form.get("alamat1Resepsi")
        alamat2Resepsi = request.form.get("alamat2Resepsi")
        linkMapsResepsi = request.form.get("linkMapsResepsi")

        # Ensure all fields was submitted
        if not namaevent or not mempelaipria or not panggilanpria or not putrake or not mempelaiwanita or not panggilanwanita or not putrike or not ayahmempelaipria or not ibumempelaipria or not ayahmempelaiwanita or not ibumempelaiwanita or not tanggalAkad or not jamAkad or not alamat1Akad or not alamat2Akad or not linkMapsAkad or not tanggalResepsi or not jamResepsi or not alamat1Resepsi or not alamat2Resepsi or not linkMapsResepsi:
            flash('Seluruh form harus diisi', 'warning')
            return render_template("create.html")

        # Find from DB event with the same name
        dbevent = db.execute(
            "SELECT * FROM event WHERE namaevent = ?", namaevent)

        # Check if the same event already exists
        if len(dbevent) != 0:
            flash('Event already exists', 'warning')
            return render_template("create.html")

        else:
            # Create user and assign it to this event
            username = namaevent
            password = namaevent
            role = "user"

            db.execute("INSERT INTO users (username, hash, role) VALUES (?, ?, ?)", username, generate_password_hash(password, method='scrypt'), role)
            user_id = db.execute("SELECT id FROM users WHERE username=?", username)
            id = user_id[0]['id']
            
            print(f"id is {id}")

            # Register event to database
            db.execute("INSERT INTO event (user_id, namaevent, mempelaipria, panggilanpria, putrake, mempelaiwanita, panggilanwanita, putrike, ayahmempelaipria, ibumempelaipria, ayahmempelaiwanita, ibumempelaiwanita, tanggalAkad, jamAkad, alamat1Akad, alamat2Akad, linkMapsAkad, tanggalResepsi, jamResepsi, alamat1Resepsi, alamat2Resepsi, linkMapsResepsi) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", id, namaevent, mempelaipria, panggilanpria, putrake, mempelaiwanita, panggilanwanita, putrike, ayahmempelaipria, ibumempelaipria, ayahmempelaiwanita, ibumempelaiwanita, tanggalAkad, jamAkad, alamat1Akad, alamat2Akad, linkMapsAkad, tanggalResepsi, jamResepsi, alamat1Resepsi, alamat2Resepsi, linkMapsResepsi)

            # Show Events
            flash('Event Registered', 'success')
            return edit()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("create.html")
    

@app.route("/edit", methods=["GET"])
@admin_required
def edit():
    # Display the lists of all the events
    # query database for all events
    events = db.execute("SELECT * FROM event ORDER BY id DESC")
    for event in events:
        formatted_date = convert_dateformat(event['tanggalAkad'])
        event['tanggalAkad'] = formatted_date
    return render_template("edit.html", events=events)


@app.route("/editing/<int:id>", methods=["GET", "POST"])
@admin_required
def editing(id):

    if request.method == "POST":
        namaevent = request.form.get("namaevent")
        mempelaipria = request.form.get("mempelaipria")
        panggilanpria = request.form.get("panggilanpria")
        putrake = request.form.get("putrake")
        mempelaiwanita = request.form.get("mempelaiwanita")
        panggilanwanita =  request.form.get("panggilanwanita")
        putrike = request.form.get("putrike")
        ayahmempelaipria = request.form.get("ayahmempelaipria")
        ibumempelaipria = request.form.get("ibumempelaipria")
        ayahmempelaiwanita = request.form.get("ayahmempelaiwanita")
        ibumempelaiwanita = request.form.get("ibumempelaiwanita")
        tanggalAkad = request.form.get("tanggalAkad")
        jamAkad = request.form.get("jamAkad")
        alamat1Akad = request.form.get("alamat1Akad")
        alamat2Akad = request.form.get("alamat2Akad")
        linkMapsAkad = request.form.get("linkMapsAkad")
        tanggalResepsi = request.form.get("tanggalResepsi")
        jamResepsi = request.form.get("jamResepsi")
        alamat1Resepsi = request.form.get("alamat1Resepsi")
        alamat2Resepsi = request.form.get("alamat2Resepsi")
        linkMapsResepsi = request.form.get("linkMapsResepsi")

        # Ensure all fields was submitted
        if not namaevent or not mempelaipria or not panggilanpria or not putrake or not mempelaiwanita or not panggilanwanita or not putrike or not ayahmempelaipria or not ibumempelaipria or not ayahmempelaiwanita or not ibumempelaiwanita or not tanggalAkad or not jamAkad or not alamat1Akad or not alamat2Akad or not linkMapsAkad or not tanggalResepsi or not jamResepsi or not alamat1Resepsi or not alamat2Resepsi or not linkMapsResepsi:
            flash('Seluruh form harus diisi', 'warning')
            return editing(id)

        # Update event in database
        db.execute("UPDATE event SET namaevent = ?, mempelaipria = ?, panggilanpria = ?, putrake = ?, mempelaiwanita = ?, panggilanwanita = ?, putrike = ?, ayahmempelaipria = ?, ibumempelaipria = ?, ayahmempelaiwanita = ?, ibumempelaiwanita = ?, tanggalAkad = ?, jamAkad = ?, alamat1Akad = ?, alamat2Akad = ?, linkMapsAkad = ?, tanggalResepsi = ?, jamResepsi = ?, alamat1Resepsi = ?, alamat2Resepsi = ?, linkMapsResepsi = ? WHERE id = ?", namaevent, mempelaipria, panggilanpria, putrake, mempelaiwanita, panggilanwanita, putrike, ayahmempelaipria, ibumempelaipria, ayahmempelaiwanita, ibumempelaiwanita, tanggalAkad, jamAkad, alamat1Akad, alamat2Akad, linkMapsAkad, tanggalResepsi, jamResepsi, alamat1Resepsi, alamat2Resepsi, linkMapsResepsi, id)

        # Show Events
        flash('Event Updated', 'success')
        return edit()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        event = db.execute("SELECT * FROM event WHERE id = ?", id)
        if event:
            event = event[0]
        return render_template("editing.html", event=event)
    
@app.route("/delete/<int:id>", methods=["GET", "POST"])
@admin_required
def delete(id):
        
        rows = db.execute("SELECT user_id FROM event WHERE id IS ?", id)
        user_id = rows[0]['user_id']

        db.execute("DELETE FROM attendance WHERE event_id IS ?", id)
        print("Attendance Deleted")

        db.execute("DELETE FROM event WHERE id IS ?", id)
        print("Event Deleted")

        db.execute("DELETE FROM contacts WHERE user_id IS ?", user_id)
        print("Contacts Deleted")

        db.execute("DELETE FROM users WHERE id IS ?", user_id)
        print("User Deleted")


        flash('Event Deleted', 'warning')

        return edit()


@app.route("/upload/<int:id>", methods=["GET", "POST"])
@admin_required
def upload(id):
    if request.method == 'POST':
        # Create a folder named after the provided id after deleting it if it already exists
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
        
        if os.path.exists(upload_folder):
            shutil.rmtree(upload_folder)

        os.makedirs(upload_folder, exist_ok=True)

        # Process each single file upload
        single_fields = [
            "GroomPhoto",
            "BridePhoto",
            "AkadPhoto",
            "ResepsiPhoto",
            "LeftHalfPhoto",
            "ClosingPhoto",
        ]

        for field in single_fields:
            file = request.files.get(field)
            if file and allowed_file(file.filename):
                orig_filename = secure_filename(file.filename)
                file_ext = orig_filename.rsplit('.', 1)[1]
                # New filename: fieldName_UUID.extension
                new_filename = f"{field}.{file_ext}"
                file.save(os.path.join(upload_folder, new_filename))

        
        # Process the multiple BestMoments file input
        best_moments_photos = request.files.getlist("BestMoments")
        # Rename files as BestMomentsPhoto1 upto BestMomentsPhoto8 even if fewer are uploaded
        for i, file in enumerate(best_moments_photos, start=1):
            if i > 8:
                break
            if file and allowed_file(file.filename):
                orig_filename = secure_filename(file.filename)
                file_ext = orig_filename.rsplit('.', 1)[1]
                new_filename = f"BestMomentsPhoto{i}.{file_ext}"
                file.save(os.path.join(upload_folder, new_filename))

        # Show Events
        flash('Photos Uploaded', 'success')
        return redirect(url_for('edit'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("upload.html", id=id)
    

#Route to serve static files from any Wedding templates directory
@app.route('/Wedding/<template_num>/<path:filename>')
def wedding_static(template_num, filename):
    return send_from_directory(os.path.join(app.root_path, 'templates', f'Wedding{template_num}'), filename)
    

@app.route("/undangan/<namaevent>", methods=["GET", "POST"])
def undangan(namaevent):

    if request.method == 'POST':
        # get personalized name
        kepada = request.args.get('kepada')

        event = db.execute("SELECT * FROM event WHERE namaevent IS ?", namaevent)
        if event:
            event = event[0]
            event_id = event['id']
            inisialpria = event['panggilanpria'][0]
            inisialwanita = event['panggilanwanita'][0]

            # formats datetime
            date_str_akad = event['tanggalAkad']
            date_str_resepsi = event['tanggalResepsi']

            # set locale to indonesia
            locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

            # Convert into datetime object
            date_obj_akad = datetime.strptime(date_str_akad, "%Y-%m-%d")
            date_obj_resepsi = datetime.strptime(date_str_resepsi, "%Y-%m-%d")

            # Extract year, month, day, date
            yearAkad = date_obj_akad.year
            monthAkad = date_obj_akad.strftime('%B')
            dayAkad = date_obj_akad.day
            hariAkad = date_obj_akad.strftime("%A")

            yearResepsi = date_obj_resepsi.year
            monthResepsi = date_obj_resepsi.strftime('%B')
            dayResepsi = date_obj_resepsi.day
            hariResepsi = date_obj_resepsi.strftime("%A")

            # code to handle attendance form submission
            KonfirmasiNama = request.form.get("KonfirmasiNama")
            KonfirmasiKehadiran = request.form.get("KonfirmasiKehadiran")
            
            names = db.execute("SELECT * FROM attendance WHERE nama IS ?", KonfirmasiNama)

            if len(names) != 0:
                print("Form kehadiran sudah diisi dengan nama yang sama")
                return apology("Form kehadiran sudah diisi dengan nama yang sama", 404)

            db.execute("INSERT INTO attendance (event_id, nama, kehadiran) VALUES (?,?,?)", event_id, KonfirmasiNama, KonfirmasiKehadiran)
        
            return render_template(f'Wedding1/template.html', namaevent=namaevent, event=event, inisialwanita=inisialwanita, inisialpria=inisialpria, yearAkad=yearAkad, monthAkad=monthAkad, dayAkad=dayAkad, hariAkad=hariAkad, yearResepsi=yearResepsi, monthResepsi=monthResepsi, dayResepsi=dayResepsi, hariResepsi=hariResepsi, kepada=kepada)
        
        else:
            return apology("Not Found", 404)


    else:

        # get personalized name
        kepada = request.args.get('kepada')

        # Check database for the event
        event = db.execute("SELECT * FROM event WHERE namaevent IS ?", namaevent)

        if event:
            event = event[0]
            inisialpria = event['panggilanpria'][0]
            inisialwanita = event['panggilanwanita'][0]

            # define links for photos

            # formats datetime
            date_str_akad = event['tanggalAkad']
            date_str_resepsi = event['tanggalResepsi']

            # set locale to indonesia
            locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

            # Convert into datetime object
            date_obj_akad = datetime.strptime(date_str_akad, "%Y-%m-%d")
            date_obj_resepsi = datetime.strptime(date_str_resepsi, "%Y-%m-%d")

            # Extract year, month, day, date
            yearAkad = date_obj_akad.year
            monthAkad = date_obj_akad.strftime('%B')
            dayAkad = date_obj_akad.day
            hariAkad = date_obj_akad.strftime("%A")

            yearResepsi = date_obj_resepsi.year
            monthResepsi = date_obj_resepsi.strftime('%B')
            dayResepsi = date_obj_resepsi.day
            hariResepsi = date_obj_resepsi.strftime("%A")

            return render_template(f'Wedding1/template.html', namaevent=namaevent, event=event, inisialwanita=inisialwanita, inisialpria=inisialpria, yearAkad=yearAkad, monthAkad=monthAkad, dayAkad=dayAkad, hariAkad=hariAkad, yearResepsi=yearResepsi, monthResepsi=monthResepsi, dayResepsi=dayResepsi, hariResepsi=hariResepsi, kepada=kepada)

        else:
            return apology("Not Found", 404)
        

@app.route("/attendees/", methods=["GET"])
def attendees():
    
    # Check db for attendees of event with provided id
    user_id = session['user_id']
    rows = db.execute("SELECT nama, kehadiran FROM attendance JOIN event on attendance.event_id=event.id JOIN users ON users.id=event.user_id WHERE user_id IS ?", user_id)

    return render_template('attendees.html', rows=rows)

@app.route("/send/", methods=["GET", "POST"])
def send():
    names = []
    if request.method == 'POST':
        user_id = session['user_id']

        #get namaevent
        rows = db.execute("SELECT namaevent FROM event WHERE user_id IS ?", user_id)
        namaevent = rows[0]['namaevent']
        content = request.form['names']

        # split the content by newline and create slugs
        names = content.split('\n')
        names = [name.strip() for name in names if name.strip()]
        
        print(f"{names}")

        links = [f'127.0.0.1:5000/undangan/{namaevent}?kepada={quote(name)}' for name in names]

        # combine names and links into a list of tuples
        results = list(zip(names, links))

        # Save to database
        for name, link in results:
            db.execute('INSERT INTO contacts (user_id, name, link) VALUES (?, ?, ?)', user_id, name, link)
        
        results = db.execute ("SELECT id, name, link FROM contacts WHERE user_id IS ?", user_id)
        return render_template('send.html', results=results)
    
    else:
        user_id = session['user_id']

        #get contacts list
        results = db.execute ("SELECT id, name, link FROM contacts WHERE user_id IS ?", user_id)

        return render_template('send.html', results=results)
    
@app.route("/delete_contact/<int:id>", methods=["GET", "POST"])
def delete_contact(id):
        
        db.execute("DELETE FROM contacts WHERE id IS ?", id)
        return send()
