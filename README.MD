# 🏗️ Lakehouse with PostgreSQL, Hudi, Trino & Superset

## 📦 Stack:
- PostgreSQL (external DB)
- Apache Spark + Hudi
- Hive Metastore (with PostgreSQL backend)
- Trino
- MinIO
- Apache Superset (for visualization)


## Condition to run
1. **Apache Hive 3.1.3**
   wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
   tar -xzf apache-hive-3.1.3-bin.tar.gz

  copy needed file in lib folder to hive/lib to run 
2. **Hadoop 3.3.4**
    wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
    tar -xzf hadoop-3.3.5.tar.gz

    make sure to allow the script after decompress it and allow system in your system
3. **External DB**
    In this project, I create a DB in pgadmin4 tool using postgreSQL, and name it Lakehouse_demo(you can name it what ever you want)
    create two tables name: car_sales and car_sales_updated, and then using JDBC to connect to postgres and get data from it. 
    You can do the same with any data you got from postgres 
## 🛠️ How to run

```bash
#Start the docker container
docker compose up -d
#Run Spark ETL script
docker exec -it spark /opt/bitnami/spark/bin/spark-submit \
  --packages org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.1 \
  --jars /opt/bitnami/spark/jars/postgresql-42.7.3.jar \
  /spark/script.py

# Query with trino
docker exec -it trino trino
  ```