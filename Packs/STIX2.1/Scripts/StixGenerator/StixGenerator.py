
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback
import stix2generator
import stix2generator.language.builder
import stix2generator.generation.object_generator
import stix2generator.logging
import configparser


''' STANDALONE FUNCTION '''


# TODO: REMOVE the following dummy function:
def stix2generator_function(prototype_file, export, extra_specs, embed_variable_names, config) -> Dict[str, str]:

    with open(prototype_file, "r", encoding='utf-8') as f:
        proto_lang = f.read()

    if extra_specs:
        with open(extra_specs, "r", encoding='utf-8') as f:
            extra_specs = json.load(f)

    tmp_config = {}
    if config:
        config_parser = configparser.SafeConfigParser()
        config_parser.read(config)
        tmp_config = config_parser['main']

    generator_config = stix2generator.generation.object_generator.Config(
        **tmp_config
    )

    processor = stix2generator.create_default_language_processor(
        generator_config, extra_specs, '2.1'
    )
    stix_objs = processor.build_graph(
        proto_lang, embed_variable_names=embed_variable_names
    )

    if export:
        bundle = stix2generator.utils.make_bundle(
            stix_objs, '2.1'
        )
        return bundle.serialize(pretty=True)
    else:
        for obj in stix_objs:
            return obj.serialize(pretty=True)


''' COMMAND FUNCTION '''


# TODO: REMOVE the following dummy command function
def stix2parser_command(args: Dict[str, Any]) -> CommandResults:

    prototype_file = args.get('prototype', None)
    export = args.get('export', False)
    extra_specs = args.get('extra_specs', None)
    embed_variable_names = args.get('embed_variable_names', None)
    config = args.get('config', None)

    result = stix2generator_function(prototype_file=prototype_file,
                                     export=export,
                                     extra_specs=extra_specs,
                                     embed_variable_names=embed_variable_names,
                                     config=config)

    return CommandResults(
        outputs_prefix='STIX2',
        outputs_key_field='',
        outputs=result,
    )


''' MAIN FUNCTION '''


def main():
    try:
        # TODO: replace the invoked command function with yours
        return_results(stix2parser_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute BaseScript. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
