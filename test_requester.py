from unittest.mock import Mock, patch
from cruncher import NumberRequester
import pytest
from datetime import datetime as dt


@patch("cruncher.requests.get")
def test_number_requester_returns_a_valid_result_when_called(mock_get):
    """Test that the call method returns a valid item.

    Given:
         A NumberRequester instance making a successful call

    Result:
        A result as a dict in the form {'result': 'SUCCESS', 'number': 13, "fact": "13 is lucky for some."}

    """
    # Arrange
    mock_get.return_value = Mock(status_code=200, text="13 is lucky for some.")

    number_requester = NumberRequester()

    expected = {"result": "SUCCESS", "number": 13, "fact": "13 is lucky for some."}
    # Act
    result = number_requester.call()
    # Assert
    assert result == expected


@pytest.mark.parametrize("status_code", [400, 404, 500])
@patch("cruncher.requests.get")
def test_number_requester_returns_error_result_for_non_200_response(
    mock_get, status_code
):
    """Test that the call method returns a valid item when a request fails.

    Given:
         A NumberRequester instance making an unsuccessful call

    Result:
        A result as a dict in the form {'result': 'FAILURE', 'error_code': 404}

    """
    # Arrange
    mock_get.return_value = Mock(status_code=status_code)

    number_requester = NumberRequester()

    expected = {"result": "FAILURE", "error_code": status_code}
    # Act
    result = number_requester.call()
    # Assert
    assert result == expected


@patch("cruncher.dt")
@patch("cruncher.requests.get")
def test_number_requester_keeps_log_of_requests(mock_get, mock_dt):
    """Test that a NumberRequester instance keeps a log of its own requests.

    Given:
        A NumberRequester is instantiated.
        The NumberRequester.call method is called 5 times at known times.

    Result:
        The NumberRequester.log attribute returns a array of five valid results. Each result
        is a serialisable dict in the form:
        {'request_number': 1, 'call_time': '2022-11-09T16:38:23.417667', 'end_point': 'http://numbersapi.com/random/math',
        'result': 'SUCCESS', 'number': 49}
    Ensure that you test that each dict is exactly correct - including the 'call_time'.
    """
    # Arrange
    mock_dt.now.side_effect = [
        dt(2024, 11, 4, 11, 10, 8, 132263),
        dt(2024, 11, 4, 11, 10, 9, 132265),
        dt(2024, 11, 4, 11, 10, 10, 132268),
        dt(2024, 11, 4, 11, 10, 11, 132271),
        dt(2024, 11, 4, 11, 10, 12, 132273),
    ]

    mock_get.return_value = Mock(status_code=200, text="13 is lucky for some.")

    number_requester = NumberRequester()

    expected_request_nums = [1, 2, 3, 4, 5]
    expected_times = [
        "2024-11-04T11:10:08.132263",
        "2024-11-04T11:10:09.132265",
        "2024-11-04T11:10:10.132268",
        "2024-11-04T11:10:11.132271",
        "2024-11-04T11:10:12.132273",
    ]
    # Act
    for _ in range(5):
        number_requester.call()
    # Assert
    assert len(number_requester.log) == 5

    for index, record in enumerate(number_requester.log):
        assert isinstance(record, dict)
        assert record["request_number"] == expected_request_nums[index]
        assert record["call_time"] == expected_times[index]
        assert record["end_point"] == "http://numbersapi.com/random/math"
        assert record["result"] == "SUCCESS"
        assert record["number"] == 13
