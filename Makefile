PROJECT_NAME=$(notdir $(CURDIR))
VERSION=$(shell date "+%Y%m%d.%H%M%S")

.PHONY: help
help:
	@echo "help              this help"
	@echo "build             build project with date as version"
	@echo "clean             rm build output"
	@echo "deploy            running server"

.PHONY: build
build:
	mkdir -p build
	GOPATH=$(CURDIR) go build -ldflags "-s -w -X main.version=$(VERSION)" -o build/$(PROJECT_NAME) src/$(PROJECT_NAME)/*.go
	cp build/$(PROJECT_NAME) build/$(PROJECT_NAME)_v$(VERSION)
	# cp deploy/settings.ini build/

.PHONY: clean
clean:
	rm -rf .tmp
	rm -rf ./build
