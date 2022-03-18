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
import zlib
import binascii

''' STANDALONE FUNCTION '''


def zlib_data(function_name, data_to_process, compression_level, hash_type):

    match function_name:
        case 'compress':
            processed_data = zlib.compress(bytes(data_to_process, 'utf-8'), int(compression_level))
        case 'decompress':
            data_to_process_binary = data_to_process.encode('iso-8859-15')
            print(data_to_process_binary)
            processed_data = zlib.decompress(data_to_process_binary)
            print(processed_data)
        case 'hash':
            match hash_type:
                case 'crc32':
                    processed_data = zlib.crc32(data_to_process)
                case 'alder32':
                    processed_data = zlib.adler32(data_to_process)

    return {"processed_data": str(processed_data) }


''' COMMAND FUNCTION '''


def zlib_data_command(args: Dict[str, Any]) -> CommandResults:

    function_name = args.get('function_name')
    data_to_process = args.get('data_to_process')
    compression_level = args.get('compression_level')
    hash_type = args.get('hash_type')

    result = zlib_data(function_name=function_name, data_to_process=data_to_process,
                       compression_level=compression_level, hash_type=hash_type)

    zlib_output = {
        "Input": data_to_process,
        "Output": result.get('processed_data'),
        "Function": function_name
    }
    return CommandResults(
        outputs_prefix='Zlib',
        outputs_key_field='',
        outputs=zlib_output,
    )


''' MAIN FUNCTION '''


def main():
    try:
        return_results(zlib_data_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute Zlib. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
