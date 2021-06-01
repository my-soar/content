
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback


''' STANDALONE FUNCTION '''


def merge_lists(path1, path2, list1, list2, output):
    merged_list = []
    for item1 in path1[list1]:
        items_list = []
        for item2 in path2[list2]:
            if item1 in item2:
                items_list.append(item2)
        merged_list.append({"Parent": {list1: item1, list2: items_list}})
    return {output: merged_list}


''' COMMAND FUNCTION '''


def merge_lists_command(args: Dict[str, Any]) -> CommandResults:

    path1 = args.get('path1', None)
    path2 = args.get('path2', None)
    list1 = args.get('list1', None)
    list2 = args.get('list2', None)
    output = args.get('output', None)

    result = merge_lists(path1, path2, list1, list2, output)

    return CommandResults(
        outputs_key_field='',
        outputs=result,
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(merge_lists_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute BaseScript. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
