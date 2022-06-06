# Flight Management API

Flight and Aircraft Management API written with Django and DjangoRestFramework.

# Run Steps
## Locally With Docker [using postgres]
1. Clone this repository
2. run `cd flight-manager`
2. create a `.env` file and copy the contents of env.example file into it.
3. run `docker-compose up -d --build`
4. run `docker-compose exec backend sh` to enter the shell terminal.
5. run `python manage.py createsuperuser` to create a superuser.
## Locally Without Docker [using sqlite]
1. Clone the repository.
2. Run `cd flight-manager`
3. create a virtualenvironment and activate.
4. run `pip install -r requirements.txt`
5. open the `core/settings.py` file and uncomment the SQLITE DATABASE config to use sqlite.
6. create a `.env` file and add
```Javascript
SECRET_KEY = "dj_secret"
DEBUG = "TRUE"
ALLOWED_HOSTS = "*"
```
6. run `python manage.py migrate`
7. run `python manage.py runserver`
8. To test the code, run `python manage.py test`.
9. To create a superuser for testing run `python manage.py createsuperuser` and follow the prompts.


# PostMan Documentation
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0b41713ac23cb1a3e90b?action=collection%2Fimport#?env%5BFlight%20%7C%20Local%20Host%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cDovLzEyNy4wLjAuMTo4MDAwIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAiLCJzZXNzaW9uSW5kZXgiOjB9XQ==)

### PostMan Documentation Link
https://documenter.getpostman.com/view/13640451/Uz5JGaXW



# API Documentation

## Authorization

The API uses JWT Bearer Token For Authenticating Users.

To authenticate an API request, you should provide your JWT Token in the `Authorization` header. For example

```
{"Authorization": "Bearer <jwt access token>"}
```
`access` token expires every `24` hours and `refresh` token expires every `2 days`.

## API Response

The API response is in the following format:
```javascript
{
  "status": bool,
  "message": string,
  "data": json object | dictionary
}
```
- The `status` attribute describes if the api call was successfull or not.
- The `message` a short message for errors or successful requests.
- The `data` attribute contains any other metadata associated with the response. It may not be present.

## Status Codes

Gophish returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 401 | `UNAUTHORIZED` |
| 403 | `NOT PERMITTED` |
| 500 | `INTERNAL SERVER ERROR` |


## Login

```http
POST /api/login/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "email" : string,
  "password" : string
}
```

### Response

{
  "refresh": "string",
  "access": "string"
}

## Refresh Token

```http
POST /api/refresh_token/
```

### Authorization: No Auth

### Request Body

```javascript
{
  "refresh" : string
}
```

### Response
```javascript
{
  "access": "string"
}
```

## Create Aircraft
#### Endpoint to create Aircraft

```http
POST /api/aircraft/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| serial_number | `string` | `Yes`
| manufacturer | `string` | `Yes`


### Sample Request Body

```javascript
{
    "serial_number": string,
    "manufacturer": string
}
```

### Sample Response
```Javascript
{
    "uid": "0e42d487-5778-477d-82e2-9e3ba5db62ba",
    "created_at": "2022-06-05T22:33:21.461601Z",
    "updated_at": null,
    "serial_number": "JMFRIHPL",
    "manufacturer": "nuvolar"
}
```

## Fetch Aircrafts
#### Get All Aircrafts from the database

```http
GET /api/aircraft/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": [
        {
            "uid": "0e42d487-5778-477d-82e2-9e3ba5db62ba",
            "created_at": "2022-06-05T22:33:21.461601Z",
            "updated_at": null,
            "serial_number": "JMFRIHPL",
            "manufacturer": "nuvolar"
        }
    ]
}
```
## Update Aircraft
#### Endpoint to update an aircraft. Capable of performing partial or full update by specifying the fields to update.
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| serial_number | `string` | `No`
| manufacturer | `string` | `No`

```http
PUT /api/aircraft/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Request Body

```javascript
{
    "serial_number": string,
    "manufacturer": string
}
```

### Sample Response
```Javascript
{
    "uid": "0e42d487-5778-477d-82e2-9e3ba5db62ba",
    "created_at": "2022-06-05T22:33:21.461601Z",
    "updated_at": null,
    "serial_number": "JMFRIHPL",
    "manufacturer": "nuvolar"
}
```

## Retrieve Aicraft
#### Get Aircraft By ID

```http
GET /api/aircraft/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": {
        "uid": "0e42d487-5778-477d-82e2-9e3ba5db62ba",
        "created_at": "2022-06-05T22:33:21.461601Z",
        "updated_at": null,
        "serial_number": "JMFRIHPL",
        "manufacturer": "nuvolar"
    }
}
```

## Delete Aicraft

```http
DELETE /api/aircraft/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "message": "Deleted"
}
```

## Create Airport
#### Endpoint to create Airport

```http
POST /api/airport/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| name | `string` | `Yes`
| icao | `string` | `Yes`
| location | `json {lat, lng, area, city, country}` | `Yes`


### Sample Request Body

```javascript
{
    "name": "Aiport2", 
    "icao": "1Ej9", 
    "location": {
        "area": "Test Area2", 
        "city": "Test City2", 
        "country": "Test Country2", 
        "lat": "7.4968", 
        "lng": "6.7890"
    }
}
```

### Sample Response
```Javascript
{
    "uid": "5f66bc4b-66d2-4c1f-a87b-3864ab10cfa4",
    "location": {
        "id": 1,
        "area": "Test Area2",
        "city": "Test City2",
        "country": "Test Country2",
        "lat": "7.4968",
        "lng": "6.7890"
    },
    "created_at": "2022-06-05T22:53:31.635678Z",
    "updated_at": null,
    "name": "Aiport2",
    "icao": "1EJ9"
}
```
## Fetch Airports
#### Get All Airports from the database

```http
GET /api/airport/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": [
        {
            "uid": "5f66bc4b-66d2-4c1f-a87b-3864ab10cfa4",
            "location": {
                "id": 1,
                "area": "Test Area2",
                "city": "Test City2",
                "country": "Test Country2",
                "lat": "7.4968",
                "lng": "6.7890"
            },
            "created_at": "2022-06-05T22:53:31.635678Z",
            "updated_at": null,
            "name": "Aiport2",
            "icao": "1EJ9"
        }
    ]
}

```
## Update Airport
#### Endpoint to update an airport. Capable of performing partial or full update by specifying the fields to update.
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| name | `string` | `No`
| icao | `string` | `No`

```http
PUT /api/airport/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Request Body

```javascript
{
    "name": "Aiport",
    "icao": "1EC4"
}
```

### Sample Response
```Javascript
{
    "status": true,
    "message": "updated"
}
```

## Retrieve Airport
#### Get Aircraft By ID

```http
GET /api/airport/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": {
        "uid": "5f66bc4b-66d2-4c1f-a87b-3864ab10cfa4",
        "location": {
            "id": 1,
            "area": "Test Area2",
            "city": "Test City2",
            "country": "Test Country2",
            "lat": "7.4968",
            "lng": "6.7890"
        },
        "created_at": "2022-06-05T22:53:31.635678Z",
        "updated_at": "2022-06-05T22:56:56.902141Z",
        "name": "Aiport",
        "icao": "1EC4"
    }
}
```

## Delete Aicraft

```http
DELETE /api/airport/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "message": "Deleted"
}
```

## Create Flight
#### Endpoint to create Flight

```http
POST /api/flight/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| departure | `string` | `Yes`
| arrival | `string` | `Yes`
| airport | `json {lat, lng, area, city, country}` | `No`
| departure_dt | `datetime string format[%Y-%M-%D %H:%M]` | `Yes`
| arrival_dt | `datetime string format[%Y-%M-%D %H:%M]` | `Yes`

* All Datetime Strings Must be in UTC format.
### Sample Request Body

```javascript
{
    "departure": "1EC9",
    "arrival": "1EC9",
    "departure_dt": "2022-06-05 15:30",
    "arrival_dt": "2022-06-05 21:30",
    "status": "arrived"
}
```

### Sample Response
```Javascript
{
    "uid": "3c7710c2-9951-4f11-88b5-2af070f54578",
    "aircraft": null,
    "departure": "1EC4",
    "arrival": "1EJ2",
    "created_at": "2022-06-05T23:17:00.237653Z",
    "updated_at": null,
    "departure_dt": "2022-06-14T15:30:00Z",
    "arrival_dt": "2022-06-14T21:30:00Z",
    "status": "arrived"
}
```
## Fetch All Flights
#### Get All Flights from the database

```http
GET /api/flight/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": [
        {
            "uid": "30f758ab-870f-4616-89c4-bb4f32abd631",
            "aircraft": null,
            "departure": {
                "uid": "5f66bc4b-66d2-4c1f-a87b-3864ab10cfa4",
                "location": {
                    "id": 1,
                    "area": "Test Area2",
                    "city": "Test City2",
                    "country": "Test Country2",
                    "lat": "7.4968",
                    "lng": "6.7890"
                },
                "created_at": "2022-06-05T22:53:31.635678Z",
                "updated_at": "2022-06-05T22:56:56.902141Z",
                "name": "Aiport",
                "icao": "1EC4"
            },
            "arrival": {
                "uid": "95287024-d127-43d5-bec6-e9d6e319d251",
                "location": {
                    "id": 3,
                    "area": "Test Area2",
                    "city": "Test City2",
                    "country": "Test Country2",
                    "lat": "7.4968",
                    "lng": "6.7890"
                },
                "created_at": "2022-06-05T23:12:45.189404Z",
                "updated_at": null,
                "name": "Aiport2",
                "icao": "1EJ2"
            },
            "created_at": "2022-06-05T23:13:44.044456Z",
            "updated_at": null,
            "departure_dt": "2022-06-10T15:30:00Z",
            "arrival_dt": "2022-06-10T21:30:00Z",
            "status": "arrived"
        },
    ]
}

```
## Update Flight
#### Endpoint to update a flight. Capable of performing partial or full update by specifying the fields to update.
### Payload
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| arrival | `string` | `No`
| departure | `string` | `No`
| arrival_dt | `datetime string format[%Y-%M-%D %H:%M]` | `No`
| departure_dt | `datetime string format[%Y-%M-%D %H:%M]` | `No`
| status | `string <options (scheduled, cancelled, departed, arrived)>` | `No`

* Note: All DateTime strings are in UTC
```http
PUT /api/flight/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Request Body

```javascript
{
    "departure": "1EJ2",
    "arrival": "1EC4",
    "departure_dt": "2022-06-13 15:30",
    "arrival_dt": "2022-06-13 21:30",
    "status": "arrived"
}
```

### Sample Response
```Javascript
{
    "status": true,
    "message": "updated"
}
```

## Retrieve Flight
#### Get Flight By ID

```http
GET /api/flight/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "data": {
        "uid": "3c7710c2-9951-4f11-88b5-2af070f54578",
        "aircraft": null,
        "departure": {
            "uid": "95287024-d127-43d5-bec6-e9d6e319d251",
            "location": {
                "id": 3,
                "area": "Test Area2",
                "city": "Test City2",
                "country": "Test Country2",
                "lat": "7.4968",
                "lng": "6.7890"
            },
            "created_at": "2022-06-05T23:12:45.189404Z",
            "updated_at": null,
            "name": "Aiport2",
            "icao": "1EJ2"
        },
        "arrival": {
            "uid": "5f66bc4b-66d2-4c1f-a87b-3864ab10cfa4",
            "location": {
                "id": 1,
                "area": "Test Area2",
                "city": "Test City2",
                "country": "Test Country2",
                "lat": "7.4968",
                "lng": "6.7890"
            },
            "created_at": "2022-06-05T22:53:31.635678Z",
            "updated_at": "2022-06-05T22:56:56.902141Z",
            "name": "Aiport",
            "icao": "1EC4"
        },
        "created_at": "2022-06-05T23:17:00.237653Z",
        "updated_at": null,
        "departure_dt": "2022-06-13T15:30:00Z",
        "arrival_dt": "2022-06-13T21:30:00Z",
        "status": "arrived"
    }
}
```

## Delete Flight

```http
DELETE /api/flight/:uid/
```

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### Sample Response
```Javascript
{
    "status": true,
    "message": "Deleted"
}
```

## Flight Search

Search Flight By departure, arrival and departure time range

### Authorization: Bearer Auth e.g `Bearer <jwt_access_token>`

### QUERY PARAMS
| Field Name | Data Type | Required |
| :--- | :--- | :--- |
| dept | `string` | `No`
| arr | `string` | `No`
| dept_rng | `time range string` | `No`

### Search By Arrival Airport ICAO code
```http
GET /api/flight/search/?arr=1ec9
```

### Search By Departure Airport ICAO code
```http
GET /api/flight/search/?dept=1ec9
```

### Search By Departure Time Range
```http
GET /api/flight/search/?dept_rng=10:30;2:30
```

