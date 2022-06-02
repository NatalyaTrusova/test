Service for creating DB about heroes from Harry Potter and working with it. 

There are next tables:
1) Heroes - table with name, birthday day, side and power for each hero;
2) Slogans - table with slogans of heroes. Сan contain only slogans of heroes that are in the 'Heroes' table.
3) Stories - table with stories of heroes. Сan contain only stories of heroes that are in the 'Heroes' table.
4) Warfares - table with warfares of heroes. There is ids of two heroes from different side, their slogans and winner.

There is also view "statistics_for_db" containing statistics about the database.

Setting up a DEV environment:
 DOCKER:
 docker-compose up --build
 
 PYTHON:
 In app's CLI:
	# for db initialization
	python main.py
	# to add a new hero
	python queries_for_db.py add_new_hero "Harry Potter" "1980-07-31" "Phoenix Order" 100
 
 POSTGRES:
 In app's CLI:
	psql --user=postgres --dbname=harrypotterDEV
	SELECT * FROM heroes;
 

Setting up a PROD environment:
 DOCKER:
 docker-compose -f docker-compose.prod.yml up -d --build 
 
 PYTHON:
 In app's CLI:
	python queries_for_db.py add_new_slogan 1 "I'm Harry Potter"
 
 POSTGRES:
 In app's CLI: 
	psql --user=postgres --dbname=harrypotterPROD	
	# already has some data in db from .sql file
	SELECT * FROM heroes;

Logging:
There are different loggers with different handlers. 
For inserting there is INFO logger and it's file. For deleting there is WARNING handler for previous logger and it's own file.
For integrity constraints error there is ERROR logger, which prints warning into command line.

For problems with authentication (when connecting to the database during the formation of the engine) there is CRITICAL logger 
which sends messages in telegram. Although, there is more simple way to test it: def function_for_admin_only from queries_for_db.
For example, user can write in python app's CLI:
	python queries_for_db.py function_for_admin_only "admin" "qwerty"
it would just print "Hello, admin!"
But if user would write:
	python queries_for_db.py function_for_admin_only "not_admin" "qwerty"
a warning message would be sent into telegram chat named 'DB_logs' (https://t.me/db_logs)