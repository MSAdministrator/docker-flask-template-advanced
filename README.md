# swimlane-app-form

This project aims to provide a dynamic webform generator for Swimlane applications so that users can submit requests directly to Swimlane based on one or more defined fields.

This project has the following features:

* Bootstrap 4 frontend
* Dynamically render fields from Swimlane applications based on the application acronym

> NOTE: This is docker-compose project with only one container

### Prerequisites

To use this project you must download Docker and docker-compose on your local system. You can find more information about how to do that [here](https://docs.docker.com/compose/install/).

### Installing

To get started you must first clone this repository and then make a copy of the `.env.example` file on your local system

```
git clone git@github.com:swimlane/dofeedback.git
cd dofeedback
cp .env.example .env
```

Once you have your repository and the `.env` file then you can run the following to rebuild and setup your containers:

```
docker-compose up --build --remove-orphans
```

## Running the tests

There are currently `NO TESTS` but we will need to create some overtime.

### Break down into end to end tests
N/A

### And coding style tests

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

Currently there is a production deployment docker-compose file [docker-compose.production.yml](docker-compose.production.yml) but there needs some work done to make it fully production ready.

## Built With

* [carcass](https://github.com/MSAdministrator/carcass) - Python packaging template

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* Josh Rickard - *Initial work* - [MSAdministrator](https://github.com/MSAdministrator)

See also the list of [contributors](https://github.com/MSAdministrator/attck_viz/contributors) who participated in this project.
