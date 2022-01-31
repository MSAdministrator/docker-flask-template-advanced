# Advanced Docker Flask Template

This project is a basic `Docker` (and `docker-compose`) Flask project that can be used as a base template.

This project contains the following containers/services:

* flask - This is the Flask web application service
* worker - This is a single celery worker
* monitor - This is a Flower container which can be used to monitor Redis Queues
* redis - This is our Queue system which our Flask app will send data to and our worker will pick items off of the queue to be worked.
* mongo - This is our database which stores User information as well as saves searches (as an example only).

This project has the following features:

* User Account features
    * Registration
    * Password Reset
    * Change Email
    * Login 
    * Email Templates
    * Plus many commmon user attributes
* Celery Features
    * A template layout support celery workers using Redis
    * Hook worker requests for logging or troubleshooting
    * Example of `Chaining` celery tasks
* MongoDB Connection
    * Database Session management best practices
* Bootstrap 4 frontend
* Utilizes best practices including:
    * Flask application context
    * Flask logging and error handling
    * Flask Blueprints
    * Utilizes a base template inherited within all blueprints
    * Plus more!

> A simpler template can be found [here](https://github.com/MSAdministrator/docker-flask-template)

### Prerequisites

To use this project you must download Docker and docker-compose on your local system. You can find more information about how to do that [here](https://docs.docker.com/compose/install/).

### Installing

To get started you must first clone this repository and then make a copy of the `.env.example` file on your local system

```
git clone https://github.com/MSAdministrator/docker-flask-template-advanced.git
cd docker-flask-template-advanced
cp .env.example .env
```

Once you have your repository and the `.env` file then you can run the following to rebuild and setup your containers:

```
docker-compose up --build --remove-orphans
```

### Structure

All sections of the website should be segmented into blueprints. Each `blueprint` should have the following structure:

```
📦user
 ┣ 📂templates
 ┃ ┗ 📂user
 ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┣ 📜members.html
 ┃ ┃ ┣ 📜register.html
 ┃ ┃ ┗ 📜reset_password.html
 ┣ 📜__init__.py
 ┣ 📜forms.py
 ┣ 📜models.py
 ┗ 📜views.py
```

Not all modules (single .py files) may be needed. For example not every blueprint will have a `forms.py` or a `models.py` but each blueprint should have a `__init__.py`, a `views.py`, and a `template/{blueprint_name}` folder structure.

## Deployment

Currently there is `NO` production deployment docker-compose file.

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/attck_viz/contributors) who participated in this project.
