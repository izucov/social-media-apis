# Social Media APIs for AccuKnox


## Steps to Run via Docker Compose

1. Build the image, and run the contains for both django app and postgres db
    ```bash
    docker-compose up -d --build
    ```

2. Open a separate terminal on the same machine, and run the migrations
    ```bash
    docker-compose exec web python manage.py migrate --noinput
    ```

## Steps to run without Docker
1. Spin up a Postgres server, and update the `.env` with right details
2. Create a virtual environment using :
    ```bash
    virtualenv -p python3.8 venv
    ```
3. Activate the environment :
    ```bash
    source venv/bin/activate
    ```
4. Install the dependencies :
    ```bash
    pip install -r requirements.txt
    ```
5. Run the migrations :
    ```bash
    python manage.py migrate
    ```
6. Run the Server :
    ```bash
    python manage.py runserver
    ```

## Scope of Further development
Following things can be further added to this project.
- Two factor authentication system
- More resilient server with Gunicon WSGI server, and reverse proxy
- Add more social media APIs

## More related links
- [Postman API Collection](https://api.postman.com/collections/2686731-62469d9c-0722-4ffc-b7d3-9b9a4ff3a596?access_key=PMAT-01HN11PX8D60N649MPJ8J95MB0)
- [Redoc Documentation for Social Media APIs](/api/schema/redoc/#tag/search)
- [Swagger/Open API 2 Spec for Social Media APIs](/api/schema/swagger-ui/)