Online Reservation System
====================

A 3-tiered web application for mass meeting reservation 

## Prerequisite

- Docker 19.03.0+
- Docker-compose 1.25.5+
- GNU make

## Development Quick Start

1. copy `.env.sample` to `.env` and modify the configuration. 
2. Run command 
   ```sh
   docker-compose build
   docker-compose up
   ```
3. While docker-compose is running, ```docker-compose up```, open another terminal and run the following command to finish the setup
   ```sh
   make migrate-db
   make add-super-user   
   ```

## Maintaince
The following actions required docker-compose to be running, ```docker-compose up```,
open another terminal and run maintaince command there.

### Create database migration

```sh
make migrate-db
```

### Upgrade database schema

```sh
make create-migration
```

### Add Django-superuser

```sh
make add-super-user
```

## Authors

Developer List:
1. Ho Wang Howard LAI
2. Qixin WANG

## Remark
This project starts as the capstone project for Ho Wang Howard LAI in 2020 Fall semester,
where Qixin Wang is the supervisor. 
