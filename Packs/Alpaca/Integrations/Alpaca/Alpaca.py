from CommonServerPython import *
from CommonServerUserPython import *
''' IMPORTS '''

import urllib3
import requests

# Disable insecure warnings
urllib3.disable_warnings()


''' CONSTANTS '''


INTEGRATION_NAME = 'Alpaca'


'''API Client'''


class Client(BaseClient):

    api_id = ''
    api_secret_key = ''
    api_request_headers = {}

    def update_api_credentials(self, api_id, api_secret_key):
        self.api_id = api_id
        self.api_secret_key = api_secret_key
        self.api_request_headers = {
            "APCA-API-KEY-ID": self.api_id,
            "APCA-API-SECRET-KEY": self.api_secret_key
        }

    def get_clock(self):
        LOG('Getting Clock Value')
        res = self._http_request(
            "GET",
            url_suffix='/v2/clock',
            resp_type="json",
            headers=self.api_request_headers
        )
        return res

    def get_account_information(self):
        LOG('Getting Account Information')
        res = self._http_request(
            "GET",
            url_suffix='/v2/account',
            resp_type="json",
            headers=self.api_request_headers
        )
        return res

    def get_last_trade(self,ticker):
        LOG('Getting Last Trade Information')
        res = self._http_request(
            "GET",
            url_suffix='/v1/last/stocks/'+ticker,
            resp_type="json",
            headers=self.api_request_headers
        )
        return res

'''' Commands '''


def test_module(client):
    res = client.get_clock()
    if res['is_open'] == 'true' or 'false':
        return 'ok'
    else:
        return 'Failed to connect to the API'


def get_account_info(client):
    title = f'{INTEGRATION_NAME} - Account Information'
    raw_response = client.get_account_information()

    if raw_response:
        raws = alpaca_ec = raw_response
    else:
        return f'{INTEGRATION_NAME} - Could not find any Accounts'

    context_entry = {
        "Alpaca.Account": alpaca_ec
    }

    human_readable = tableToMarkdown(t=context_entry.get('Alpaca.Account'), name=title)
    return [human_readable, context_entry, raws]


def get_last_trade(client, args):
    title = f'{INTEGRATION_NAME} - Last Trade Information'
    raw_response = client.get_last_trade(args['ticker'])
    if raw_response:
        raws = raw_response
        alpaca_ec ={
            "Ticker": raw_response['symbol'],
            "Price": raw_response['last']['price'],
            "TimeStamp": raw_response['last']['timestamp']
        }
    else:
        return f'{INTEGRATION_NAME} - Could not Get The Last Trade Information'

    context_entry = {
        "Alpha.Stock.LastTrade": alpaca_ec
    }

    human_readable = tableToMarkdown(t=context_entry.get('Alpha.Stock.LastTrade'), name=title)
    return [human_readable, context_entry, raws]


def main():
    """
        PARSE AND VALIDATE INTEGRATION PARAMS
    """
    params = demisto.params()
    api_id = params.get('credentials', {}).get('identifier', '')
    api_secret_key = params.get('credentials', {}).get('password', '')
    base_url = params['url'][:-1] if (params['url'] and params['url'].endswith('/')) else params['url']
    data_url = params['dataURL'][:-1] if (params['dataURL'] and params['dataURL'].endswith('/')) else params['dataURL']
    verify_certificate = not params.get('insecure', False)
    proxy = params.get('proxy', False)

    demisto.debug(f'Command being called is {demisto.command()}')

    try:
        account_client = Client(
            base_url=base_url,
            verify=verify_certificate,
            proxy=proxy,
            ok_codes=(200, 201, 204),
            headers={'accept': "application/json"}
        )
        account_client.update_api_credentials(api_id=api_id, api_secret_key=api_secret_key)

        data_client = Client(
            base_url=data_url,
            verify=verify_certificate,
            proxy=proxy,
            ok_codes=(200, 201, 204),
            headers={'accept': "application/json"}
        )
        data_client.update_api_credentials(api_id=api_id, api_secret_key=api_secret_key)


        if demisto.command() == 'test-module':
            result = test_module(account_client)
            return_outputs(result)

        elif demisto.command() == 'alpaca-get-account-information':
            result = get_account_info(account_client)
            return_outputs(*result)

        elif demisto.command() == 'alpaca-get-last-trade':
            result = get_last_trade(data_client, demisto.args())
            return_outputs(*result)

    except Exception as e:
        return_error(str(f'Failed to execute {demisto.command()} command. Error: {str(e)}'))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
