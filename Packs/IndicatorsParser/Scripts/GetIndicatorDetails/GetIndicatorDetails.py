
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback


''' STANDALONE FUNCTION '''


def get_indicator_details(value: str) -> Dict[str, str]:
    indicators = execute_command("findIndicators", {'value': value, 'raw-response': 'true'})[0]
    if not indicators:
        return {}
    return indicators


''' COMMAND FUNCTION '''


def get_indicator_details_command(args: Dict[str, Any]) -> CommandResults:

    value = args.get('indicator_value', None)
    if not value:
        raise ValueError('Indicator value not specified')

    result = get_indicator_details(value)

    readable_data = {
        "Value": str(result['value']),
        "ID": result['id'],
        "Type": result['indicator_type'],
        "Source": result['sourceBrands'],
    }

    readable_output = tableToMarkdown(t=readable_data, name='Indicator Parsed')

    return CommandResults(
        outputs_prefix='IndicatorDetails',
        outputs_key_field='id',
        readable_output=readable_output,
        outputs=result
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(get_indicator_details_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())
        return_error(f'Failed to execute GetIndicatorDetails. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
