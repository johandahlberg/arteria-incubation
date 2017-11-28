
up:
	docker-compose up -d

down:
	docker-compose down

interact: up
	docker exec -it stackstorm /bin/bash

exec:
	docker exec -it stackstorm $(cmd)

remove-all: down
	docker rmi $$(docker images -a -q)

clean: remove-all
	echo "Cleaned!"

remove-st2: down
	docker images -a  | grep stackstorm | awk '{print($$1)}' | xargs docker rmi
