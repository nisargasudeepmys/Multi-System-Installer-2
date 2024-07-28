from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import DatabaseManager

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_inventory_connection():
    inventory_conn = sqlite3.connect('software_inventory.db')
    inventory_conn.row_factory = sqlite3.Row
    return inventory_conn

def get_inventory_tables():
    inventory_conn = get_inventory_connection()
    cur = inventory_conn.cursor()
    tables = cur.execute("SELECT name from sqlite_master where type='table'").fetchall()
    inventory_conn.close()
    return [table['name'] for table in tables]

@app.route('/machines', methods=['GET'])
def get_machines():
    conn = get_db_connection()
    machines = conn.execute('SELECT * FROM machines').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in machines])

@app.route('/scheduled-jobs', methods=['GET'])
def get_scheduled_job_list():
    conn = get_db_connection()
    scheduled_jobs = conn.execute('SELECT * FROM scheduled_jobs').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in scheduled_jobs])

@app.route('/completed-jobs', methods=['GET'])
def get_completed_job_list():
    conn = get_db_connection()
    completed_jobs = conn.execute('SELECT * FROM completed_jobs').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in completed_jobs])

@app.route('/software', methods=['GET'])
def get_software_list():
    conn = get_db_connection()
    software_repository = conn.execute('SELECT * FROM software_repository').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in software_repository])

@app.route('/tables', methods=['GET'])
def list_tables():
    tables = get_inventory_tables()
    return jsonify(tables)

def create_table_route(table):
    @app.route(f'/{table}', methods=['GET'], endpoint=f'get_{table}_data')
    def get_table_data():
        conn = get_inventory_connection()
        data = conn.execute(f'SELECT * FROM {table}').fetchall()
        conn.close()
        return jsonify([dict(row) for row in data])

tables = get_inventory_tables()
for table in tables:
    create_table_route(table)

@app.route('/admin-mail', methods=['GET'])
def get_admin_mail_list():
    conn = get_db_connection()
    admin_mail = conn.execute('SELECT * FROM admin_mail').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in admin_mail])

@app.route('/machines', methods=['POST'])
def create_machine_entry():
    try:
        data = request.get_json()
        machine_id = data["machine_id"]
        ip_address = data["ip_address"]
        port_no = data["port_no"]
        username = data["username"]
        os_type = data["os_type"]
        path = data["path"]
        email = data["email"]
        machine_type = data["machine_type"]
        password = data["password"]

        DatabaseManager("database.db").create_machine(machine_id, ip_address, port_no, username, os_type, path, email, machine_type, password)
        return jsonify({'message': 'Machine entry created successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/scheduled-jobs', methods=['POST'])
def create_scheduled_job_entry():
    data = request.get_json()
    machine_id = data["machine_id"]
    software_id = data["software_id"]
    scheduled_time = data["scheduled_time"]

    DatabaseManager("database.db").create_scheduled_job(machine_id, software_id, scheduled_time)
    return jsonify({'message': 'Scheduled job entry created successfully'})

@app.route('/software', methods=['POST'])
def create_software_entry():
    data = request.get_json()
    software_id = data["software_id"]
    name = data["name"]
    version = data["version"]
    description = data["description"]
    os_type = data["os_type"]
    extension = data["extension"]

    DatabaseManager("database.db").create_software(software_id, name, version, description, os_type, extension)
    return jsonify({'message': 'Software entry created successfully'})

@app.route('/admin-mail', methods=['POST'])
def add_admin_mail():
    try:
        data = request.get_json()
        email_id = data.get('email_id')
        smtp_server = data.get('smtp_server')
        port = data.get('port')
        api_token = data.get('api_token')
        DatabaseManager("database.db").create_admin_mail(email_id, smtp_server, port, api_token)
        return jsonify({'message': 'Admin mail entry created successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/machines/<int:machine_id>', methods=['DELETE'])
def delete_machine_entry(machine_id):
    try:
        DatabaseManager("database.db").delete_machine(machine_id)
        return jsonify({'message': 'Machine entry deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/scheduled-jobs/<int:job_id>', methods=['DELETE'])
def delete_scheduled_job_entry(job_id):
    try:
        DatabaseManager("database.db").delete_scheduled_job(job_id)
        return jsonify({'message': 'Scheduled job entry deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/admin-mail/<string:email_id>', methods=['DELETE'])
def delete_mail_entry(email_id):
    try:
        DatabaseManager("database.db").delete_mail(email_id)
        return jsonify({'message': 'Admin mail entry deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/software/<int:software_id>', methods=['DELETE'])
def delete_software_entry(software_id):
    try:
        DatabaseManager("database.db").delete_software(software_id)
        return jsonify({'message': 'Software entry deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
