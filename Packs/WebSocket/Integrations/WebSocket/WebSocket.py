from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
from CommonServerUserPython import *  # noqa
''' IMPORTS '''
import asyncio
import websockets

''' Classes '''

INTEGRATION_NAME = 'WebSocket App'


''' HELPER FUNCTIONS '''


def try_parse_integer(int_to_parse, err_msg):
    try:
        res = int(int_to_parse)
    except (TypeError, ValueError):
        raise DemistoException(err_msg)
    return res


def get_params_port(params):
    port_mapping: str = params.get('longRunningPort', '')
    err_msg: str
    port: int
    if port_mapping:
        err_msg = f'Listen Port must be an integer. {port_mapping} is not valid.'
        if ':' in port_mapping:
            port = try_parse_integer(port_mapping.split(':')[1], err_msg)
        else:
            port = try_parse_integer(port_mapping, err_msg)
    else:
        raise ValueError('Please provide a Listen Port.')
    return port


''' Routes '''


async def echo(websocket, path):
    message = await websocket.recv()
    return_outputs(f"Received message: {message} on path {path}")

    message_echo = f"Echo: {message}!"

    await websocket.send(message_echo)
    return_outputs(f"> {message_echo}")


'''' Commands '''


def test_module(_, params):
    return "ok"


def run_long_running(params):

    port = get_params_port(params)

    start_server = websockets.serve(echo, "0.0.0.0", port)
    return_outputs('WebSocket Server Started!')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def main():

    params = demisto.params()

    demisto.debug(f'Command being called is {demisto.command()}')

    try:
        if demisto.command() == 'long-running-execution':
            run_long_running(params)
        elif demisto.command() == 'test-module':
            result = test_module(demisto.args(), params)
            return_results(result)

    except Exception as e:
        return_error(str(f'Failed to execute {demisto.command()} command. Error: {str(e)}'))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()