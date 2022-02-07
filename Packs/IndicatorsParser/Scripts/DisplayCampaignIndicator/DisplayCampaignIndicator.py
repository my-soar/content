register_module_line('DisplayCampaignIndicator', 'start', __line__())

import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback


''' STANDALONE FUNCTION '''

def displaycampaignindicator(campaign_details):
    md = "\r\n\r\n"
    md += "### Campaign Overview"
    md += "\r\n\r\n"
    md += campaign_details.get('CustomFields', None).get('description',None)
    md += "\r\n\r\n"
    md += "### Campaign Publications"
    md += "\r\n\r\n"

    for publication in campaign_details.get('CustomFields', None).get('publications'):
        md += f"[{publication.get('title', None)}]({publication.get('link', None)})"
        md += "\r\n\r\n"
    return md


''' COMMAND FUNCTION '''

def displaycampaignindicator_command() -> CommandResults:
    campaign_name = demisto.incidents()[0].get('CustomFields',None).get('campaignname',None)
    if not campaign_name:
        raise ValueError('Campaign name field is empty')

    campaign_details = execute_command("findIndicators", {'value': campaign_name, 'raw-response': 'true'})[0]

    result_md = displaycampaignindicator(campaign_details)

    return CommandResults(
        readable_output=result_md
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(displaycampaignindicator_command())
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute DisplayCampaingIndicator. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
