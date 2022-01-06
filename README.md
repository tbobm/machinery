# machinery

[![CI](https://github.com/tbobm/machinery/actions/workflows/ci.yml/badge.svg)](https://github.com/tbobm/machinery/actions/workflows/ci.yml)

State-aware workflow orchestrator.

This project aims to bring stateful workflows, by defining a list of actions
representing multiple microservices.

Define a suite of actions to process events, abstract intelligence for your microservices.

Once defined, use your workflows to process your Events.

## Example

We have 3 microservices:
- The `upper` microservice that transforms texts into uppercase
- The `reverse` microservice that reverses a text
- The `space-counter` microservice that returns the number of space in a string

Suppose we want to process some text by making it uppercase and reversing it.

We will define the following definitions:
- [`examples/definitions/service-upper.json`](./examples/definitions/service-upper.json)
- [`examples/definitions/service-reverse.json`](./examples/definitions/service-reverse.json)
- [`examples/definitions/service-space-counter.json`](./examples/definitions/service-space-counter.json)

Then, we can define a Workflow in [`examples/definitions/workflow-process-text.json`](./examples/definitions/workflow-process-text.json).

After having created our Workflow, we can send our first Event !

We will send the content of [`examples/definitions/event-text.json`](./examples/definitions/event-text.json)

## Goals

- Register services (ex: a new API)
- Define a simple Workflow (subsequent calls to different services)
- Allow async (expose endpoint for webhook?)
- Visualisation

## Development

The recommended approach is to use `virtualenv` to install the API's dependencies.

```console
$ pip install virtualenv
$ python -m virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements_dev.txt
$ pip install -e .
```

In order to ease iterations, some helpers scripts are available.

**start the database**

Starts a background MongoDB container in host networking mode.

```console
$ ./run-background-service.sh
```

**run the api in development mode**

Start the Flask Application in development + debug mode.

```console
$ ./run_app 
 * Serving Flask app 'machinery.api:create_app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
```

## Testing

Every testing-related dependency is listed in the `requirements_dev.txt` file.

```console
$ pip install -r requirements_dev.txt
```

### Unit tests

This project implements unittests using `pytest`.

In a configured environment, run the following command:
```console
$ pytest
```

### Linting

This project is linted using `pylint`

In a configured environment, run the following command:
```console
$ pylint machinery
```

### Functional tests

This API is tested using Postman/Newman. ([newman: Getting Started][newman])

Assets are available in the `./postman` directory and expect the API to be accessible at `http://localhost:5000`.
This can be achieved using the `./run_app` script.

**Example:**
```console
$ npm install newman
$ ./node_modules/newman/bin/newman.js run ./postman/Machinery.postman_collection.json -e postman/Machinery\ -\ Local.postman_env.json 
newman

Machinery

→ Create a Service
  POST http://localhost:5000/s [201 CREATED, 197B, 38ms]
  ✓  Status code is 201
  ✓  Response contains a service_id

┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│            test-scripts │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│      prerequest-scripts │                0 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │                2 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 70ms                                      │
├───────────────────────────────────────────────────────────────┤
│ total data received: 47B (approx)                             │
├───────────────────────────────────────────────────────────────┤
│ average response time: 38ms [min: 38ms, max: 38ms, s.d.: 0µs] │
└───────────────────────────────────────────────────────────────┘
```

[newman]: https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/

#### A Note on functional tests

As this Python project is to be considered to be a POC to define the required
feature set for the "production-grade" version of Machinery, this testing part
is the most important than any other tests.

The next version _probably_ will not be written in Python and this contract
will allow to quickly develop a stable version.

Being able to define a usable API is the current goal for Machinery.

## Components

### API (WIP)

_Could be divided into Consumer API and Management API._

- Register services
- Define Workflows (json with arbitrary service definition)
- Treat Event

## Data structures

### Service

```json
{
    "name": "upper",
    "address": "http://upper.local:5000/",
    "inputs": [
         {
            "name": "message",
            "type": "string",
            "description": "The text to transform"
        }
    ],
    "outputs": [
         {
            "name": "message",
            "type": "string",
            "description": "The transformed text, in uppercase"
        }
    ]
}
```


input:
- `name`: The name of the Service
- `address`: The URL of the Service
- `inputs`: Each input with its type and description
- `outputs`: Each output with its type and description

output: TBD
(service-id, ack date)

### Event

POST `/e/<workflow-id>`

```json
{
    "data": {
        "message": "The Sun will rise in the morning !"
    }
}
```

POSTing an Event will return an `event-id`, an ack date and a status.
input:
- `data`: The Event's data that **must** match the Workflow's inputs.

### Workflow

```json
{
    "name": "process-text",
    "services": ["upper", "reverse", "space-counter"],
    "inputs": [
         {
            "name": "message",
            "type": "string",
            "description": "The text to process"
        }
    ],
    "outputs": [
         {
            "name": "message",
            "type": "string",
            "description": "The processed text"
        },
         {
            "name": "space_count",
            "type": "int",
            "description": "The number of spaces"
        }
    ],
    "operations": [
        {
            "type": "copy",
            "source": "message",
            "dest": "original",
            "apply": "before",
            "service": "0"
        }
    ]
}
```

input:
- `name`: The name of the Workflow
- `services`: The Services to be called, in order
- `inputs`: The inputs of this Workflow
- `outputs`: The outputs of this workflow
- `operations`: A list of operations that modifies the event data between service calls

output: TBD
(workflow-id, ack date)
