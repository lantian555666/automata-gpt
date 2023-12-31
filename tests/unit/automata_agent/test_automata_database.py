import os
import shutil
from unittest.mock import patch

import pytest

from automata.llm import OpenAIChatMessage
from automata.memory_store import OpenAIAutomataConversationDatabase

db_dir = os.path.join(os.path.dirname(__file__), "db")
db_path = os.path.join(db_dir, "task.db")


@pytest.fixture
def db():
    """Fixture to provide a clean database for each test."""
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)  # Delete the database file

    # Setup: create a clean database
    os.mkdir(db_dir)

    db = OpenAIAutomataConversationDatabase(db_path=db_path)
    yield db

    # Teardown: clean up the database
    db.close()  # Close the connection to the database before deleting the file
    shutil.rmtree(db_dir)  # Delete the database file


# Now, you can use the db fixture in your tests like this:


def table_exists(conn, table_name):
    """Check if a table exists in the database"""
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    # if the count is 1, then table exists
    return cursor.fetchone()[0] == 1


def test_init(db):
    """Tests that the __init__ method sets up the database correctly."""
    # Check that the db table exists
    assert table_exists(
        db.conn, OpenAIAutomataConversationDatabase.PRIMARY_TABLE_NAME
    )


def test_get_last_interaction_id(db):
    """Tests that the last_interaction_id method returns the correct ID."""

    with patch(
        "automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.select"
    ) as mock_select:
        mock_select.return_value = [(5,)]
        assert db._get_last_interaction_id("test_session") == 5


def test_save_message(db):
    """Tests that the save_message method saves a message correctly."""

    with patch(
        "automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.insert"
    ) as mock_insert, patch(
        "automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.select"
    ) as mock_select:
        mock_select.return_value = [(5,)]
        message = OpenAIChatMessage(role="assistant", content="Hello, world!")
        db.save_message("test_session", message)
        mock_insert.assert_called_once()


def test_get_messages(db):
    """Tests that the get_messages method returns the correct messages."""

    with patch(
        "automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.select"
    ) as mock_select:
        mock_select.return_value = [
            ("test_session", 1, "assistant", "Hello, world!", None),
            ("test_session", 2, "user", "Hello!", None),
        ]
        messages = db.get_messages("test_session")
        assert len(messages) == 2
        assert messages[0].role == "assistant"
        assert messages[0].content == "Hello, world!"
        assert messages[1].role == "user"
        assert messages[1].content == "Hello!"


def test_invalid_session_id(db):
    """Tests that an error is raised when trying to save a message with an invalid session ID."""
    db.session_id = None
    message = OpenAIChatMessage(role="assistant", content="Hello, world!")
    with pytest.raises(ValueError):
        db.save_message(None, message)


def test_persistence(db):
    """Tests that data is persisted correctly in the database."""
    message = OpenAIChatMessage(role="assistant", content="Hello, world!")
    db.save_message("test_session", message)
    messages_before = db.get_messages("test_session")
    db.close()
    db.connect(db_path)
    messages = db.get_messages("test_session")
    assert len(messages) == 1
    assert messages[0].role == "assistant"
    assert messages[0].content == "Hello, world!"
    assert messages == messages_before


@patch(
    "automata.memory_store.conversation_database_providers.OpenAIAutomataConversationDatabase.insert"
)
def test_error_handling(mock_insert, db):
    """Tests that an error is handled correctly when a database operation fails."""
    mock_insert.side_effect = Exception("Database error")
    message = OpenAIChatMessage(role="assistant", content="Hello, world!")
    with pytest.raises(Exception) as e:
        db.save_message("test_session", message)
    assert str(e.value) == "Database error"


# TODO - It might not be great that this test is a function of the external environment
# We should consider if it is worth keeping.
@pytest.mark.performance
def test_performance(db):
    """Tests that a large number of messages can be saved and retrieved quickly."""
    import time

    messages = [
        OpenAIChatMessage(role="assistant", content="Hello, world!")
        for _ in range(1000)
    ]
    start = time.time()
    for message in messages:
        db.save_message("test_session", message)
    end = time.time()
    assert end - start < 5  # The operation should be completed within 5 second
    start = time.time()
    messages = db.get_messages("test_session")
    end = time.time()
    assert end - start < 5  # The operation should be completed within 5 second
    assert len(messages) == 1000
