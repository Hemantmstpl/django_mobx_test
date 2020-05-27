# Mobx Test
Following are the steps to be taken to setup the django project.

### Creating Virtual environment:

**Linux**
Ubuntu

    virtualenv -p python3 env
    source env/bin/activate

### Install Requirements:

    pip install -r requirements.txt

### 
**Creating .env file**


    export DB_NAME=db_name
    export DB_USER=postgres
    export DB_PASSWORD=postgres
    export DB_HOST=localhost
    export DJANGO_SETTINGS_MODULE=backend.settings.local
Here the DJANGO_SETTINGS_MODULE refers to the settings to be used.
Export env using command:
`source .env`

### Run Migrate:
    python manage.py migrate
    
### Load the initial data using
     python manage.py create_restaurants
     
### Start the server
    python manage.py runserver
    
### Run the test case using:

    python manage.py test

## Data loaded in database
Using the managment command we create :
1. Owner with:
  email = owner1@gmail.com 
  password "test" 
  username "owner1"
  Restaurants for this owner with name- "Restaurant1", "Restaurant2" and 
  "Restaurant3"
3. Owner with:
  email = owner2@gmail.com 
  password "test" 
  username "owner2"
  Restaurants for this owner with name- "Restaurant1", "Restaurant2" and 
  "Restaurant3"
