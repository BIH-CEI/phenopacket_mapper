import json
from pathlib import Path


class NotebookBuilder:
    """
    A class to build a Jupyter notebook programmatically.
    """

    def __init__(self):
        """
        Initializes a new instance of the NotebookBuilder class.

        Sets up the initial structure of the notebook with metadata and an empty list of cells.
        """
        self.notebook_content = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.x"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }

    def add_markdown_cell(self, text):
        """
        Adds a Markdown cell to the notebook.

        :param text: The Markdown content to be added to the cell.
        """
        cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [text]
        }
        self.notebook_content['cells'].append(cell)

    def add_code_cell(self, code):
        """
        Adds a code cell to the notebook.

        :param code: The Python code to be added to the cell.
        """
        cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [code]
        }
        self.notebook_content['cells'].append(cell)

    def write_to_file(self, path: Path):
        """
        Writes the notebook content to a file.

        :param path: The name of the file where the notebook will be saved.
        """
        with open(path, 'w') as f:
            json.dump(self.notebook_content, f, indent=4)
        print(f"Notebook saved to {path.absolute()}")


# Example usage
if __name__ == "__main__":
    builder = NotebookBuilder()
    builder.add_markdown_cell("# My Notebook")
    builder.add_code_cell("import numpy as np")
    builder.add_code_cell("x = np.linspace(0, 10, 100)\nprint(x)")
    builder.add_markdown_cell("## Analysis")
    builder.add_code_cell("y = np.sin(x)\nprint(y)")
    builder.write_to_file(Path('my_notebook.ipynb'))
