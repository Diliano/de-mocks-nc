from unittest.mock import Mock
from cruncher import NumberCruncher
import pytest


def test_number_cruncher_likes_even_numbers():
    """Test that the crunch method saves number facts for even numbers.

    Given:
         A Number cruncher instance getting an even result for its "crunch" method (eg 42)

    Result:
        Method returns "Yum! 42"
        The tummy attribute contains a dict such as {'number': 42, "fact": "42 is the meaning of life."}

    """
    # Arrange
    mock_requester = Mock()
    mock_requester.call.return_value = {
        "result": "SUCCESS",
        "number": 42,
        "fact": "42 is the meaning of life.",
    }

    number_cruncher = NumberCruncher(1, mock_requester)

    expected_return = "Yum! 42"
    expected_tummy = [{"number": 42, "fact": "42 is the meaning of life."}]
    # Act
    result = number_cruncher.crunch()
    # Assert
    assert result == expected_return
    assert number_cruncher.tummy() == expected_tummy


def test_number_cruncher_hates_odd_numbers():
    """Test that the crunch method rejects number facts for odd numbers.

    Given:
         A Number cruncher instance getting an odd result for its "crunch" method eg 13

    Result:
        Method returns "Yuk! 13"
        The tummy attribute is unchanged.

    """
    # Arrange
    mock_requester = Mock()
    mock_requester.call.return_value = {
        "result": "SUCCESS",
        "number": 13,
        "fact": "13 is the speed of rush hour traffic on average in kilometres per hour in London.",
    }

    number_cruncher = NumberCruncher(1, mock_requester)

    expected_return = "Yuk! 13"
    expected_tummy = []
    # Act
    result = number_cruncher.crunch()
    # Assert
    assert result == expected_return
    assert number_cruncher.tummy() == expected_tummy


def test_number_cruncher_discards_oldest_item_when_tummy_full():
    """Test that the crunch method maintains a maximum number of facts.

    Given:
         A Number cruncher instance with tummy size 3 having 3 items in tummy getting
         an even result for its "crunch" method, eg 24.

    Result:
        Method deletes oldest result from tummy (eg 42)
        Method returns "Burp! 42"
        The tummy attribute contains 24 but not 42.

    """
    # Arrange
    mock_requester = Mock()
    mock_requester.call.side_effect = [
        {
            "result": "SUCCESS",
            "number": 42,
            "fact": "42 is the meaning of life.",
        },
        {
            "result": "SUCCESS",
            "number": 10,
            "fact": "10 is the number of fingers on a pair of human hands.",
        },
    ]

    number_cruncher = NumberCruncher(1, mock_requester)

    expected_return = "Burp! 42"
    expected_tummy = [
        {"number": 10, "fact": "10 is the number of fingers on a pair of human hands."}
    ]
    # Act
    number_cruncher.crunch()
    result = number_cruncher.crunch()
    # Assert
    assert result == expected_return
    assert number_cruncher.tummy() == expected_tummy


def test_number_cruncher_raises_runtime_error_if_invalid_number_request():
    """Test that there is a runtime error if NumberRequester response is
    invalid

    Given:
        A NumberCruncher instance, receiving an invalid NumberRequester
        response (eg an AttributeError)

    Result:
        Raises RuntimeError
    """
    # Arrange
    mock_requester = Mock()
    mock_requester.side_effect = AttributeError

    number_cruncher = NumberCruncher(1, mock_requester)
    # Act + Assert
    with pytest.raises(RuntimeError) as excinfo:
        number_cruncher.crunch()
    assert str(excinfo.value) == "Unexpected error"
