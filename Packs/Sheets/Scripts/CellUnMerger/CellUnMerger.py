"""Base Script for Cortex XSOAR (aka Demisto)

This is an empty script with some basic structure according
to the code conventions.

MAKE SURE YOU REVIEW/REPLACE ALL THE COMMENTS MARKED AS "TODO"

Developer Documentation: https://xsoar.pan.dev/docs/welcome
Code Conventions: https://xsoar.pan.dev/docs/integrations/code-conventions
Linting: https://xsoar.pan.dev/docs/integrations/linting

"""

import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries

''' STANDALONE FUNCTION '''


# TODO: REMOVE the following dummy function:
def basescript_dummy(dummy: str) -> Dict[str, str]:
    """Returns a simple python dict with the information provided
    in the input (dummy).

    :type dummy: ``str``
    :param dummy: string to add in the dummy dict that is returned

    :return: dict as {"dummy": dummy}
    :rtype: ``str``
    """

    return {"dummy": dummy}
# TODO: ADD HERE THE FUNCTIONS TO INTERACT WITH YOUR PRODUCT API


''' COMMAND FUNCTION '''

def list_cellunmerger (context_list: str) -> List:


# TODO: REMOVE the following dummy command function
def basescript_cellunmerger_command(args: Dict[str, Any]) -> CommandResults:

    context_list = args.get('list', None)
    sheet_file = args.get('sheet_file', None)
    object_type = args.get('object_type', None)
    unmerged_list = []
    # Call the standalone function and get the raw response
    if object_type is 'list' and context_list is None:
        return_error(f'Failed to execute CellUnMerger. Error: Please specify a contex list')
    if object_type is 'list' and sheet_file is None:
        return_error(f'Failed to execute CellUnMerger. Error: Please specify a sheet file')

    if object_type is 'list':
        unmerged_list = list_cellunmerger (context_list)
    else:
        unmerged_list = list_cellunmerger (context_list)

    result = unmerged_list

    return CommandResults(
        outputs_prefix='Sheets',
        outputs_key_field='',
        outputs=result,
    )
# TODO: ADD additional command functions that translate XSOAR inputs/outputs


''' MAIN FUNCTION '''


def main():
    try:
        # TODO: replace the invoked command function with yours
        return_results(basescript_cellunmerger_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute CellUnMerger. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
