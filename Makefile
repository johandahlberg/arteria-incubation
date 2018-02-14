# This file has been modified from the https://github.com/StackStorm/st2-docker repo
# It is therefore subject to Apache Licence 2.0.
# It has been modified to work with the specific Arteria services and workflow.

up:
	mkdir -p docker-mountpoints/bcl2fastq-output
	mkdir -p docker-mountpoints/monitored-folder
	mkdir -p docker-runtime/entrypoint.d
	mkdir -p docker-runtime/st2.d
	docker-compose up -d

down:
	docker-compose down

interact: up
	docker exec -it stackstorm /bin/bash

test-pack: up
	docker exec stackstorm st2-run-pack-tests -c -v -p /opt/stackstorm/packs/arteria

test-integration: up
	docker exec stackstorm /opt/stackstorm/packs/arteria/tests/integration_tests

exec:
	docker exec -it stackstorm $(cmd)

remove-all: down
	docker rmi $$(docker images -a -q)

clean: remove-all
	echo "Cleaned!"

remove-st2: down
	docker images -a  | grep stackstorm | awk '{print($$1)}' | xargs docker rmi
