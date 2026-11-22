#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""


"""
Helper functions to read EM resposnes to human-readable data-files
"""


import numpy as np


def read_amt(filename):
    """
    Read frequency-domain AMT data from an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Input filename.

    Returns
    -------
    dict
        Dictionary containing:
        f : ndarray, shape (nf,)
            Frequencies in Hz.
        rx : ndarray, shape (nrx, 3)
            Receiver coordinates (X, Y, Z).
        cmp : tuple of str
            Component names.
        data : ndarray of complex, shape (nf, nrx, ncomp)
            Complex-valued AMT responses.
            Axis 0: Frequencies.
            Axis 1: Receivers.
            Axis 2: Components.
    """

    with open(filename) as f:
        lines = iter(f)
        components = None

        for line in lines:
            line = line.strip()

            if line.startswith('# COMPONENTS'):
                components = np.array(line.split()[2:])

            elif line.startswith('# FREQUENCIES_HZ'):
                nf = int(line.split()[-1])
                frequencies = np.fromstring(next(lines), sep=' ')

            elif line == '# RECEIVERS':
                next(lines)
                rx_coords = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        break
                    rx_coords.append([float(v) for v in line.split()[1:]])
                rx_coords = np.asarray(rx_coords)

            elif line == '# AMT DATA VALUES':
                next(lines)
                nrx, nc = len(rx_coords), len(components)
                data = np.zeros((nf, nrx, nc), dtype=complex)

                for jf in range(nf):
                    for irx in range(nrx):
                        line = next(lines).strip()
                        while not line or line.startswith('#'):
                            line = next(lines).strip()
                        values = np.fromstring(line, sep=' ')[1:]
                        data[jf, irx] = values[::2] + 1j * values[1::2]
                break

    return {'f': frequencies, 'rx': rx_coords, 'cmp': components,
            'data': data}


def read_csem(filename):
    """
    Read frequency-domain CSEM data from an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Input filename.

    Returns
    -------
    dict
        Dictionary containing:
        f : ndarray, shape (nf,)
            Frequencies in Hz.
        rx : ndarray, shape (nrx, 3)
            Receiver coordinates (X, Y, Z).
        cmp : tuple of str
            Component names.
        data : ndarray of complex, shape (nf, nrx, ncomp)
            Complex-valued CSEM responses.
            Axis 0: Frequencies.
            Axis 1: Receivers.
            Axis 2: Components.
        tx_id : int
            Transmitter identifier.
        tx_position : ndarray, shape (3,) or None
            Transmitter coordinates (X, Y, Z).
    """

    with open(filename) as f:
        lines = iter(f)
        tx_id, tx_position, components = None, None, None

        for line in lines:
            line = line.strip()

            if line.startswith('# TX_ID'):
                tx_id = int(line.split()[-1])

            elif line.startswith('# TX_POSITION'):
                tx_position = np.array([float(v) for v in line.split()[2:]])

            elif line.startswith('# COMPONENTS'):
                components = np.array(line.split()[2:])

            elif line.startswith('# FREQUENCIES_HZ'):
                nf = int(line.split()[-1])
                frequencies = np.fromstring(next(lines), sep=' ')

            elif line == '# RECEIVERS':
                next(lines)
                rx_coords = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        break
                    rx_coords.append([float(v) for v in line.split()[1:]])
                rx_coords = np.asarray(rx_coords)

            elif line == '# CSEM DATA VALUES':
                next(lines)
                nrx, nc = len(rx_coords), len(components)
                data = np.zeros((nf, nrx, nc), dtype=complex)

                for jf in range(nf):
                    for irx in range(nrx):
                        line = next(lines).strip()
                        while not line or line.startswith('#'):
                            line = next(lines).strip()
                        values = np.fromstring(line, sep=' ')[1:]
                        data[jf, irx] = values[::2] + 1j * values[1::2]
                break

    return {'f': frequencies, 'rx': rx_coords, 'cmp': components,
            'data': data, 'tx_id': tx_id, 'tx_position': tx_position}


def read_tem(filename):
    """
    Read time-domain TEM data from an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Input filename.

    Returns
    -------
    dict
        Dictionary containing:
        t : ndarray, shape (nt,)
            Measurement times in seconds.
        rx : ndarray, shape (nrx, 3)
            Receiver coordinates (X, Y, Z).
        cmp : tuple of str
            Component names.
        data : ndarray of float, shape (nt, nrx, ncomp)
            Real-valued TEM responses.
            Axis 0: Time channels.
            Axis 1: Receivers.
            Axis 2: Components.
    """

    with open(filename) as f:
        lines = iter(f)
        components = None

        for line in lines:
            line = line.strip()

            if line.startswith('# COMPONENTS'):
                components = np.array(line.split()[2:])

            elif line.startswith('# TIMES_S'):
                nt = int(line.split()[-1])
                times = np.fromstring(next(lines), sep=' ')

            elif line == '# RECEIVERS':
                next(lines)
                rx_coords = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        break
                    rx_coords.append([float(v) for v in line.split()[1:]])
                rx_coords = np.asarray(rx_coords)

            elif line == '# TEM DATA VALUES':
                next(lines)
                nrx, nc = len(rx_coords), len(components)
                data = np.zeros((nt, nrx, nc))

                for jt in range(nt):
                    for irx in range(nrx):
                        line = next(lines).strip()
                        while not line or line.startswith('#'):
                            line = next(lines).strip()
                        values = np.fromstring(line, sep=' ')[1:]
                        data[jt, irx] = values
                break

    return {'t': times, 'rx': rx_coords, 'cmp': components, 'data': data}