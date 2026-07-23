import mysql.connector


def get_db_connection():
    """Establece y devuelve la conexión a la base de datos MySQL (XAMPP)."""
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Usuario por defecto en XAMPP
        password="",        # Contraseña por defecto
        database="tfg_pneumonia"
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        dataset_path VARCHAR(500),
        model_name VARCHAR(100),
        status VARCHAR(50) DEFAULT 'In Progress',
        progress FLOAT DEFAULT 0.0,
        metrics_json TEXT,
        started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        finished_at DATETIME NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Base de datos inicializada: tabla training_jobs verificada.")
