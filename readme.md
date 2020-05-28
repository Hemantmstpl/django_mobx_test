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

### API created at backend
**1. API to getting access token**
    URL : `/api/token/`
  Method : POST
  Returns the JWT token and refresh token, to be used for 
  authentication.

**2. API to refresh the token:**
   URL : `/api/token/refresh/`
   Method : POST

**3. API to get list of all restaurants**
   URL : `/api/restaurants/choices/`
   Method: GET
    Authorization headers required
   Response: 
       

    [       
     {
      "id": 1,
        "name": "Test Contract Template"      
     } 
    ...
    ]

**4.  API to get list of all tickets of restaurants**
   URL : `/api/restaurants/<restaurants_id>/tickets/`
   Method: GET
   Authorization headers required
   Response:
      

  [
    { 
      "id": 1,
      "name": "Test Tickets",
      "available_quantity": 10,
    "code" : <uuid>       
    }
     ...
  ]

**5. API to create a ticket for restaurants**
   URL : `/api/restaurants/<restaurants_id>/tickets/`
   Method: POST
   Authorization headers required
   Request data:
   

  {
   "name" : <ticket_name>,
   "max_purchase_count": count 
  }
  
**6. API to retrieve a ticket of a restaurant**
   URL : `/api/restaurants/<restaurantss_id>/tickets/<ticket_id>`
   Method : GET
   Authorization headers required
   Respone:
  

  {
   "id": 1,
   "name": "Test Tickets",
   "available_quantity": 10,
   "code" :"a1349bdf-0422-4c7f-8775-6e7c0447139c"
  }

**7. API to update a ticket information of a restaurant**
   URL : `/api/restaurants/<restaurantss_id>/tickets/<ticket_id>`
   Method : PUT
   Authorization headers required
   Request data:
  

  {
    "name": "Test Tickets",
    "max_purchase_count":10
  }
  
**8.API to delete a ticket information of a restaurant**
    URL : `/api/restaurants/<restaurantss_id>/tickets/<ticket_id>`
   Method : DELETE
   
**9. API to get all tickets for users to purchase** 
     URL : `/api/tickets/`  
     Method : GET
    Authentication not required    

**10. API to retrieve ticket for users to purchase**
   URL : `/api/tickets/<ticket_code>/`  
     Method : GET
    Authentication not required  
    
**11. API to purchase a ticket**
    URL : `/api/tickets/<ticket_code>/purchase/`
    Method : POST
    Authentication not required
    Request data :


>  { 
>     "email":"test4@yopmail.com", 
>   "count":3
>      }

Response:
  

> {   
> "id": 10,
>   "ticket": "coupon3",
>     "created_at": "2020-05-27T14:21:48.680160Z", 
>     "last_update":"2020-05-27T14:21:48.680182Z", 
>     "email": "test4@yopmail.com",
>   "count": 3
>   }

Response in case of error:
a. If no ticket is available :

> { "detail": "No more tickets available" }

b. If avaialble ticket count is less than the requested purchase count

> { "detail": "Only {} ticket are available" }
