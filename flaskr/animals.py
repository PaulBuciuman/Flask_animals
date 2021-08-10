from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import os,requests
import urllib.request
from flaskr.db import get_db

bp = Blueprint('animals', __name__)

@bp.route('/', methods=('GET', 'POST'))
def fav_animal():
	if request.method == 'POST':
		username = request.form['username']
		animal_type=request.form['animal_type']
		db=get_db()
		error=None

		if not username:
			error = 'Username is required.'

		if request.form["action"] == 'Save':
			directory = 'flaskr/animal_photos/'+username
			if not os.path.exists(directory):
				os.makedirs(directory)

			if error is None:
				try:
					db.execute('INSERT INTO user (username) VALUES (?)',
					(username,),
					)
					db.execute('INSERT INTO animal (type,owner_id) VALUES (?,?)',
					(animal_type,'SELECT last_insert_rowid()'),
					)
					db.commit()

				except db.IntegrityError:
					error=f"User {username} is already registered."
				else:
					return redirect(url_for("animals.fav_animal"))
		elif request.form["action"]=='Fetch':
			user = db.execute('SELECT * FROM user WHERE username =?',(username,)).fetchone()

			if user is None:
				error = 'User does not exist'

			if error is None:
				directory = 'flaskr/animal_photos/'+username
				for i in range(2):
					JSONresponse = requests.get('https://thatcopy.pw/catapi/rest/')
					response=requests.get(JSONresponse.json()["url"])

					cats = db.execute('SELECT * FROM animal WHERE type =?',('Cat',)).fetchall()
					print(cats)



					with open(directory+'/cat'+str(i)+'.jpg',"wb") as f:
						f.write(response.content)

				return redirect(url_for("animals.fav_animal"))

		flash(error)

	return render_template('animals/index.html')






  