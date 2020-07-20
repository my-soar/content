import json


def load_test_data(json_path):
    with open(json_path) as f:
        return json.load(f)


def test_get_atom():
    atom_response = load_test_data('./test_data/get-atom.json')
    from Atom import get_atom
    args = {
        "orbit": "true",
        "center": "true"
    }
    outputs = get_atom(args).outputs
    expected_output = atom_response['Center']
    assert outputs[0]['Center'] == expected_output
