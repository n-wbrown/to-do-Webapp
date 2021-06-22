# To-Do 

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
### Running the CLI

The CLI tool can be run using the following syntax. The `create`, `read`,
`update`, and `delete` subcommands each have their own arguments that can be
read using the `--help` command following the respective subcommand.

```bash
usage: todo [-h] --db DB {create,read,update,delete} ...

optional arguments:
  -h, --help            show this help message and exit
  --db DB               select your database

Subcommands:

  {create,read,update,delete}
    create              Create a new to-do item
    read                Read the data of an existing to-do item
    update              Update an existing to-do item
    delete              Delete a to-do item
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
