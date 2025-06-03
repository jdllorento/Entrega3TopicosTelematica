#!/bin/bash

# Parámetros
CLUSTER_NAME="OpenMeteo-AutoBatch"
BUCKET_NAME="open-meteo-bucket-batchproject"
REGION="us-east-1"
SCRIPT_PATH="s3://${BUCKET_NAME}/scripts/dataprep.py"
export PATH=$PATH:/usr/local/bin

# Crear clúster EMR
aws emr create-cluster \
  --name "$CLUSTER_NAME" \
  --release-label emr-7.9.0 \
  --applications Name=Hadoop Name=Spark \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --use-default-roles \
  --log-uri "s3://${BUCKET_NAME}/logs/" \
  --auto-terminate \
  --region $REGION \
  --steps Type=Spark,Name="DataPrepStep",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,"$SCRIPT_PATH"] \
  --visible-to-all-users