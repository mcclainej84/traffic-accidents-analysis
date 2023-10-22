# 🚘 Proyecto de Análisis de Accidentes de Tráfico 🚘

# Índice

1. [Proyecto de Análisis de Accidentes de Tráfico](#proyecto-de-análisis-de-accidentes-de-tráfico)
   - 1.1. [Fuentes Principales del Proyecto](#fuentes-principales-del-proyecto)
   
2. [Proyecto de Enriquecimiento](#proyecto-de-enriquecimiento)
   - 2.1. [Stack Tecnológico](#stack-tecnológico)
   - 2.2. [Configuración](#configuración)
   - 2.3. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
   - 2.4. [Archivos y Carpetas en `project`](#archivos-y-carpetas-en-project)
      - 2.4.1. [Subcarpeta `Files`](#subcarpeta-files)
      - 2.4.2. [Subcarpeta `Notebooks`](#subcarpeta-notebooks)
   
3. [Streamlit](#streamlit)
   - 3.1. [Stack Tecnológico](#stack-tecnológico)
   - 3.2. [Configuración](#configuración)
      - 3.2.1. [Modos de Uso](#modos-de-uso)
   - 3.3. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
   - 3.4. [Construir una imagen de Docker](#construir-una-imagen-de-docker)
      - 3.4.1. [Construir una imagen de Docker en modo local](#construir-una-imagen-de-docker-en-modo-local)
      - 3.4.2. [Publicar la imagen y ejecutarla en AWS mediante ECR](#publicar-la-imagen-y-ejecutarla-en-aws-mediante-ecr)
   - 3.5. [Archivos y Carpetas en `streamlit`](#archivos-y-carpetas-en-streamlit)
      - 3.5.1. [Carpeta `source`](#carpeta-source)
         - 3.5.1.1. [Subcarpeta `img`](#subcarpeta-img)
         - 3.5.1.2. [Subcarpeta `data`](#subcarpeta-data)

4. [Configuración y Ejecución](#configuración-y-ejecución)
5. [Contribuciones](#contribuciones)

# Proyecto de Análisis de Accidentes de Tráfico

Este repositorio alberga un proyecto de análisis de datos de accidentes de tráfico en la ciudad de Madrid. El objetivo principal de este proyecto es comprender mejor las causas de los accidentes de tráfico en Madrid. El proyecto se organiza en tres carpetas principales.

## 1. Fuentes Principales del Proyecto

Las fuentes de datos principales para este proyecto provienen del portal de datos abiertos de la Comunidad de Madrid y son de acceso público. Los datos utilizados en este proyecto abarcan desde enero hasta mayo de 2023. A continuación, se detallan los enlaces a las fuentes de datos originales:

  ### 1.1. Accidentes en la Ciudad de Madrid
  [Datos de Accidentes](http://datos.munimadrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=7c2843010d9c3610VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

  ### 1.2. Histórico del Tráfico en la Ciudad de Madrid
  [Histórico de Tráfico](http://datos.munimadrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

  ### 1.3. Ubicación de Puntos de Medida del Tráfico en la Ciudad de Madrid
  [Puntos de Medida de Tráfico](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?page=1&vgnextoid=ee941ce6ba6d3410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD)

  ### 1.4. Distritos Municipales de Madrid
  [Distritos Municipales](https://geoportal.madrid.es/IDEAM_WBGEOPORTAL/dataset.iam?id=541f4ef6-762b-11e9-861d-ecb1d753f6e8)

  ### 1.5. Barrios Municipales de Madrid
  [Barrios Municipales](https://geoportal.madrid.es/IDEAM_WBGEOPORTAL/dataset.iam?id=422fa235-762b-11e9-861d-ecb1d753f6e8)

## 2. Proyecto de Enriquecimiento

La carpeta `project` contiene el código y los recursos relacionados con un trabajo de enriquecimiento y limpieza de los datos diseñado para procesar datos ubicados en la carpeta `project/Files`.

  ### 2.1. Stack Tecnológico

  - **Lenguaje de Programación:** Python
  - **Bibliotecas Relevantes:** Pandas, Geopandas, json, pyproj, requests, configparser, numpy, os

  ### 2.2. Configuración

  Para la ejecución de las llamadas a las APIs correspondientes es necesario tener la API_KEY facilitada por los responsables de la API correspondiente y añadida en su sección dentro del fichero `api_keys.cfg`.

  ### 2.3. Ejecución de la Aplicación

  La ejecución del programa principal se realiza a través del fichero `main.py`.

  ### 2.4. Archivos y Carpetas en `project`

  - **requirements.txt**: Lista de dependencias de Python para el proyecto de enriquecimiento de los datos.
  - **api_keys.cfg**: Fichero de configuración para las llamadas a las APIs.
  - **main.py**: Programa principal del proyecto.
  - **coordinates_data.py**: Programa para obtener las coordenadas en formato Latitud/Longitud.
  - **geolocation_data.py**: Llamada a la API de geolocalización.
  - **speed_data.py**: Llamada a la API para obtener datos de Velocidad máxima.
  - **density.py**: Programa para aplicar conjunto de datos de densidad a los accidentes.
  - **clean_data.py**: Programa encargado de la limpieza del dataset final.
  - **Files**: Carpeta que contiene archivos de datos en formato CSV y GeoJSON utilizados en el proyecto.
  - **Notebooks**: Carpeta que contiene archivos de Jupyter Notebook utilizados para el análisis de datos y realización de pruebas de concepto.

  ### 2.4.1 Subcarpeta `Files`

  - **2023_Accidentalidad_schema.json**: Esquema del Dataset de accidentes.
  - **geodata_array.csv**: Conjunto de datos de la API de Geolocalización.
  - **speed_array.csv**: Conjunto de datos de la API de Velocidad máxima.
  - **geodata_array_raw.json**: Datos en bruto de la API de Geolocalización.
  - **speed_array_raw.json**: Datos en bruto de la API de Velocidad máxima.
  - **Distritos_de_Madrid.geojson**: Conjunto de datos con la información geoespacial de los Distritos de Madrid.
  - **2023_Accidentalidad.csv**: Conjunto de datos de accidentes.  
  - **2023_Accidentalidad.csv**: Conjunto de datos original de los Accidentes de la Ciudad de Madrid.
  - **2023_Accidentalidad_c_g_s_d_clean.csv**: Conjunto de datos enriquecido y limpiado de los Accidentes de la Ciudad de Madrid.
  - **2023_Accidentalidad_predicciones.csv**: Conjunto de datos utilizado para las predicciones.  
  - **density**: Carpeta que contiene archivos relacionados con el análisis de densidad de datos.
  - **Barrios**: Carpeta que almacena datos geoespaciales relacionados con los barrios de Madrid.

  ℹ️ No se han incluido los archivos intermedios de cada uno de los pasos de enriquecimiento ya que se pueden generar fácilmente a partir del dataset original. ℹ️

  ### 2.4.2 Subcarpeta `Notebooks`

  La carpeta `Notebooks` contiene archivos de Jupyter Notebook utilizados para el análisis de datos y realización de pruebas de concepto.

  ### Stack Tecnológico

  - **Lenguaje de Programación:** Python
  - **Bibliotecas Relevantes:** Pandas, Geopandas, json, pyproj, requests, configparser, numpy, os, sklearn
  - **Entorno de Desarrollo:** Jupyter Notebook

  ### Cuadernos en `Notebooks`

  - **analisis_barrios.ipynb**: Analisis de los datos por barrios.
  - **map_quarter.html**: Mapa de ejemplo.
  - **Limpieza_dataset_accidentes.ipynb**: Pruebas, exploración y análisis del dataset de accidentes.
  - **densidad_test.ipynb**: Pruebas y exploración de los datos de densidad y accidentes.
  - **Proyecto Detección Accidentes de Tráfico.ipynb**: Libreta que contiene la generacion del conjunto de datos predictivo.

## 3. Streamlit

La carpeta `streamlit` contiene archivos necesarios para la creación de una aplicación Streamlit y construir una imagen de Docker para poder ejecutarla en entornos locales con datos en AWS o lanzarla desde un Cluster de ECS.

### 3.1. Stack Tecnológico

- **Lenguaje de Programación:** Python
- **Biblioteca principal de gestión de la aplicación:** Streamlit
- **Bibliotecas para Visualización de Datos:** Folium, branca
- **Gestión de Almacenamiento en la Nube y Procesamiento de Archivos:** Boto3, base64
- **Manipulación de Conjuntos de Datos:** geopandas, pandas, json
- **Librerías Auxiliares Adicionales:** datetime, functools, calendar
- **Gestión de Contenedores:** Docker

### 3.2. Configuración

### 3.2.1 Modos de Uso

- **Local**: Si la constante 'LOCAL' se establece en 'True' en el fichero `file_aux.py`, la aplicación accede a los archivos de forma local en sus respectivas ubicaciones (únicamente para pruebas locales).
- **Híbrido**: A través del fichero de credenciales 'aws_credentials', la aplicación se ejecuta tanto localmente como en un entorno externo a AWS. Si el fichero 'aws_credentials' está configurado correctamente, se permite el acceso remoto al Bucket de S3 para cargar datos.
- **Todo en AWS**: En caso de que el fichero 'aws_credentials' no esté presente en el contenedor o en la aplicación, el programa asume que se encuentra desplegado en un entorno de Cloud (AWS). En esta situación, intenta acceder al Bucket de S3 sin necesidad de credenciales adicionales.

### 3.3. Ejecución de la Aplicación

La aplicación se ejecuta en modo local mediante el comando de Streamlit "Streamlit run app.py".

ℹ️ Hay que tener en cuenta que esta Aplicación sirve en el puerto 5007, si se desea utilizar otro puerto se deberá cambiar el código y los ficheros correspondientes. ℹ️

### 3.4. Construir una imagen de Docker

### 3.4.1 Construir una imagen de Docker en modo local
Para construir una imagen de Docker en modo local ejecutar el comando: `docker build -t traffic-accidents-app-local .`

### 3.4.2 Publicar la imagen y ejecutarla en AWS mediante ECR
Instrucciones para subir la imagen a un repositorio remoto en ECR (AWS):

- `aws configure` (Configura aws_access_key_id y aws_secret_access_key)

- `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com`

- `docker build --platform linux/amd64 -t <your-app-name>.`
    
- `docker tag <your-app-name>:latest <account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:<tag>`

- `docker push <account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:<tag>`

[Para más información, consulta esta guía](https://docs.aws.amazon.com/ecr/)

### 3.5. Archivos y Carpetas en `streamlit`

- **requirements.txt**: Lista de dependencias de Python para la aplicación.
- **Dockerfile**: Instrucciones de construcción de imagen Docker.
- **docker-compose.yml**: Definición de contenedores Docker.
- **.dockerignore**: Exclusión de archivos en imágenes Docker.
- **source**: Carpeta con el Código fuente de la aplicación.
- **Notebooks**: Carpeta que contiene libretas para crear las Listas de Valores de la App y subirlas a un Bucket en S3.

### 3.5.1. Carpeta `source`

La carpeta `source` contiene el código fuente de la aplicación Streamlit, incluyendo scripts de Python y archivos relacionados.

- **app.py**: Archivo principal de la aplicación.
- **maps.py**: módulo para la generación de mapas.
- **ml.py**: módulo relacionado con las visualización predictiva de lesividad.
- **eda.py**: Script para el análisis gráfico de los datos.
- **file_aux.py**: Script auxiliar para el tratamiento de ficheros en local y en AWS.
- **aws_credentials**: Archivo de credenciales para AWS.

##### 3.5.1.1. Subcarpeta `img`

La subcarpeta `img` almacena imágenes utilizadas en la aplicación.

- **TrafficBW.jpeg**: Imagen relacionada con el tráfico en blanco y negro.
- **accidente_portada.jpg**: Imagen de portada relacionada con accidentes.

##### 3.5.1.2. Subcarpeta `data`

La subcarpeta `data` contiene archivos de datos utilizados por la aplicación.

- **2023_Accidentalidad_predicciones.csv**: Conjunto de datos utilizado para las predicciones.
- **Distritos_de_Madrid.geojson**: Datos geoespaciales de los distritos de Madrid.
- **LOV.json**: Listas de Valores para la aplicación.
- **2023_Accidentalidad_c_g_s_d_clean.csv**: Conjunto de datos limpiado y enriquecido.


## 4. Configuración y Ejecución

Para configurar y ejecutar estos proyectos, sigue las instrucciones proporcionadas en cada sección correspondiente. Asegúrate de que las dependencias especificadas en los archivos `requirements.txt` estén instaladas antes de ejecutar los proyectos.

## 5. Contribuciones

Si deseas contribuir a estos proyectos, te animamos a hacerlo. Puedes colaborar de varias maneras, como reportando problemas, enviando solicitudes de extracción o mejorando la documentación. Si decides contribuir, asegúrate de seguir las pautas de contribución del proyecto.

