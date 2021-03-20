FROM mysql:latest
COPY containers.sql /docker-entrypoint-initdb.d/
# ENV MYSQL_DATABASE containers_db
ENV MYSQL_ROOT_PASSWORD qwerty
#RUN mysql < containers.sql 
EXPOSE 3306 
