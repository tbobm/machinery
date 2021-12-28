#!/bin/sh

set -xe

export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=machinery.api:create_app

# may be improved to check if the db has already been init.
machinery-cli
flask run --host=0.0.0.0
