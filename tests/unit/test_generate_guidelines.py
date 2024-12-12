import pytest
from unittest.mock import patch, MagicMock
from ai_dev_toolkit.commands.generate_guideline import GenerateGuidelineCommand, GuidelineResult

def test_generate_guideline_command_initialization():
    cmd = GenerateGuidelineCommand()
    assert cmd.name == "generate-guideline"
    assert cmd.help == "Generate a guideline from a file"

@patch('builtins.open', create=True)
def test_should_read_file_content_when_given_valid_path(mock_open):
    # Setup
    mock_file = MagicMock()
    mock_file.read.return_value = "test content"
    mock_open.return_value.__enter__.return_value = mock_file
    
    # Execute
    cmd = GenerateGuidelineCommand()
    content = cmd._read_file("test.py")
    
    # Verify
    assert content == "test content"
    mock_open.assert_called_once_with("test.py", "r")

def test_should_generate_guideline_when_given_file_content():
    # Setup
    cmd = GenerateGuidelineCommand()
    mock_agent = MagicMock()
    mock_result = MagicMock()
    mock_result.data = GuidelineResult(guideline="test guideline")
    mock_agent.run_sync.return_value = mock_result
    cmd.agent = mock_agent
    
    # Execute
    guideline = cmd._generate_guideline("test content")
    
    # Verify
    assert guideline == "test guideline"
    mock_agent.run_sync.assert_called_once()

@patch('builtins.open', create=True)
def test_should_save_guideline_when_given_content_and_path(mock_open):
    # Setup
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    
    # Execute
    cmd = GenerateGuidelineCommand()
    cmd._save_guideline("test guideline", "test.py")
    
    # Verify
    mock_open.assert_called_once_with("test.py.guideline.md", "w")
    mock_file.write.assert_called_once_with("test guideline")

def test_should_execute_full_workflow_when_given_valid_inputs():
    # Setup
    cmd = GenerateGuidelineCommand()
    
    # Mock file operations
    mock_content = "test content"
    cmd._read_file = MagicMock(return_value=mock_content)
    cmd._save_guideline = MagicMock()
    
    # Mock agent
    mock_agent = MagicMock()
    mock_result = MagicMock()
    mock_result.data = GuidelineResult(guideline="test guideline")
    mock_agent.run_sync.return_value = mock_result
    cmd.agent = mock_agent
    
    # Execute
    cmd.execute("test.py")
    
    # Verify file read
    cmd._read_file.assert_called_once_with("test.py")
    # Verify guideline generation
    mock_agent.run_sync.assert_called_once()
    # Verify guideline save
    cmd._save_guideline.assert_called_once_with("test guideline", "test.py")
