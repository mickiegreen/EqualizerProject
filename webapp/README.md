# reango
The Django + GraphQL Relay Modern backend.


## Features

* Relay Support
* User Registration/Sign up using JWT
* Heroku or Docker Deployment

## Quick start:
You will need python 3 and node installed.
You will also need to have a virtualenv activated before running npm install/yarn or the post install build step will fail as django needs to be available to dump the graphql_schema
```
source ~/.virtualenvs/reango/bin/activate
pip3 install -r ./deps/dev.txt
yarn
```

## Getting started
Define a django model, register the node and query with in the ./server/reango/schema.py

To work with the client side, add a route in the ./client/routes

Reusable components go in ./client/components, 
If you'd like you can split of django apps into there own folders in the 
./client/modules like the django apps concept

## Prod

See readme in `./lib/deployment`

### Front-End originally based on the awesome Relay Fullstack
https://github.com/lvarayut/relay-fullstack
