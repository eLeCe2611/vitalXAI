import os

import mysql.connector


def get_db_connection():
    """Establece y devuelve la conexión a la base de datos MySQL."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "tfg_pneumonia")
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refresh_tokens (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        token_hash VARCHAR(255) NOT NULL,
        expires_at DATETIME NOT NULL,
        revoked BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()
    print("Base de datos inicializada: tablas training_jobs y refresh_tokens verificadas.")
