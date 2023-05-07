docker build -t api2post .
docker run -e TEST_POSTGRES_PASSWORD=XXX api2post