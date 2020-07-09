from CommonServerPython import *


def test_module():
    """
    Returning 'ok' indicates that the integration works like it is supposed to.
    """
    try:
        x = 1 + 1
        if x == 2:
            return 'ok'
    except Exception as e:
        demisto.error(e)


def get_atom(args):
    """
    Args:
        args (dict): all command arguments.

    Returns:
        CommandResults Object, for more info:
        https://xsoar.pan.dev/docs/integrations/code-conventions#commandresults
    """
    orbit = args.get('orbit')
    center = args.get('center')

    raw = []
    context = []

    if orbit == 'true' and center == 'true':
        raw.append({
            'Center': 'nucleus',
            'Orbit': 'electron'
        })
        context.append({
            'Center': 'nucleus',
            'Orbit': 'electron'
        })
    elif center == 'true':
        raw.append({
            'Center': 'nucleus',
            'Orbit': 'void'
        })
        context.append({
            'Center': 'nucleus',
            'Orbit': 'void'
        })
    elif orbit == 'true':
        raw.append({
            'Center': 'void',
            'Orbit': 'electron'
        })
        context.append({
            'Center': 'void',
            'Orbit': 'electron'
        })
    else:
        raw.append({
            'Center': 'void',
            'Orbit': 'void'
        })
        context.append({
            'Center': 'void',
            'Orbit': 'void'
        })
    return CommandResults(
        outputs_prefix="Atom",
        outputs=context,
        outputs_key_field="center"
    )


def main():
    demisto.info(f'Command being called is {demisto.command()}')
    try:
        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module()
            return_results(result)

        elif demisto.command() == 'get-atom':
            result = get_atom(args=demisto.args())
            return_results(result)

    # Log exceptions
    except Exception as e:
        return_error(f'Failed to execute {demisto.command()} command. Error: {str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
