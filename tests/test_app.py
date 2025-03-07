from main import answer_query

def test_answer_query_returns_response():
    """
    Test that the answer_query function returns a non-empty string response.
    This test checks the following:
    - The response is of type string.
    - The response is not an empty string (after stripping whitespace).
    - The response contains the word "man" or "fortune" (case insensitive), 
      which are expected to be part of the content in the Pride and Prejudice document.
    Raises:
        AssertionError: If any of the assertions fail.
    """
    query = "What is Pride and Prejudice about?"
    answer = answer_query(query)
    
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
    assert "man" in answer.lower() or "fortune" in answer.lower()

def test_empty_query_handling():
    """
    Test the handling of an empty query in the answer_query function.

    This test checks if the answer_query function returns the appropriate
    message when an empty query string is provided.

    Assertions:
        - The response should contain the message "Please enter a valid query".
    """
    answer = answer_query("")
    assert "Please enter a valid query" in answer
