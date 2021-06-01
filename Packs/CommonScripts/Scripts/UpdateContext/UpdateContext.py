
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback


''' COMMAND FUNCTION '''


def update_context_command(args: Dict[str, Any]) -> CommandResults:

    to = args.get('to', None)
    id = args.get('id', None)
    source = args.get('source', None)

    return CommandResults(
        outputs_prefix=to,
        outputs_key_field=id,
        outputs=source,
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(update_context_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute BaseScript. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
