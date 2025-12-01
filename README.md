# Application Overview

## Application Logic

This app logic is very simple, as it is not the main focus.

The app exposes an API for the enduser and connects with a MySQL database.

The theme of the app is 'reviews'. You write the name and rating out of 5 through a POST endpoint. And you can retrieve the value from GET endpoints.

### APP Endpoints

`/review/new` - This is the POST endpoint.

It takes the data in the below format

data = {
    'Name' = 'name_value',
    'Rating' = 4
}

`/review/` - This is a GET endpoint. Used to retrieve all revies.

`/review/name/<Name:str>` - This is a GET endpoint. Used to retrieve a specific review from the database.

`/review/Rating/<Rating:int>` - This is a GET endpoint. Used to retrieve all reviews with a specific rating.


### Monitoring Endpoints

There will be readiness, liveness and startup probes. Each probe will communicate with an API Endpoint.

All API endpoints will begin with `/metrics`

* More details will be included later

## Containerization

There will be a docker container named 'Reviews' for the API logic. It will be running on port 5000.

As for the MySQL database, i will use the docker container `mysql:8.0.44-debian`.

The app will initialize a table once connected to the database.

## Kubernetes

The kubernetes part will be split into 3 parts.

1- The Application Logic
2- The Database
3- Monitoring and Logging

### Application logic

I will deploy the application using a Deployment with 3 pods.

I will expose the the application using a NodePort Service or Loadbalancer for the external communication

I will also expose the application using a clusterIP service for the monitoring and logging.

### The Database

I will deploy the database using a statefulset with 1-3 pods.

I will expose the database using a headless serice for the application.

I will configure the root and an additional user for the application to use. 

### Monitoring and Logging

This is empty for now.