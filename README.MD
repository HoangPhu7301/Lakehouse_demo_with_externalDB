# 🏗️ Lakehouse with PostgreSQL, Hudi, Trino & Superset

## 📦 Stack:
- PostgreSQL (external DB)
- Apache Spark + Hudi
- Hive Metastore (with PostgreSQL backend)
- Trino
- MinIO
- Apache Superset (for visualization)

## ⚙️ Prerequisites

### 1. Apache Hive 3.1.3
```bash
wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
tar -xzf apache-hive-3.1.3-bin.tar.gz
```
- Copy required JAR files from `lib` folder to `hive/lib`

### 2. Hadoop 3.3.4
```bash
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
tar -xzf hadoop-3.3.4.tar.gz
```
- Make scripts executable after extraction
- Configure system permissions as needed

### 3. PostgreSQL Database Setup
- Create a database named `lakehouse_demo` (or your preferred name) using pgAdmin4
- Create two tables:
  - `car_sales`
  - `car_sales_updated`
- Use JDBC to connect Spark to PostgreSQL and ingest data

## 🛠️ How to run
```bash
#Start the docker container
docker compose up -d

#Run Spark ETL Pipeline
docker exec -it spark /opt/spark/bin/spark-submit \
  --packages org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  --driver-class-path /opt/spark/jars/postgresql-42.7.3.jar \
  --jars /opt/spark/jars/postgresql-42.7.3.jar \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  --master 'local[*]' \
  /spark/script.py

# Query with trino
docker exec -it trino trino
```

## 🌀 Airflow (optional orchestration)

This project can run fine without Airflow, but you can also bring up an Airflow
web UI to orchestrate the pipeline.

1. Start everything (including Airflow):

   ```bash
   docker compose up -d
   ```

2. Open Airflow UI at: <http://localhost:8081>

3. You should see a DAG called `lakehouse_spark_etl_example`. It currently uses
   simple `BashOperator` placeholders that just `echo` messages. You can edit
   `airflow/dags/lakehouse_spark_etl_example.py` to:

   - Replace the placeholder tasks with real `spark-submit` / Trino commands.
   - Or integrate with your existing ETL scripts.

Airflow is intended here as an optional local scheduler/visualizer. The core
lakehouse flow (Spark + Hudi + Trino + Superset) still works without it.