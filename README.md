## How to run services:

- Download this repository
- Go to the root directory
- Run docker-compose `docker-compose up --scale sensor_app=8`

That would run 11 containers: 9 - sensors, 1 - controller, 1 - manipulator, 1 - web interface, 1 - nginx

Applications logs could be found in the corresponding folders. Logs destination directory can be changed in the 
docker-compose.yml file

After the application start, you can go to the http://localhost:5000/ and see the controller status 
pressing refresh button. Ajax request from the page goes to the controller application over HTTPS protocol.

Just because there is self-signed ssl certificate is in use - you have to add it as an exception in you browser.