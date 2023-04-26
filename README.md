# TELEGET
- Get elevation from single/batch lat/long in Vietnam.
- Get realtime AQI data for single/batch lat/long in Ho Chi Minh city.
- Get historical AQI data for single lat/long in Ho Chi Minh city.
- Crawl `iqair` periodically at every 1 hour to fetch the latest AQI data.

## How to install this application
1. Install docker and docker-compose.
2. Add raster file of Vietnam into ./data/
```
cd teleget
mkdir data
wget https://data.opendevelopmentmekong.net/dataset/b3e1e48c-95bb-450d-abfa-5bf725edcb10/resource/2b7edeed-2d46-4a38-8f40-08d3b7e486bd/download/dem.zip
unzip dem.zip
```
3. Run `docker-compose up`.
4. Checkout `http://localhost:8000/api/docs/` to get the API documentation.


## How to deploy this application AWS EC2 machine.
- Follow this doc to encrypt HTTP requests with Let's encrypt on EC2 machine.
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04
Should encrypt with Let's encrypt because this site is popular and accepted by all of browsers.

- EC2 machine need to be configured with allowing access via HTTPS 443.

## Reference:
- https://github.com/ajnisbet/opentopodata
