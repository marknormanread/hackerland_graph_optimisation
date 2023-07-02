IMAGE_NAME = hackerland
WORKING_DIR = $(shell pwd)

docker-build:
	docker build -t $(IMAGE_NAME) .

# This mounds the current working directory (where this makefile resides) to /home in the container. 
docker-run:
	docker run -it --rm -v $(WORKING_DIR):/home $(IMAGE_NAME)