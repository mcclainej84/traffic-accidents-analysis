FROM python:3.10

EXPOSE 5007

WORKDIR /streamlit-app
COPY ./source/ .
COPY requirements.txt .

# Install GDAL and geospatial libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev

# Set GDAL environment variables
ENV GDAL_VERSION 3.3.2
ENV GDAL_CONFIG /usr/bin/gdal-config

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=5007", "--server.address=0.0.0.0"]