"""Utility methods for the README-AI project."""

import re
from pathlib import Path

import git
import nbformat
import tiktoken
from nbconvert import PythonExporter


def clone_repository(url: str, repo_path: Path) -> None:
    """Clone a repository to a temporary directory."""
    try:
        git.Repo.clone_from(url, repo_path, depth=1)
    except git.exc.GitCommandError as e:
        raise (f"Error cloning repository from {url}: {e}")


def convert_ipynb_to_py(ipynb_file_path):
    """Convert an IPython Notebook file to a Python script."""
    with open(ipynb_file_path, "r", encoding="utf-8") as nb_file:
        notebook = nbformat.read(nb_file, as_version=nbformat.NO_CONVERT)

    exporter = PythonExporter()

    (python_code, metadata) = exporter.from_notebook_node(notebook)

    return python_code


def flatten_list(nested_list):
    """Flatten a nested list."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def format_sentence(text: str) -> str:
    """Clean up a sentence generated by OpenAI's GPT API."""
    # Remove non-letter characters from beginning of string
    text = re.sub(r"^[^a-zA-Z]*", "", text)

    # Remove extra white space around punctuation except for '('
    text = re.sub(r"\s*([)'.!,?;:])(?!\.\s*\w)", r"\1", text)

    # Remove extra white space before opening parentheses
    text = re.sub(r"(\()\s*", r"\1", text)

    # Replace multiple consecutive spaces with a single space
    text = re.sub(" +", " ", text)

    # Remove extra white space around hyphens
    text = re.sub(r"\s*-\s*", "-", text)

    return text.strip().strip('"')


def get_token_count(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def truncate_text_tokens(text, encoding_name="cl100k_base", max_tokens=3900):
    """Truncate a text string to a maximum number of tokens."""
    encoding = tiktoken.get_encoding(encoding_name)
    encoded_text = encoding.encode(text)[:max_tokens]
    return encoded_text


def valid_url(s: str) -> bool:
    """Check if a given string is a valid URL."""
    regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,63}|[A-Z]{2,63}\.[A-Z]{2,63}))"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return bool(regex.match(s))
