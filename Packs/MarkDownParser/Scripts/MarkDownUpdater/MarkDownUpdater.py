
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback
import markdown

''' STANDALONE FUNCTION '''


def markdownupdater(section: str) -> Dict[str, str]:

    return {"dummy": dummy}


''' COMMAND FUNCTION '''


def markdownupdater_command(args: Dict[str, Any]) -> CommandResults:

    dummy = args.get('dummy', None)
    if not dummy:
        raise ValueError('dummy not specified')

    result = basescript_dummy(dummy)

    return CommandResults(
        outputs_prefix='MarkDownUpdater',
        outputs_key_field='',
        outputs=result,
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(markdownupdater_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute MarkDownUpdater. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
