# scripts/load_data.py

import pandas as pd
import psycopg2
import os

def load_data_to_db():
    """
    Carga datos del archivo CSV en la base de datos PostgreSQL.
    """
    try:
        # Credenciales de la base de datos desde variables de entorno
        db_host = os.environ['DB_HOST']
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        db_name = os.environ['DB_NAME']
        
        # Conexión a la base de datos
        conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname=db_name)
        cur = conn.cursor()

        # Crear la tabla si no existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                Airline VARCHAR(255),
                Date_of_Journey DATE,
                Source VARCHAR(255),
                Destination VARCHAR(255),
                Route VARCHAR(255),
                Dep_Time VARCHAR(255),
                Arrival_Time VARCHAR(255),
                Duration VARCHAR(255),
                Total_Stops VARCHAR(255),
                Additional_Info TEXT,
                Price INT
            );
        """)
        conn.commit()

        # Leer el archivo CSV
        df = pd.read_csv('data/IndianFlightdata - Sheet1.csv')
        
        # Convertir el DataFrame a una lista de tuplas para una carga eficiente
        records = [tuple(row) for row in df.itertuples(index=False)]

        # Insertar datos en la tabla
        for record in records:
            cur.execute("INSERT INTO flights VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", record)
        
        conn.commit()
        print("Datos cargados exitosamente.")

    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    load_data_to_db()