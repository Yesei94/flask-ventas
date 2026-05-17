# flask-ventas

Sistema web de gestión de ventas desarrollado con **Python**, **Flask**, **SQLAlchemy** y **Flask-AppBuilder**.

## Stack
- Python 3.13
- Flask + Flask-AppBuilder
- SQLAlchemy / Flask-SQLAlchemy
- MySQL (vía PyMySQL)
- Chart.js para gráficas

## Cómo levantar el proyecto

```powershell
# 1. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear base de datos MySQL "examen2"
#    En MySQL: CREATE DATABASE examen2;

# 4. Crear usuario admin
$env:FLASK_APP = "run.py"
flask fab create-admin

# 5. Levantar
python run.py
```

Acceder en [http://localhost:8080](http://localhost:8080)
