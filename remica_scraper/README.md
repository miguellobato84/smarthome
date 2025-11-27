# Remica Scraper

Script automatizado para extraer el consumo de radiadores desde la web de Remica y publicarlo en Home Assistant mediante MQTT.

## Características

- Login automático en el portal de clientes de Remica
- Extracción del consumo del último periodo de facturación
- Publicación automática en MQTT
- Integración automática con Home Assistant mediante MQTT Discovery
- Ejecución programada cada 24 horas

## Configuración

1. Copia el archivo de ejemplo de variables de entorno:
   ```bash
   cp remica_scraper/.env.example remica_scraper/.env
   ```

2. Edita el archivo `.env` con tus credenciales de Remica:
   ```bash
   REMICA_USERNAME=tu_usuario@email.com
   REMICA_PASSWORD=tu_contraseña
   ```

3. Construye y levanta el contenedor:
   ```bash
   cd compose
   docker-compose -f remica-scraper.yml up -d --build
   ```

## Uso Manual

Si quieres ejecutar el script manualmente sin Docker:

```bash
cd remica_scraper
pip install -r requirements.txt

# Configura las variables de entorno
export REMICA_USERNAME="tu_usuario@email.com"
export REMICA_PASSWORD="tu_contraseña"
export MQTT_BROKER="localhost"

python remica_scraper.py
```

## Integración con Home Assistant

El script publica automáticamente los datos en MQTT con Home Assistant Discovery, creando un sensor llamado `sensor.remica_consumo_radiadores`.

Los datos incluyen:
- **Consumo**: Consumo en kWh del último periodo
- **Periodo**: Fecha del periodo de facturación
- **Importe**: Importe de la factura
- **Last Update**: Fecha de última actualización

## Troubleshooting

Si el script no puede extraer los datos:

1. Revisa los logs del contenedor:
   ```bash
   docker logs remica-scraper
   ```

2. Verifica los screenshots guardados en `/docker/remica/`:
   - `remica_login_error.png`: Error en el login
   - `remica_page.png`: Página después del login
   - `remica_page.html`: HTML de la página para análisis

3. Ajusta los selectores CSS en el script según la estructura real de la página de Remica.

## Nota Importante

El script utiliza Selenium con Chrome headless. Es posible que necesites ajustar los selectores CSS en la función `extract_consumption_data()` según la estructura exacta de la web de Remica, ya que las páginas web pueden cambiar con el tiempo.

Los selectores actuales son genéricos y pueden necesitar ajustes específicos para tu caso.
