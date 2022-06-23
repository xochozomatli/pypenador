"""Scrounge Module

Functions for scrounging.
"""

import re
import multiprocessing as mp
import os
import sys
import logging
from typing import BinaryIO

from .constants import FILE_BOUNDS, DEFAULT_BATCH_SIZE, DEFAULT_FILE_TYPE


def buffer(filename: str, batch_size: int = DEFAULT_BATCH_SIZE) -> bytes:
    """Generator that reads a file in chunks and returns bytes.

    Parameters
    ----------
    filename : str
        Path to file to be read.
    batch_size : int, optional
        Number of bytes to read at a time.

    Yields
    ------
    chunk : bytes
        byte string of size batch_size
    """
    with open(filename, 'rb') as fd:
        yield (chunk := fd.read(batch_size))
        while chunk:
            chunk = fd.read(batch_size)
            yield chunk


def search_buffer(
        byte_string, file_bounds=FILE_BOUNDS[DEFAULT_FILE_TYPE]):
    """Finds substrings of a byte string that match start of file
    of end of file sequences.

    Parameters
    ----------
    byte_string : bytes
        Byte string to search.
    file_bounds : tuple, optional
        Tuple of two byte strings. The first is the start of file, the second
        is the end of file.

    Returns
    -------
    list of (start, end, group) triples
    """
    header, eof = file_bounds
    boundaries_regex = header + b"|" + eof
    return [(m.start(), m.end(), m.group()) for m in re.finditer(boundaries_regex, byte_string)]

def compile_boundary_lists(buf_gen, finder=search_buffer,
                       batch_size=DEFAULT_BATCH_SIZE):
    """Finds all file boundaries in a generator of byte strings,
    translating buffer offsets to file offsets.

    Parameters
    ----------
    boundaries = []
    for i, buf in enumerate(buf_gen):
        boundaries.append(boundary_finder(buf))
    return boundaries
    """
    boundaries = []
    for i, buf in enumerate(buf_gen):
        boundaries.extend([(x[0] + (batch_size * i),
                            x[1] + (batch_size * i),
                            x[2]) for x in finder(buf)])
    return boundaries


def match(boundary_match_list, header=FILE_BOUNDS[DEFAULT_FILE_TYPE][0],
          eof=FILE_BOUNDS[DEFAULT_FILE_TYPE][1]):
    """
    header offsets, footer offsets => generator of file offsets spans
    """
    pairs = []
    header_ix = None
    for start, end, group in boundary_match_list:
        if group == header:
            header_ix = start
            continue
        if header_ix is not None:
            pairs.append((header_ix, end))
            header_ix = None
    return pairs


def retrieve(fd: BinaryIO, start: int, end: int) -> bytes:
    """
    data file descriptor, start offset, end offset =>
    copy of suspected file as bytestring
    """
    size = end - start
    fd.seek(start)
    data = fd.read(size)
    return data


def find_files(
        filename: str, file_type: str = DEFAULT_FILE_TYPE,
        batch_size: int = DEFAULT_BATCH_SIZE):
    """Finds all candidate bytestrings
    corresponding to file_type.

    Parameters
    ----------
    filename : str
        Path to file to be read.
    file_type : str, optional
        File type to be searched for.
    batch_size : int, optional
        Number of bytes to read into buffer at each step.

    Returns
    -------
    generator of candidate bytes strings
    """
    candidate_ix_spans = match(
                    compile_boundary_lists(
                        buffer(filename, batch_size)),
                    header=FILE_BOUNDS[file_type][0],
                    eof=FILE_BOUNDS[file_type][1])

    with open(filename, 'rb') as fd:
        for ix_span in candidate_ix_spans:
            yield retrieve(fd, ix_span[0], ix_span[1])
