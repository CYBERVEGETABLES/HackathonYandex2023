run:
	poetry run python src/main.py

docker-build:
	docker build -t alice_skill_study_nr .

docker-run:
	docker run --rm alice_skill_study_nr
