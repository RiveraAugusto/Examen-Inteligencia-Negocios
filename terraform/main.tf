# main.tf

# Configuración del proveedor de Google Cloud
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Configuración del proyecto y la región
provider "google" {
  project = "single-station-472604-t8"  # ID real de tu proyecto
  region  = "southamerica-east1"        # Región recomendada para Sudamérica (São Paulo)
}

# Habilitar la API de Cloud SQL
  project            = "single-station-472604-t8"
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

# Crear una instancia de Cloud SQL para PostgreSQL
resource "google_sql_database_instance" "flight_database" {
  name             = "flight-price-dataset-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier      = "db-f1-micro"
    disk_size = 10
    disk_type = "PD_SSD"
    
    ip_configuration {
      ipv4_enabled    = true
      require_ssl     = false
      authorized_networks {
        value = "0.0.0.0/0"
      }
    }
  }
}

# Crear una base de datos dentro de la instancia
resource "google_sql_database" "flight_db" {
  name     = "flightpricedataset"
  instance = google_sql_database_instance.flight_database.name
}

# Crear un usuario de base de datos
  name     = "admin"
  instance = google_sql_database_instance.flight_database.name
  password = "Upt2025" # ¡No uses esto en producción! Usa Google Secrets Manager.
}

# Exportar el endpoint de la base de datos
output "db_ip_address" {
  value = google_sql_database_instance.flight_database.ip_address.0.ip_address
}