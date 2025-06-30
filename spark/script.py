from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# Tạo Spark session
spark = SparkSession.builder \
    .appName("pgAdmin_to_Hudi_ETL") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.hudi.catalog.HoodieCatalog") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Cấu hình PostgreSQL
jdbc_url = "jdbc:postgresql://host.docker.internal:5432/Lakehouse_demo"
jdbc_properties = {
    "user": "postgres",
    "password": "931943",
    "driver": "org.postgresql.Driver"
}

# Danh sách bảng và cấu hình tương ứng
tables = [
    {
        "source_table": "public.car_sales",
        "hudi_table": "car_sales",
        "recordkey": "id",
        "precombine": "year",
        "path": "s3a://carsalesdata/car_sales"
    },
    {
        "source_table": "public.car_sales_updated",
        "hudi_table": "car_sales_updated",
        "recordkey": "id",
        "precombine": "year",
        "path": "s3a://carsalesdata/car_sales_updated"
    }
]

# Lặp qua từng bảng để ingest
for t in tables:
    print(f"\n🚗 Ingesting table: {t['hudi_table']}")

    df = spark.read.jdbc(url=jdbc_url, table=t["source_table"], properties=jdbc_properties)
    df = df.select([F.col(c).alias(c.replace(" ", "_").lower()) for c in df.columns])

    df.write.format("hudi") \
        .option("hoodie.table.name", t["hudi_table"]) \
        .option("hoodie.datasource.write.recordkey.field", t["recordkey"]) \
        .option("hoodie.datasource.write.precombine.field", t["precombine"]) \
        .option("hoodie.datasource.write.operation", "insert") \
        .option("hoodie.datasource.hive_sync.enable", "true") \
        .option("hoodie.datasource.hive_sync.mode", "hms") \
        .option("hoodie.datasource.hive_sync.metastore.uris", "thrift://hive-metastore:9083") \
        .option("hoodie.datasource.hive_sync.table", t["hudi_table"]) \
        .option("hoodie.datasource.hive_sync.database", "default") \
        .option("hoodie.datasource.hive_sync.support_timestamp", "true") \
        .option("path", t["path"]) \
        .mode("overwrite") \
        .save()

    # Kiểm tra Hive Metastore đã sync chưa
    try:
        spark.sql(f"DESC TABLE default.{t['hudi_table']}")
        print(f"✅ Hive table `{t['hudi_table']}` is signup.")
    except Exception:
        print(f"⚠️ Hive table `{t['hudi_table']}` none exist, need create...")
        spark.sql(f"""
        CREATE TABLE default.{t['hudi_table']}
        USING hudi
        LOCATION '{t["path"]}'
        """)
        print(f"✅ hive table create complete `{t['hudi_table']}`.")

print("\n✅ Ingestion to Hudi and Hive sync complete.")