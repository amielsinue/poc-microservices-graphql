# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
-include $(shell pwd)/.app.rc
export DOCKER_DEFAULT_PLATFORM=linux/amd64

.PHONY: help
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

null:
	help

# Makefile Command Line Arguments!
ARGS = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

CURRENT_UID := $(shell id -u)
CURRENT_GID := ${CURRENT_UID}
WWWUSER=${WWWUSER:-$(CURRENT_UID)}
WWWGROUP=${WWWGROUP:-$(CURRENT_GID)}
export WWWUSER
export WWWGROUP
UID=${CURRENT_UID}
GID=${CURRENT_GID}
export UID
export GID

NODE18 := docker run -it --rm \
     		--user $(id -u):$(id -g) \
     		-v `pwd`:/usr/src/app \
            -w "/usr/src/app" node:18

.PHONY: prepare
prepare: ## Prepare environment
	@cd kong-ui && $(NODE18) yarn
	@docker compose buil

.PHONY: node
node: ## Run Node 18
	@$(NODE18) $(ARGS)

.PHONY: down
down: ## Stop all containers
	@docker compose down

.PHONY: up
up: ## start all containers
	@make down && docker compose up -d

.PHONY: build
build: ## build images
	@make down && docker compose build

.PHONY: ps
ps: ## List all containers
	@docker compose ps

.PHONY: logs
logs: ## log for one or all services
	@docker compose logs -f $(ARGS)


.PHONY: bash
bash: ## Login to bash container
	@docker compose exec $(ARGS) bash