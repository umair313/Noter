from core import db,create_app,create_db

app = create_app()
create_db(app,db)

if __name__ == "__main__":
	app.run(debug=True)
