# Utiliza una imagen base oficial de Python
FROM python:3.11-slim

# Instala netcat-openbsd para wait-for.sh
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Copia el archivo de variables de entorno (opcional)
COPY BD.env ./

# Copia el script wait-for.sh
COPY wait-for.sh /wait-for.sh
RUN chmod +x /wait-for.sh

# Expone el puerto en el que corre Flask
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["/wait-for.sh", "mysql", "python", "app.py"] 