#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""


"""
Helper functions to write EM resposnes to human-readable data-files
"""


def write_amt(filename, DATA, frequencies, rx_coords,
              components=('Zxx', 'Zxy', 'Zyx', 'Zyy', 'Tx', 'Ty')):
    """
    Write frequency-domain AMT data to an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Output filename.

    DATA : ndarray of complex, shape (nf, nrx, ncomp)
        Complex-valued AMT responses.
        Axis 0: Frequencies, matching `frequencies`.
        Axis 1: Receivers, matching `rx_coords`.
        Axis 2: Components, matching `components`.
        Each complex value is written as separate real and imaginary parts.

    frequencies : ndarray of float, shape (nf,)
        Frequencies in Hz.

    rx_coords : ndarray of float, shape (nrx, 3)
        Receiver coordinates (X, Y, Z).

    components : tuple of str, optional
        Component names corresponding to the last axis of DATA.
        Default: ('Zxx', 'Zxy', 'Zyx', 'Zyy', 'Tx', 'Ty').

    Notes
    -----
    Data are stored frequency by frequency, with one row per receiver.
    Complex-valued components are written as interleaved real and
    imaginary values (Re, Im).
    """

    nf = len(frequencies)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# AMT frequency-domain data\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# FREQUENCIES_HZ {nf}\n")
        f.write(" ".join(f"{v:.8g}" for v in frequencies) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# AMT DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(
            f"{c}_{p}" for c in components for p in ('Re', 'Im')
        ))
        f.write("\n")

        for jf in range(nf):
            f.write(f"\n#f{jf:02d}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jf][irx][:6]:
                    row.extend((f"{z.real:.8e}", f"{z.imag:.8e}"))
                f.write(" ".join(row) + "\n")

def write_csem(filename, DATA, frequencies, rx_coords, tx_id=1,
               tx_position=None,
               components=('Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz')):
    """
    Write frequency-domain CSEM data to an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Output filename.

    DATA : ndarray of complex, shape (nf, nrx, ncomp)
        Complex-valued CSEM responses.
        Axis 0: Frequencies, matching `frequencies`.
        Axis 1: Receivers, matching `rx_coords`.
        Axis 2: Components, matching `components`.
        Each complex value is written as separate real and imaginary parts.

    frequencies : ndarray of float, shape (nf,)
        Frequencies in Hz.

    rx_coords : ndarray of float, shape (nrx, 3)
        Receiver coordinates (X, Y, Z).

    tx_id : int, optional
        Transmitter identifier. Default is 1.

    tx_position : array-like of float, shape (3,), optional
        Transmitter coordinates (X, Y, Z).

    components : tuple of str, optional
        Component names corresponding to the last axis of DATA.
        Default: ('Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz').

    Notes
    -----
    Data are stored frequency by frequency, with one row per receiver.
    Complex-valued components are written as interleaved real and
    imaginary values (Re, Im).
    """

    nf = len(frequencies)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# CSEM frequency-domain data\n\n")

        f.write(f"# TX_ID {tx_id:02d}\n\n")
        if tx_position is not None:
            f.write("# TX_POSITION " + " ".join(map(str, tx_position)) + "\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# FREQUENCIES_HZ {nf}\n")
        f.write(" ".join(f"{v:.8g}" for v in frequencies) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# CSEM DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(
            f"{c}_{p}" for c in components for p in ('Re', 'Im')
        ))
        f.write("\n")

        for jf in range(nf):
            f.write(f"\n#f{jf:02d}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jf][irx]:
                    row.extend((f"{z.real:.8e}", f"{z.imag:.8e}"))
                f.write(" ".join(row) + "\n")


def write_tem(filename, DATA, times, rx_coords,
              components=('Ex', 'Ey', 'Ez', 'dBx', 'dBy', 'dBz')):
    """
    Write time-domain TEM data to an ASCII file.

    Parameters
    ----------
    filename : str or pathlib.Path
        Output filename.

    DATA : ndarray of float, shape (nt, nrx, ncomp)
        Real-valued TEM responses.
        Axis 0: Time channels, matching `times`.
        Axis 1: Receivers, matching `rx_coords`.
        Axis 2: Components, matching `components`.

    times : ndarray of float, shape (nt,)
        Measurement times in seconds.

    rx_coords : ndarray of float, shape (nrx, 3)
        Receiver coordinates (X, Y, Z).

    components : tuple of str, optional
        Component names corresponding to the last axis of DATA.
        Default: ('Ex', 'Ey', 'Ez', 'dBdx', 'dBdy', 'dBdz').

    Notes
    -----
    Data are stored time channel by time channel, with one row per
    receiver. Unlike CSEM and AMT, TEM data are real-valued and
    are written without splitting into real and imaginary parts.
    """

    nt = len(times)
    nrx = len(rx_coords)

    with open(filename, 'w') as f:
        f.write("# TEM time-domain data\n\n")

        f.write(f"# COMPONENTS {' '.join(components)}\n\n")

        f.write(f"# TIMES_S {nt}\n")
        f.write(" ".join(f"{v:.8g}" for v in times) + "\n\n")

        f.write("# RECEIVERS\n# ID X Y Z\n")
        for i, xyz in enumerate(rx_coords):
            f.write(f"{i} " + " ".join(f"{v:.8g}" for v in xyz) + "\n")
        f.write("\n")

        f.write("# TEM DATA VALUES\n")
        f.write("# COLUMNS Rx_ID " + " ".join(components) + "\n")

        for jt in range(nt):
            f.write(f"\n#t{times[jt]:.8e}\n")
            for irx in range(nrx):
                row = [str(irx)]
                for z in DATA[jt][irx]:
                    row.append(f"{z:.8e}")
                f.write(" ".join(row) + "\n")