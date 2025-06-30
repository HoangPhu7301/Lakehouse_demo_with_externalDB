```bash
docker exec -it spark /opt/bitnami/spark/bin/spark-submit \
  --packages org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.1 \
  --jars /opt/bitnami/spark/jars/postgresql-42.7.3.jar \
  /spark/script.py

  docker exec -it trino trino
  ```
  