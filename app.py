from flask import Flask, jsonify
import boto3
import time

app = Flask(__name__)

# Parámetros de configuración
ATHENA_DB = "openmeteo"
ATHENA_OUTPUT = "s3://open-meteo-bucket-batchproject/results/"
QUERY_STRING = "SELECT * FROM refined_descriptive_stats;"

# Cliente de boto3 para Athena
athena = boto3.client('athena')

def run_athena_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': ATHENA_DB},
        ResultConfiguration={'OutputLocation': ATHENA_OUTPUT}
    )
    return response['QueryExecutionId']

def wait_for_query(query_execution_id):
    while True:
        response = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = response['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            return state
        time.sleep(1)

def get_query_results(query_execution_id):
    result = athena.get_query_results(QueryExecutionId=query_execution_id)
    headers = [col['Name'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    rows = result['ResultSet']['Rows'][1:]  # Omitir encabezado

    results = []
    for row in rows:
        data = {}
        for i, cell in enumerate(row['Data']):
            data[headers[i]] = cell.get('VarCharValue', None)
        results.append(data)
    return results

@app.route('/stats', methods=['GET'])
def stats():
    try:
        query_id = run_athena_query(QUERY_STRING)
        state = wait_for_query(query_id)

        if state == 'SUCCEEDED':
            results = get_query_results(query_id)
            return jsonify(results)
        else:
            return jsonify({"error": f"Query failed with state {state}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
