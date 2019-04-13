## How to run services:

- Download this repository
- Go to the root directory
- Run docker-compose `docker-compose up --scale sensor_app=8`

That would run 11 containers: 8 - sensors, 1 - controller, 1 - manipulator, 1 - web interface

Applications logs could be found in the corresponding folders. Logs destination directory can be changed in the 
docker-compose.yml file