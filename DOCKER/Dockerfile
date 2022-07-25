#Download Python from DockerHub and use it
FROM python:3.9.12

#Set the working directory in the Docker container
WORKDIR /code

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install the dependencies

# Poppler from build
#RUN apt-get update && apt-get install wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev -y
#RUN wget https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz \
#    && tar -xf poppler-data-0.4.9.tar.gz \
#    && cd poppler-data-0.4.9 \
#    && make install \
#    && cd .. \
#    && wget https://poppler.freedesktop.org/poppler-20.08.0.tar.xz \
#    && tar -xf poppler-20.08.0.tar.xz \
#    && cd poppler-20.08.0 \
#    && mkdir build \
#    && cd build \
#    && cmake .. \
#    && make \
#    && make install \
#    && ldconfig
#CMD tail -f /dev/null

# Poppler from build
# https://stackoverflow.com/questions/61272431/installing-poppler-utils-of-version-0-82-in-docker/63265495#63265495
RUN apt-get update && apt-get install apt-utils wget build-essential cmake libfreetype6-dev pkg-config libfontconfig-dev libjpeg-dev libopenjp2-7-dev libcairo2-dev libtiff5-dev -y
RUN wget https://poppler.freedesktop.org/poppler-data-0.4.10.tar.gz \
    && tar -xf poppler-data-0.4.10.tar.gz \
    && cd poppler-data-0.4.10 \
    && make install \
    && cd .. \
    && wget https://poppler.freedesktop.org/poppler-21.03.0.tar.xz \
    && tar -xf poppler-21.03.0.tar.xz \
    && cd poppler-21.03.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && cd ../.. \
    && ldconfig \
    && rm poppler-data-0.4.10.tar.gz \
    && rm -rf poppler-data-0.4.10 \
    && rm poppler-21.03.0.tar.xz \
    && rm -rf poppler-21.03.0

# Nano
RUN apt-get update && \
    apt-get install -y nano && \
    rm -fr /var/lib/apt/lists/*


# Any other dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
COPY src/ .

#Run the container
CMD [ "python", "./app.py" ]

# Run on port 80
EXPOSE 80
