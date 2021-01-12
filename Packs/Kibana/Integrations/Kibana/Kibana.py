
import demistomock as demisto
from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
from CommonServerUserPython import *  # noqa
import urllib3
import uuid
import traceback
from typing import Dict, Any

# Disable insecure warnings
urllib3.disable_warnings()  # pylint: disable=no-member


''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR

''' CLIENT CLASS '''


class Client(BaseClient):

    def get_signals_index(self) -> Dict[str, str]:
        response = self._http_request(method='Get', url_suffix='detection_engine/index')
        return response

    def set_signal_status(self, signal, status) -> Dict[str, str]:
        guid = uuid.uuid4()
        headers = {
            'kbn-xsrf': str(guid)
        }
        body = json.dumps({
          "signal_ids": [
            signal
          ],
          "status": status
        })

        print (body)
        response = self._http_request(method='Post', url_suffix='detection_engine/signals/status', data=body, headers=headers)
        return response

''' HELPER FUNCTIONS '''

# TODO: ADD HERE ANY HELPER FUNCTION YOU MIGHT NEED (if any)

''' COMMAND FUNCTIONS '''


def test_module(client: Client) -> str:
    try:
        client.get_signals_index()
        message = 'ok'
    except DemistoException as e:
        if 'Forbidden' in str(e) or 'Authorization' in str(e):  # TODO: make sure you capture authentication errors
            message = 'Authorization Error: make sure credentials are correctly set'
        else:
            raise e
    return message


def kibana_get_signals_index_command(client: Client, args: Dict[str, Any]) -> CommandResults:

    result = client.get_signals_index()
    return CommandResults(
        outputs_prefix='Kibana.Index',
        outputs_key_field='',
        outputs=result
    )


def kibana_set_signal_status_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    signal = args.get('signal')
    status = args.get('status')
    result = client.set_signal_status(signal=signal, status=status)
    if int(result.get('batches')) > 0:
        result = {
            'signals updated': int(result.get('batches'))
        }
        return CommandResults(
            outputs_prefix='',
            outputs_key_field='',
            outputs=result
        )
    else:
        return_error('Failed to update the signal status')

''' MAIN FUNCTION '''


def main() -> None:

    base_url = urljoin(demisto.params()['url'], '/api')
    verify_certificate = not demisto.params().get('insecure', False)
    proxy = demisto.params().get('proxy', False)
    username = demisto.params().get('credentials', {}).get('identifier')
    password = demisto.params().get('credentials', {}).get('password')
    auth = (username, password)
    demisto.debug(f'Command being called is {demisto.command()}')
    try:
        headers: Dict = {}

        client = Client(
            base_url=base_url,
            verify=verify_certificate,
            headers=headers,
            proxy=proxy,
            auth=auth
            )

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client)
            return_results(result)

        elif demisto.command() == 'kibana-get-signals-index':
            return_results(kibana_get_signals_index_command(client, demisto.args()))

        elif demisto.command() == 'kibana-set-signal-status':
            return_results(kibana_set_signal_status_command(client, demisto.args()))

    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
