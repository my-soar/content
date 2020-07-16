from CommonServerPython import *

''' IMPORTS '''

from tempfile import NamedTemporaryFile
from ssl import SSLContext, SSLError, PROTOCOL_TLSv1_2
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request
from multiprocessing import Process
from typing import Any, Dict, cast


''' Classes '''


class Handler:
    @staticmethod
    def write(msg):
        demisto.info(msg)


''' CONSTANTS '''


INTEGRATION_NAME = 'Gravity LongRunning Integration'
APP: Flask = Flask('Github-LRI')
XSOAR_LOGGER: Handler = Handler()


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


def validate_authentication(headers, app_secret, app_id=None):
    request_app_id = headers.get('X-App-ID', '')
    request_app_secret = headers.get('X-App-Secret', '')

    if not request_app_secret:
        return False
    elif app_id is None and app_secret not in request_app_secret:
        return False
    elif app_secret in request_app_secret and app_id in request_app_id:
        return True
    return False


''' ROUTE FUNCTIONS '''


@APP.route('/', methods=['GET'])
def void():
    params = demisto.params()

    app_id = params.get('app_id')
    app_secret = params.get('app_secret')

    if app_secret:
        headers = cast(Dict[Any, Any], request.headers)
        if not validate_authentication(headers, app_secret=app_secret, app_id=app_id):
            err_msg = 'Authentication failed. Make sure you are using the right credentials.'
            demisto.error(err_msg)
            return Response(err_msg, status=401)

    response = {
        "message": "Void has no Gravity, try to find a space object!"
    }
    return Response(json.dumps(response), status=200, mimetype='application/json')


@APP.route('/incidents', methods=['GET', 'POST'])
def route_incidents():
    params = demisto.params()

    app_id = params.get('app_id')
    app_secret = params.get('app_secret')

    if app_secret:
        headers = cast(Dict[Any, Any], request.headers)
        if not validate_authentication(headers, app_secret=app_secret, app_id=app_id):
            err_msg = 'Authentication failed. Make sure you are using the right credentials.'
            demisto.error(err_msg)
            return Response(err_msg, status=401)

    if request.method == "GET":
        response = {
            "message": "Incident Get!"
        }
    else:
        try:
            if request.json['name']:
                response = {
                    "message": create_incident()
                }
        except:
            response = {
                "message": "Invalid Incident Data, please review your incident fields"
            }
    return Response(json.dumps(response), status=200, mimetype='application/json')


def create_incident():
    incident = [{
        'name': "incident1022",
        "type": "Gravity",
        "customFields": {"field1": "value"}
    }]
    demisto.createIncidents(incident)

    return "Incident Created!"


@APP.route('/objects', methods=['GET'])
def route_black_hole():
    """
    Main handler for values saved in the integration context
    """
    params = demisto.params()

    app_id = params.get('app_id')
    app_secret = params.get('app_secret')

    if app_secret:
        headers = cast(Dict[Any, Any], request.headers)
        if not validate_authentication(headers, app_secret=app_secret, app_id=app_id):
            err_msg = 'Authentication failed. Make sure you are using the right credentials.'
            demisto.error(err_msg)
            return Response(err_msg, status=401)

    response = process_object_args(request.args, params)

    return Response(response, status=200, mimetype='application/json')


def process_object_args(request_args, params):
    res = {}

    """
    Processing a flask request arguments and generates a RequestArguments instance from it.
    Args:
        request_args: Flask request arguments
        params: Integration configuration parameters

    Returns:
        RequestArguments instance with processed arguments
    """
    name = request_args.get('name')
    object_type = request_args.get('type')
    app_id = params.get('app_id')

    if object_type == "black-hole":
        if name and "LB-1" in str(name):
            res['Object'] = "black-hole"
            res['Name'] = name
            res['Status'] = f"{object_type} Found"
            res['Distance'] = "7400 Light Years"
            res['Mass'] = "9.2 Solar Mass"
            res['Discovered'] = "Year 2019"
        elif name and "Cygnus X-3" in str(name):
            res['Object'] = "black-hole"
            res['Name'] = name
            res['Status'] = f"{object_type} Found"
            res['Distance'] = "11100 Light Years"
            res['Mass'] = "10.3 Solar Mass"
            res['Discovered'] = "Year 1967"
        else:
            res.clear()
            res['Object'] = "black-hole"
            res['Name'] = name
            res['Status'] = "BlackHole Not Found"
    else:
        res.clear()
        res['Object'] = object_type
        res['Name'] = name
        res['Status'] = f"{object_type} Not Found"

    if app_id:
        res['AppID'] = app_id

    return json.dumps(res)






'''' Commands '''


def test_module(_, params):
    get_params_port(params)
    run_long_running(params, is_test=True)
    return "ok"


def run_long_running(params, is_test=False):
    certificate: str = params.get('certificate', '')
    private_key: str = params.get('private_key', '')

    certificate_path = str()
    private_key_path = str()

    try:
        port = get_params_port(params)
        ssl_args = dict()

        if (certificate and not private_key) or (private_key and not certificate):
            raise DemistoException('If using HTTPS connection, both certificate and private key should be provided.')

        if certificate and private_key:
            certificate_file = NamedTemporaryFile(delete=False)
            certificate_path = certificate_file.name
            certificate_file.write(bytes(certificate, 'utf-8'))
            certificate_file.close()

            private_key_file = NamedTemporaryFile(delete=False)
            private_key_path = private_key_file.name
            private_key_file.write(bytes(private_key, 'utf-8'))
            private_key_file.close()

            context = SSLContext(PROTOCOL_TLSv1_2)
            context.load_cert_chain(certificate_path, private_key_path)
            ssl_args['ssl_context'] = context
            demisto.debug('Starting HTTPS Server')
        else:
            demisto.debug('Starting HTTP Server')

        server = WSGIServer(('0.0.0.0', port), APP, **ssl_args, log=XSOAR_LOGGER)
        if is_test:
            server_process = Process(target=server.serve_forever)
            server_process.start()
            time.sleep(5)
            server_process.terminate()
        else:
            server.serve_forever()
    except SSLError as e:
        ssl_err_message = f'Failed to validate certificate and/or private key: {str(e)}'
        demisto.error(ssl_err_message)
        raise ValueError(ssl_err_message)
    except Exception as e:
        demisto.error(f'An error occurred in long running loop: {str(e)}')
        raise ValueError(str(e))
    finally:
        if certificate_path:
            os.unlink(certificate_path)
        if private_key_path:
            os.unlink(private_key_path)


def gravity_update_cache():
    incident = [{
        'name': "incident1020",
        "type": "Phishing",
        "customFields": {"field1": "value"}
    }]
    demisto.createIncidents(incident)
    return "Incident Created"


def main():
    """
        PARSE AND VALIDATE INTEGRATION PARAMS
    """
    params = demisto.params()

    credentials = params.get('credentials') if params.get('credentials') else {}
    username: str = credentials.get('identifier', '')
    password: str = credentials.get('password', '')
    if (username and not password) or (password and not username):
        err_msg: str = 'If using credentials, both username and password should be provided.'
        demisto.debug(err_msg)
        raise DemistoException(err_msg)

    demisto.debug(f'Command being called is {demisto.command()}')

    try:
        if demisto.command() == 'long-running-execution':
            run_long_running(params)
        elif demisto.command() == 'gravity-update-cache':
            result = gravity_update_cache(demisto.args())
            return_results(result)
        elif demisto.command() == 'test-module':
            result = test_module(demisto.args(), params)
            return_results(result)


    except Exception as e:
        return_error(str(f'Failed to execute {demisto.command()} command. Error: {str(e)}'))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
