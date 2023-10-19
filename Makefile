build:
	docker build -t aiogram_bot .

run:
	docker run -it --name aiogram_bot aiogram_bot