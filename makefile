include ./backend/.env
export

postgres_connection:
	@docker exec -it postgres_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

backend_shell:
	@docker exec -it docfind-backend bash