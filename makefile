include ./backend/.env
export

postgres_connection:
	@docker exec -it postgres_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

python_shell:
	@docker exec -it docfind-backend bash