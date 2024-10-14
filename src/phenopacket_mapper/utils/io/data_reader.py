from pathlib import Path
from typing import Union, Tuple, List, Iterable, Literal, Dict
from io import IOBase, TextIOWrapper, BytesIO, BufferedIOBase, TextIOBase

import pandas as pd

from phenopacket_mapper.utils.io import read_json, read_xml


class DataReader:
    def __init__(
            self,
            file: Union[str, Path, IOBase, List[str], List[Path], List[IOBase]],
            encoding: str = 'utf-8',
            file_extension: Literal['csv', 'xlsx', 'json', 'xml'] = None
    ):
        """Initializes the data reader.

        :param file: a `str`, :class:`Path` or :class:`IOBase` to read from. If `str` or :class:`Path`, then the
        input is interpreted as a path to a local file.
        :param encoding: The encoding to use when reading the file. Default is 'utf-8'.
        :param file_extension: The file extension of the file to read. If `None`, the file extension is inferred from the
        file path. Default is `None`.
        """
        # TODO: fix read xml
        # TODO: add option to pass a list of files to read
        self.is_dir = False
        self.file_extension = None

        if isinstance(file, str):
            self.path = Path(file)
            self.file = open(self.path, "r", encoding=encoding)

            if file_extension is None:  # extract the file extension from the file path
                file_extension = self.path.suffix[1:]

            self.handle_file_extension(file_extension)
        elif isinstance(file, Path):
            if not file.exists():
                raise FileNotFoundError(f"File {file} does not exist.")
            if file.is_file():
                self.path = file
                self.file = open(self.path, "r", encoding=encoding)

                if file_extension is None:  # extract the file extension from the file path
                    file_extension = self.path.suffix[1:]

                self.handle_file_extension(file_extension)
            elif file.is_dir():
                self.is_dir = True

        elif isinstance(file, IOBase):
            if isinstance(file, (TextIOWrapper, TextIOBase)):
                pass
            elif isinstance(file, (BytesIO, BufferedIOBase)):
                self.file = TextIOWrapper(file, encoding=encoding)

            if file_extension is None:
                raise ValueError("File extension must be provided when passing a file buffer.")
            else:
                self.handle_file_extension(file_extension)

        self.data, self.iterable = self._read()

    def handle_file_extension(self, fe: str):
        if fe.lower() in ['csv', 'xlsx', 'json', 'xml']:
            self.file_extension = fe.lower()
        else:
            raise ValueError(f"File extension {fe} not recognized.")

    def _read(self) -> Tuple[Union[pd.DataFrame, List, Dict], Iterable]:
        """Reads the data.

        :return: The data and an iterable representation of the data.
        """
        # we know that file is always a buffer with the contents of the file
        # change this to work with self.file
        if not self.is_dir:
            if self.file_extension == 'csv':
                df = pd.read_csv(self.file)
                return df, [row for row in df.iterrows()]
            elif self.file_extension == 'xlsx':
                df = pd.read_excel(self.file)
                return df, [row for row in df.iterrows()]
            elif self.file_extension == 'json':
                return file_contents := read_json(self.file), [file_contents]
            elif self.file_extension == 'xml':
                return file_contents := read_xml(self.file), [file_contents]
            else:
                raise ValueError(f'Unknown file type with extension {self.file_extension}')
        elif self.is_dir:
            # collect list of all files in the folder
            files: List[Path] = [file for file in self.path.iterdir() if file.is_file()]
            file_extension = list(set([file.suffix[1:] for file in files]))
            if len(file_extension) > 1:
                raise ValueError(f"Cannot read files of different types: {file_extension}")
            elif len(file_extension) == 0:
                raise ValueError(f"No files found in the directory specified: {self.file}")

            self.handle_file_extension(file_extension[0])

            if self.file_extension == 'json':
                jsons = [read_json(file) for file in files]
                return jsons, jsons
            elif self.file_extension == 'xml':
                xmls = [read_xml(file) for file in files]
                return xmls, xmls
            else:
                raise ValueError(f"File extension {file_extension} not recognized or not supported for reading files "
                                 f"from a directory. Specified directory: {self.file}. Extensions found: "
                                 f"{file_extension}")
