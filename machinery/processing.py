"""Event processing functions."""
import requests


def process_event(payload, workflow, service_definitions: dict):
    """Call each service for the Event.

    .. highlight:: python
    .. code-block:: python

        event = {
            "inputs": {
                "message": "sample test"
            },
            "outputs": {
                "message": "SAMPLE TEST"
            }
        }

    Return only the value of the `.outputs` key of the event.
    """
    services = workflow.get('services')
    event = {
        'inputs': payload,
        'outputs': {},
    }
    for service in services:
        result = requests.post(service_definitions[service]['address'], json=event['inputs'])
        event = transform_data(event, result.json())
    return event['outputs']


def transform_data(event: dict, result: dict) -> dict:
    """Integrate the result in the event.

    result outputs become merged with event outputs
    event outputs become payload inputs
    """
    event['outputs'] = _basic_override(event['outputs'], result)
    event['inputs'] = event['outputs']
    return event


# TODO: abstract processing patterns in a class / interface ?
def _basic_override(outputs: dict, to_merge: dict) -> dict:
    """Simply merge the new values into the old values."""
    return {**outputs, **to_merge}
