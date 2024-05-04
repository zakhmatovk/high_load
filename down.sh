
docker-compose -f docker/docker-compose.db.yaml -f docker/docker-compose.db-replica.yaml down
rm -rf docker/master-data

for number in 1 2
do
    # Очистим данные реплики
    rm -rf docker/replica$number-data
done