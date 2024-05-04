echo "host    replication     replicator      all          md5" >> /var/lib/postgresql/data/pg_hba.conf

cp /var/lib/postgresql/data/postgresql.conf /var/lib/postgresql/data/postgresql.conf.orig

echo "ssl = off" >> /var/lib/postgresql/data/postgresql.conf
echo "wal_level = replica" >> /var/lib/postgresql/data/postgresql.conf
echo "max_wal_senders = 4" >> /var/lib/postgresql/data/postgresql.conf