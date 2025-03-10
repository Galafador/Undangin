# Undangin
**A web based wedding invitation builder as a final project for CS50x**

Tech stack: `Python, Flask, SQLite, HTML, CSS, Javascript, Whimsical, Figma.`

video demonstration:

## Overview
Undangin is a web application for creating online wedding invitations.
The app is divided into two parts: 
1. The WebUI for the administrator and client
2. The actual wedding invitation page

### Web-UI
In this part, administrators can create events, edit events, delete events, upload photos for each event, and preview the events.
clients also have a space to preview their invitation, see a list of people that have filled the attendance form, and create invitation link personalized with a recipient's name.

### Wedding Invitation Page
The pages are automatically created from a template, no manual editing needed. currently there's only a single template, but it's very easy to add more later down the line.
each page can be personalized using `?kepada=<recipient-name-here>` query parameter. Recipients can also fill the attendance form on the page.

## How does it work?
Undangin is a Flask web application, so to run it simply clone the repo, install the requirements with `pip install -r requirements.txt` and then run the app from the commandline with `flask run`.

1. **app.py** : The brain of the app, manages all of the main functions.
2. **helpers.py** : contains several useful helpers functions, some are taken from the CS50 finance problem. *thanks CS50 :)*
3. **invitation.db** : sqlite database, contains these tables : `attendance, contacts, event, users`
4. **/templates/Wedding1/** : the template used for the invitation page.

The flow for creating an invitation page should look like this:
1. Client asks admin to create an online wedding invitation page
2. admin asks client for their info and some photos for the page
3. admin creates the page with the info
4. admin uploads photos
5. the app creates the invitation page and a default username/password for client to login to webUI (currently its just eventID for both)
6. client can personalize the invitation page with a recipients name in the Send Invitation menu
7. client can see the list of people who have filled the attendance form on tha invitation page

## To-do
1. Add a feature for recipients to add comments on the invitation page
2. Add more templates
3. Add a feature so that clients can easily broadcast the personalized links through whatsapp / email
4. Add basic account management system

## Screenshots
![Sign-in Screenshot](https://i.imgur.com/hAaOd1M.png) 
![Create Event Screenshot](https://i.imgur.com/ZUrx8Ee.png)
![Invitation Screenshot](https://i.imgur.com/tFm3QIx.png)
![Responsive Design Screenshot](https://i.imgur.com/2G6ZpmG.png)








