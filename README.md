# RIDER-USER APIS ![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

### _Tech stack used_
```
- python/django/django-restframework
- SQlite 3
```

#### Installation

##### clone or download and extract the project directory 

### check for the python version,should be version 3+

1. Create a virtualenv (better to work in virtualenv)  
```
a. virtualenv env
b. cd env
```
2. Place the downloaded project inside env
```
a. cd Cab-Booking-System
b. pip install requirements.txt
```
3. Initialization of Project
```
a. python manage.py makemigrations
b. python manage.py migrate
c. python manage.py migrate --run-syncdb
d. python manage.py createsuperuser (provide username,email,password)
e. python manage.py runserver
```
### Running the APIs. There are two apps in this project (driverAPI, passengerAPI)

Base URL :  (http://127.0.0.1:8000/api/v1/)

#### admin(http://127.0.0.1:8000/admin/)
```
a. Login using the details of the superuser created
b. create one or more passenger and driver objects in the driverAPI and passenger API ,clicking on the +Add green link.
``` 

#### passengerEndpoints(http://127.0.0.1:8000/api/v1/passenger)

a. Setting the location by entering the latitude and the longitude : <http://127.0.0.1:8000/api/v1/passenger/RequestRide/>
b. Requesting a cab by proving latitude and longitude of the destination, set booking_id = 0, use passenger-id and driver_id created previously - <http://127.0.0.1:8000/api/v1/passenger/setLocation/>
c.  Check for the ride acceptance by proving the passenger_id and checking the booking_status- <http://127.0.0.1:8000/api/v1/passenger/isRideAccepted/>


#### driverEndpoints(http://127.0.0.1:8000/api/v1/driver/)

a. See all available rides by entering source and destination address - <http://127.0.0.1:8000/api/v1/driver/available_passengers/>
b. Accepting the cab and changing the booking_status = 1 and deleting the availaible rides from the list of available rides.
- <http://127.0.0.1:8000/api/v1/driver/accept_cab>

Can Use latitude and longitude from - (<https://www.latlong.net/>) 

RANGE:[-90,90]

```
a.Simple logging is used-logger.info(),logger.warnings(),logger.error() are used.
```



