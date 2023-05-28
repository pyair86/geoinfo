#geoinfo

##Goal
Get points from an indexed PostGIS table, present them on a map, open a popup with attributes
when clicking on a point, post new points to the db with some validations in local srid.

Chosen validations are range of coordinates, numeric values only for coordinates fields,
length of fields in the form, number of dimensions of points in the db.

##How to run
1. clone https://github.com/pyair86/geoinfo
2. docker-compose build
3. docker-compose up -d
4. docker-compose exec web bash -c "python setup_db.py"
5. http://127.0.0.1:3000/

For running tests:
docker-compose exec web bash -c "pytest"


##Improvements
1. CI-CD and Linters.
2. Tests - more code coverage.  
3. Error handling.
4. More validations.
5. Spatial and normal constraints - e.g. don't insert a new point if 5 meters within another point.
6. Cache - finding a suitable cache strategy.
7. React/Vue/Angular - for a stateful and more organized frontend.
8. Big data strategy - how to store and present many points.




