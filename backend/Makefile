include .env
export

init:
	@python -m app.init

dev: init
	@DATABASE_URL=localhost:5432 flask --debug run --host=0.0.0.0 --port=5000

run: init
	@flask run --host=0.0.0.0 --port=5000