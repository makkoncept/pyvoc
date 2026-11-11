import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from pyvoc.pyvoc import parse_dictionary_response


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _entry(category, senses):
    return {
        "lexicalCategory": {"text": category},
        "entries": [{"senses": senses}],
    }


def _response(entries):
    return _FakeResponse({"results": [{"lexicalEntries": entries}]})


def test_missing_definition_does_not_reuse_previous_entry():
    response = _response(
        [
            _entry(
                "Noun",
                [{"definitions": ["a thing"], "examples": [{"text": "an example"}]}],
            ),
            _entry("Verb", [{}]),
        ]
    )
    definitions, examples = parse_dictionary_response(response)
    assert definitions == {"Noun": "a thing"}
    assert examples == {"Noun": "an example"}


def test_missing_definition_on_first_entry_does_not_crash():
    response = _response([_entry("Noun", [{}])])
    definitions, examples = parse_dictionary_response(response)
    assert definitions == {}
    assert examples == {}
