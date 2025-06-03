#!/bin/bash

# === CONFIGURACIÓN ===
INGEST_SCRIPT="/home/ubuntu/ingest_open_meteo.py"
EMR_LAUNCH_SCRIPT="/home/ubuntu/launch_emr_cluster.sh"
LOG_DIR="/home/ubuntu/pipeline_logs"
DATE=$(date +%Y-%m-%d)

mkdir -p "$LOG_DIR"

echo "📥 [$DATE] Iniciando proceso de INGESTA..." | tee -a "$LOG_DIR/pipeline_$DATE.log"
python3 $INGEST_SCRIPT >> "$LOG_DIR/ingesta_$DATE.log" 2>&1

echo "🚀 [$DATE] Iniciando lanzamiento del CLUSTER EMR..." | tee -a "$LOG_DIR/pipeline_$DATE.log"
bash $EMR_LAUNCH_SCRIPT >> "$LOG_DIR/emr_$DATE.log" 2>&1

echo "✅ [$DATE] Proceso completo." | tee -a "$LOG_DIR/pipeline_$DATE.log"