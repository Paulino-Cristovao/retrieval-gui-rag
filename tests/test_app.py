import pytest
import sys
import os

# Add the parent directory to the Python path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now we can import from main
from main import answer_query

def test_answer_query_returns_response():
    # Test that the answer_query function returns a non-empty string response
    query = "What is Pride and Prejudice about?"
    answer = answer_query(query)
    
    # Basic assertions to ensure we get a valid response
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
    # This should match content in your Pride and Prejudice document
    assert "man" in answer.lower() or "fortune" in answer.lower()

# For empty query handling
def test_empty_query_handling():
    answer = answer_query("")
    assert "Please enter a valid query" in answer
