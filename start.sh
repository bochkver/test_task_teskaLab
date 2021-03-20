docker build -t containers-sql docker_build_sql
docker run --name first -d containers-sql

# it takes some time for mysql to come online, lets just wait a little bit
sleep 10
docker build -t containers-py docker_build_python
docker run --name second --link first:mysql -d containers-py
