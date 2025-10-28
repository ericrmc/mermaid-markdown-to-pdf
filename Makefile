.PHONY: build run shell clean help

IMAGE_NAME := markdown-pdf-converter:latest
MOUNT_DIR := $(shell pwd)

help:
	@echo "Markdown to PDF Converter - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make build          Build the container image"
	@echo ""
	@echo "Usage:"
	@echo "  make run FILE=README.md                    Convert single file"
	@echo "  make run FOLDER=docs/                      Convert all files in folder"
	@echo "  make run FOLDER=docs/ OUTPUT=pdfs/         Convert with custom output dir"
	@echo "  make run ARGS='--check-deps'               Check dependencies"
	@echo ""
	@echo "Debugging:"
	@echo "  make shell          Open interactive shell in container"
	@echo "  make clean          Remove built image"

build:
	podman build -t $(IMAGE_NAME) .

run:
ifdef FILE
	podman run --rm -v $(MOUNT_DIR):/workspace:Z --userns=keep-id $(IMAGE_NAME) $(FILE) $(ARGS)
else ifdef FOLDER
ifdef OUTPUT
	podman run --rm -v $(MOUNT_DIR):/workspace:Z --userns=keep-id $(IMAGE_NAME) --folder $(FOLDER) --output-dir $(OUTPUT) $(ARGS)
else
	podman run --rm -v $(MOUNT_DIR):/workspace:Z --userns=keep-id $(IMAGE_NAME) --folder $(FOLDER) $(ARGS)
endif
else ifdef ARGS
	podman run --rm -v $(MOUNT_DIR):/workspace:Z --userns=keep-id $(IMAGE_NAME) $(ARGS)
else
	@echo "Error: Please specify FILE=, FOLDER=, or ARGS="
	@echo "Examples:"
	@echo "  make run FILE=README.md"
	@echo "  make run FOLDER=docs/"
	@echo "  make run ARGS='--help'"
	@exit 1
endif

shell:
	podman run --rm -it -v $(MOUNT_DIR):/workspace:Z --userns=keep-id --entrypoint /bin/bash $(IMAGE_NAME)

clean:
	podman rmi $(IMAGE_NAME)
