# GoCEP Python API

A zip code service.

## Features

With this API:
- Can consult address by zip code number.
- Can consult address by query params: "federated_state", "city" and "street"

### Requirements

Aplication uses:

- Python 3
- Django 3.0.4
- Django Rest Framework 3.11.0

### Clone the repository
```
git clone https://github.com/marlonleite/goCep.git
```

### Installation

Virtualenv:
```
python3 --version
python3 -m venv venv
source venv/bin/activate
 
pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Docker:
```
Create:
docker-compose up -d

Access:
http://127.0.0.1:8999

Drop:
docker-compose down

```

## How it works:

Trying the rest routes:

```
GET /api/<int:zip_code>/
```
or
```
GET /api/?federated_state=<string>&city=<string>&street=<string>/
```

```
Response:
{
    "zip_code": <string>,
    "federated_state": <string>,
    "city": <string>,
    "street": <string>,
    "neighborhood": <string>
}
```

## Running the tests

Some tests were done in the application. 
Test request by zip code. Test by street address, city and federation state. 
Expected returns status of the application.

Go there:
```
./manage.py test
```

## Live Previews

* [http://gocep.marlonleite.com.br/api/](http://gocep.marlonleite.com.br/api/)

## Authors

* **Marlon Leite** - [GitHub](https://github.com/marlonleite)

