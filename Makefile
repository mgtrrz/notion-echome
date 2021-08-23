APP_NAME := notion-echome
REGISTRY := registry.mk9.me:8443/mk9/

help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build docker image. Pass the version with VER=v.x.x.x
	docker build . -t ${REGISTRY}${APP_NAME}:$(if $(VER),$(VER),latest)

push: ## Push the docker image to the registry. Pass the version with VER=v.x.x.x
	docker push ${REGISTRY}${APP_NAME}:$(if $(VER),$(VER),latest)


.PHONY: build push
.DEFAULT_GOAL := help