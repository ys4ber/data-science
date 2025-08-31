include .env
export

DOCKER_COMPOSE = docker-compose -f ex00/docker-compose.yml

up:
	@$(DOCKER_COMPOSE) up -d

down:
	@$(DOCKER_COMPOSE) down

clear_db:
	@echo "Clearing database..."
	@$(DOCKER_COMPOSE) exec postgres psql -h $(POSTGRES_HOST) -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

check_db:
	@echo "Checking database tables..."
	@$(DOCKER_COMPOSE) exec postgres psql -h $(POSTGRES_HOST) -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\dt"

db_info:
	@echo "Database connection info:"
	@echo "Host: $(POSTGRES_HOST)"
	@echo "Port: $(POSTGRES_PORT)"
	@echo "Database: $(POSTGRES_DB)"
	@echo "User: $(POSTGRES_USER)"