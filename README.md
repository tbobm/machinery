# machinery

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
    "name": "my-service-name",
    "address": "http://my-service:5000/",
    "spec": {
        "inputs": {
            "message": {
                "type": "string",
                "description": "The text to transform"
            }
        },
        "outputs": {
            "message": {
                "type": "string",
                "description": "The transformed text"
            }
        }
    }
}
```


input:
- `name`: The name of the Service
- `address`: The URL of the Service
- `spec`: The inputs/outputs of this Service
- `spec.inputs`: Each input with its type and description
- `spec.outputs`: Each output with its type and description

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
    "name": "my-workflow",
    "spec": {
        "services": ["service-1", "service-2"],
        "inputs": {
            "message": {
                "type": "string",
                "description": "The text to process"
            }
        },
        "outputs": {
            "message": {
                "type": "string",
                "description": "The processed text"
            }
        },
        "operations": { }
    }
}
```

input:
- `name`: The name of the Workflow
- `spec`: The spec of the Workflow
- `spec.services`: The Services to be called, in order
- `spec.inputs`: The inputs of this Workflow
- `spec.outputs`: The outputs of this workflow

output: TBD
(workflow-id, ack date)
