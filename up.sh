# Дадим права на запуск скриптов, права тоже копируются в контейнер
chmod +x docker/master-conf/10_update_conf.sh 
chmod +x docker/replica1-conf/10_update_conf.sh 

# запустим мастер постгри
docker-compose -f docker/docker-compose.db.yaml up -d
docker exec pgmaster mkdir /pgslave
sleep 5
# создадим бекап
echo 'select pg_reload_conf();'| docker exec -i pgmaster su - postgres -c psql
echo "pass" | docker exec -i pgmaster pg_basebackup -h pgmaster -D /pgslave -U replicator -v -P --wal-method=stream

for number in 1 2
do
    # Очистим данные реплики
    rm -rf docker/replica$number-data
    docker cp pgmaster:/pgslave docker/replica$number-data/
    touch docker/replica$number-data/standby.signal
    # восстановим postgres.conf на реплике
    rm -rf docker/replica$number-data/postgresql.conf
    cp docker/replica$number-data/postgresql.conf.orig docker/replica$number-data/postgresql.conf

    # дополним конфиг реплики
    echo "listen_addresses = '*'" >> docker/replica$number-data/postgresql.conf
    echo "hot_standby = on" >> docker/replica$number-data/postgresql.conf
    echo "primary_conninfo = 'host=pgmaster port=5432 user=replicator password=pass application_name=pgreplica$number'" >> docker/replica$number-data/postgresql.conf
done

# Запустим реплики
docker-compose -f docker/docker-compose.db.yaml -f docker/docker-compose.db-replica.yaml up -d

# Проверим статус реплик
sleep 5
echo 'select application_name, sync_state from pg_stat_replication;'| docker exec -i pgmaster su - postgres -c psql