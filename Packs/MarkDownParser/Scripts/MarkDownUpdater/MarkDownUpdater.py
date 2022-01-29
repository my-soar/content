
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback
import markdown

''' STANDALONE FUNCTION '''


def markdownupdater(md_data: str, section: str, updates: str, append: str):
    updated_md_data = md_data
    return updated_md_data


''' COMMAND FUNCTION '''


def markdownupdater_command(args: Dict[str, Any]):

    field = args.get('field_name', None)
    section = args.get('md_section', None)
    updates = args.get('section_update', None)
    append = args.get('append', None)

    incident = demisto.incidents()[0]
    field_data = incident.get(field, None)

    updated_field_data = markdownupdater(md_data=field_data, section=section, updates=updates, append=append)
    print (updated_field_data)
    return_results(f"Markdown Field: {field} is updated")


''' MAIN FUNCTION '''


def main():
    try:
        markdownupdater_command(demisto.args())
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute MarkDownUpdater. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
