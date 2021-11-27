#!/usr/bin/env sh

docker run --rm -d -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=user \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    -e MONGO_INITDB_DATABASE=machinery \
    --network host \
    --name machinery_db \
    mongo:4.4
