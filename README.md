# To-Do Webapp

## Operation of the To-Do app

### Building the environment

Install conda on your system and run the following command to build the
development environment. All following steps should be run from with the newly
created environment.

```bash
$ make develop
```

### Running tests

Run the following command to run the tests.

```bash
$ make test
```

### Running a development server

Run the following command to start development server in debugging mode.


```bash
$ make dev
```

### Running the deployment server

Run the following commands to start a deployment server.

Begin by running the following command if you wish to select your own database.
If this environment variable is not set, the default database will be used.
Substitute `[DB_NAME]` with the name of your sqlite database.

```bash
$ export FLASK_DATABASE=[DB_NAME]
```

The following command starts the server. Substitute `[ADDRESS]` and `[PORT]`
respectively with the IP address and port you wish to bind your server to.

```bash
$ gunicorn -w 1 --bind [ADDR]:[PORT] todo:deploy_app
```
