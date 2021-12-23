#!/bin/sh
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=app:create_app

flask run --host=0.0.0.0
