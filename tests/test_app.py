import pytest
from main import answer_query

def test_answer_query():
    # A simple test to ensure that a query returns a non-empty string.
    query = "What is the capital of France?"
    answer = answer_query(query)
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
