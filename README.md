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
    "operations": [ ]
}
```

input:
- `name`: The name of the Workflow
- `services`: The Services to be called, in order
- `inputs`: The inputs of this Workflow
- `outputs`: The outputs of this workflow

output: TBD
(workflow-id, ack date)
