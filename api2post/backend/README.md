docker build -t api2post .
docker run -e TEST_POSTGRES_PASSWORD=XXX -p 80:80 api2post


docker tag api2post us-central1-docker.pkg.dev/playground-geo/autio-transcription-services/api2post
docker push us-central1-docker.pkg.dev/playground-geo/autio-transcription-services/api2post