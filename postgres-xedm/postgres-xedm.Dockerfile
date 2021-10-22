FROM postgres:12.2-alpine

COPY ./postgres-xedm/init_database.sql /docker-entrypoint-initdb.d