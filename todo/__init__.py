import os
from flask import Flask, request, abort, jsonify
from flask_restx import Resource, Api, fields
from . import datastore


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if os.environ.get("FLASK_DATABASE", None) is None:
        db = os.path.join(app.instance_path, 'todo.sqlite'),
    else: 
        db = os.environ.get("FLASK_DATABASE")

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=db 
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_first_request
    def initial_db_setup():
        datastore.init_db()

    # Router
    router(app)

    # Documentation
    docs(app)

    return app


def router(app):
    """ Create routes """
    # CREATE 
    @app.route('/todo/create', methods=["POST"])
    def create():
        if request.method == "POST":
            data = request.get_json()
            if data is None: 
                abort(400, description="No arguments given")
            item = data.pop("item", None)
            status = data.pop("status", None)
            try:
                id = datastore.create(item, status)
            except AssertionError:
                abort(400, description="Bad arguments given")
            return jsonify(
                id=id,
                item=item,
                status=status
            ), 201

    # READ
    @app.route('/todo/read/<int:item_id>', methods=["GET"])
    def read(item_id):
        if request.method == "GET":
            try:
                result = datastore.read(item_id)
            except AssertionError:
                abort(500)

            if result is not None:
                return jsonify(
                    datastore.row_to_dict(result)
                )
            else:
                abort(410, description="ID does not exist")

    # READ ALL
    @app.route('/todo/read', methods=["GET"])
    def read_all():
        result = datastore.read_all()
        response = []
        for row in result:
            response.append(datastore.row_to_dict(row))
        return jsonify(response)

    # UPDATE
    @app.route('/todo/update/<int:id>', methods=["POST"])
    def update(id):
        if request.method == "POST":
            data = request.get_json()
            item = data.pop("item", None)
            status = data.pop("status", None)
            # Check to see if the entry exists
            try:
                result = datastore.read(id)
            except AssertionError:
                abort(500)
            if result is None:
                abort(410, description="ID does not exist")
            # Then delete it if it exists 
            try:
                datastore.update(id, item, status)
            except AssertionError:
                abort(400, description="Bad arguments given")

            return jsonify(
                id=id,
                item=item,
                status=status
            ), 201

    # DELETE
    @app.route('/todo/delete/<int:id>', methods=["POST"])
    def delete(id):
        if request.method == "POST":
            # Check to see if the entry exists
            try:
                result = datastore.read(id)
            except AssertionError:
                abort(500)
            if result is None:
                abort(410, description="ID does not exist")
            try:
                datastore.delete(id)
            except AssertionError:
                abort(400, description="Bad arguments given")
            return jsonify(
                id=id,
            ), 201


def docs(app):
    """Build swagger documentation"""

    # Initial config
    api = Api(
        app,
        title="To-do",
        description='to-do list application for Picarro'
    )
    ns = api.namespace('todo', description='Operate on to-do list')

    # Create model
    todo_model = ns.model('To-do Model', {
        'id': fields.Integer,
        'item': fields.String,
        'status': fields.String,
    })

    # CREATE
    create_parser = ns.parser()
    create_parser.add_argument(
        'item',
        type=str,
        help='To-do task list item',
        location='json',
    )
    create_parser.add_argument(
        'status',
        type=str,
        help='Status of to-do item',
        location='json',
    )

    @ns.route('/create', doc={
        "description": "Create a new to-do entry."
    })
    @ns.doc()
    class CreateDoc(Resource):
        @ns.doc(responses={
            201: 'Success',
            400: 'Bad arguments given',
        })
        @ns.expect(create_parser)
        @ns.marshal_with(todo_model, code=201)
        def post(self):
            pass

    # READ ALL
    @ns.route('/read', doc={
        "description": "List all to-do entries."
    })
    @ns.doc()
    class ReadAllDoc(Resource):
        @ns.doc(responses={
            200: "Success",
        })
        @ns.marshal_with(todo_model, code=200, as_list=True)
        def get(self, id):
            pass

    # READ
    @ns.route('/read/<int:id>', doc={
        "description": "Read a single to-do entry identified by id.",
    })
    @ns.doc()
    @ns.param('id', 'to-do item id')
    class ReadDoc(Resource):
        @ns.doc(responses={
            200: "Success",
            500: "Internal Error",
            410: "ID does not exist",
        })
        @ns.marshal_with(todo_model, code=200)
        def get(self, id):
            pass

    # UPDATE
    update_parser = ns.parser()
    update_parser.add_argument(
        'item',
        type=str,
        help='To-do task list item',
        location='json',
    )
    update_parser.add_argument(
        'status',
        type=str,
        help='Status of to-do item',
        location='json',
    )

    @ns.route('/update/<int:id>', doc={
        "description": "Update a single to-do entry identified by id.",
    })
    @ns.doc()
    @ns.param('id', 'to-do item id')
    class UpdateDoc(Resource):
        @ns.doc(responses={
            201: "Success",
            400: "Bad arguments given",
            410: "ID does not exist",
            500: "Internal Error",
        })
        @ns.expect(update_parser)
        @ns.marshal_with(todo_model, code=201)
        def post(self, id):
            pass

    # DELETE
    @ns.route('/delete/<int:id>', doc={
        "description": "Delete a single to-do entry identified by id.",
    })
    @ns.doc()
    @ns.param('id', 'to-do item id')
    class DeleteDoc(Resource):
        @ns.doc(responses={
            200: "Success",
            400: "Bad arguments given",
            410: "ID does not exist",
            500: "Internal Error",
        })
        @ns.marshal_with(todo_model, code=201)
        def post(self, id):
            pass


def run_debug(db_path=None):
    app = create_app(db_path=db_path)
    app.run(debug=True)


deploy_app = create_app()
