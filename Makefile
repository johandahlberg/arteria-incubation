
up:
	docker-compose up -d

down:
	docker-compose down

interact:
	docker exec -it stackstorm /bin/bash

exec:
	docker exec -it stackstorm $(cmd)

remove-all:
	docker rmi $$(docker images -a -q)

clean: down remove-all

remove-st2: down
	docker images -a  | grep stackstorm | awk '{print($$1)}' | xargs docker rmi
