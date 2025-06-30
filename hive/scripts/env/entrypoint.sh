#!/bin/bash
set -e

echo "===> Starting Hive Metastore initialization..."

# Set Hadoop environment variables
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=/opt/hive/conf
export HADOOP_CLASSPATH=/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/common/*
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Check if Hadoop exists
if [ ! -d "$HADOOP_HOME" ]; then
    echo "ERROR: Hadoop not found at $HADOOP_HOME"
    echo "Available directories in /opt:"
    ls -la /opt/
    exit 1
fi

# Wait for DB to be ready
echo "Waiting for PostgreSQL to be available..."
until timeout 1 bash -c "cat < /dev/null > /dev/tcp/$DB_HOST/$DB_PORT"; do
  echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
  sleep 2
done
echo "PostgreSQL is ready!"

# Run schema if not already done
if [ ! -f /metastore_initialized ]; then
  echo "===> Initializing Hive schema with PostgreSQL..."
  
  # Debug: Check what's available
  echo "HADOOP_HOME: $HADOOP_HOME"
  echo "Contents of HADOOP_HOME:"
  ls -la $HADOOP_HOME/ || echo "HADOOP_HOME directory not found"
  
  # Try schema initialization
  /opt/hive/bin/schematool -dbType postgres -initSchema || {
    echo "Schema initialization failed!"
    exit 1
  }
  touch /metastore_initialized
fi

echo "===> Checking and creating Hive default database..."
/opt/hive/bin/hive -e "CREATE DATABASE IF NOT EXISTS default;" || 
{
  echo "Failed to create default database!"
  exit 1
}

# Start metastore
echo "===> Starting Hive Metastore service..."
exec /opt/hive/bin/hive --service metastore