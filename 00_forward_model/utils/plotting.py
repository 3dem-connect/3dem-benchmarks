#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R / Skibbe.N
"""


"""
Helper functions to read EM resposnes to human-readable data-files
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as collections
from matplotlib.patches import Circle
from matplotlib.colors import Normalize, SymLogNorm, LogNorm


def init_fig_ax(components: list[str], fd: bool = True, figsize=(12, 12),
                **kwargs: object) -> tuple[plt.Figure, np.ndarray]:
    """Initialize line plot subplots for selected components."""

    nrows = 2
    ncols = len(components) if fd else len(components) // 2

    fig, ax = plt.subplots(nrows, ncols, squeeze=False, sharex=True,
                           figsize=figsize, **kwargs)

    for i in range(nrows):
        for j in range(ncols):
            component = components[j] if fd else components[i * ncols + j]
            title = f"{component} {['Real', 'Imag'][i]}" if fd else component
            ax[i, j].set_title(title)

    return fig, ax


def plot_line(pos: np.ndarray, field: np.ndarray, cmp: list[str],
              axis: int = 0, ax: np.ndarray | None = None, tag: str = '',
              fi: int = 0, freq: float = 0., **kwargs: object) -> np.ndarray:
    """Plot absolute real and imaginary electromagnetic field components."""

    indices = {'Ex': 0, 'Ey': 1, 'Ez': 2, 'Hx': 3, 'Hy': 4, 'Hz': 5,
               'Zxx': 0, 'Zxy': 1, 'Zyx': 2, 'Zyy': 3, 'Tx': 4, 'Ty': 5}
    units = {'E': 'V/m', 'H': 'A/m', 'Z': 'Ohm', 'T': ''}
    x = pos[:, axis]
    label = f'{tag}_F (Hz): {freq}'.strip()
    values = [[], []]

    for i, component in enumerate(cmp):
        data = field[fi, :, indices[component]]
        unit = units[component[0]]

        values[0].append(np.abs(data.real))
        values[1].append(np.abs(data.imag))

        ax[0, i].plot(x, values[0][-1], label=label, **kwargs)
        ax[1, i].plot(x, values[1][-1], **kwargs)
        ax[0, i].set_yscale('log')
        ax[1, i].set_yscale('log')
        ax[1, i].set_xlabel('Distance [m]')
        if i == 0:
            ax[0, i].set_ylabel(f'[{unit}]')
            ax[1, i].set_ylabel(f'[{unit}]')
            ax[0, i].legend()

    for row, vals in enumerate(values):
        limits = np.concatenate(vals)
        ax[row, 0].set_ylim(np.nanmin(limits), np.nanmax(limits))
        for axi in ax[row, :]:
            axi.set_ylim(ax[row, 0].get_ylim())

    return ax


def plot_line_td(pos: np.ndarray, field: np.ndarray, cmp: list[str],
                 axis: int = 0, ax: np.ndarray | None = None,
                 tag: str = '', ti: int = 0, time: float = 0.,
                 **kwargs: object) -> np.ndarray:
    """Plot transient electromagnetic field components along a profile."""

    indices = {'Ex': 0, 'Ey': 1, 'Ez': 2,
               'dBx': 3, 'dBy': 4, 'dBz': 5}

    units = {'E': 'mV/m', 'd': 'nT/s'}
    scaling = {'E': 1e3, 'd': 1e9}
    nlabel=10

    x = pos[:, axis]

    if ti % nlabel == 0:
        label = f'{tag}_T (s): {time:.2e}'
    else:
        label = '_nolegend_'
        kwargs.setdefault('color', 'k')
        kwargs.setdefault('linewidth', 0.5)
        kwargs.setdefault('linestyle', '-')
        kwargs['marker'] = None

    for i, component in enumerate(cmp):
        row = 0 if component.startswith('E') else 1
        col = i if row == 0 else i - 3

        data = field[ti, :, indices[component]] * scaling[component[0]]
        unit = units[component[0]]

        ax[row, col].plot(x, data, label=label, **kwargs)
        ax[row, col].set_xlabel('Distance [m]')
        ax[row, col].set_ylabel(f'[{unit}]')

        if i == 0:
            ax[row, col].legend()

    # Consistent y-axis limits within each row
    for row in range(2):
        limits = np.concatenate([line.get_ydata() for axi in ax[row, :]
                                for line in axi.lines])

        ymin, ymax = np.nanmin(limits), np.nanmax(limits)
        linthresh = np.nanmax(np.abs(limits)) * 1e-6

        for axi in ax[row, :]:
            axi.set_yscale('symlog', linthresh=linthresh)
            axi.set_ylim(ymin, ymax)

    return ax


def plot_line_misfit(pos: np.ndarray, field: np.ndarray, ref: np.ndarray,
                     cmp: list[str], axis: int = 0,
                     ax: np.ndarray | None = None, tag: str = '',
                     fi: int = 0, freq: float = 0., lim: float = 10.,
                     scale: str = 'linear', linthresh: float = 1.,
                     **kwargs: object) -> np.ndarray:
    """Plot percentage real and imaginary electromagnetic field misfits."""

    indices = {'Ex': 0, 'Ey': 1, 'Ez': 2, 'Hx': 3, 'Hy': 4, 'Hz': 5,
               'Zxx': 0, 'Zxy': 1, 'Zyx': 2, 'Zyy': 3, 'Tx': 4, 'Ty': 5}
    x = pos[:, axis]
    label = f'{tag}_F (Hz): {freq}'.strip()

    for i, component in enumerate(cmp):
        data = field[fi, :, indices[component]]
        reference = ref[fi, :, indices[component]]

        misfit_r = (data.real - reference.real) / reference.real * 100.
        misfit_i = (data.imag - reference.imag) / reference.imag * 100.

        ax[0, i].plot(x, misfit_r, label=label, **kwargs)
        ax[1, i].plot(x, misfit_i, **kwargs)
        if scale == 'lin':
            ax[0, i].set_yscale(scale)
            ax[1, i].set_yscale(scale)
        if scale == 'symlog':
            ax[0, i].set_yscale(scale, linthresh=linthresh)
            ax[1, i].set_yscale(scale, linthresh=linthresh)
        ax[0, i].set_ylim(-lim, lim)
        ax[1, i].set_ylim(-lim, lim)
        ax[1, i].set_xlabel('Distance [m]')
        if i == 0:
            ax[0, i].set_ylabel('Misfit [%]')
            ax[1, i].set_ylabel('Misfit [%]')
            ax[0, i].legend()

    return ax


def plot_line_misfit_td(pos: np.ndarray, field: np.ndarray, ref: np.ndarray,
                        cmp: list[str], axis: int = 0,
                        ax: np.ndarray | None = None, tag: str = '',
                        ti: int = 0, time: float = 0., lim: float = 10.,
                        nlabel: int = 10, **kwargs: object) -> np.ndarray:
    """Plot percentage transient electromagnetic field misfits along a profile."""

    indices = {'Ex': 0, 'Ey': 1, 'Ez': 2,
               'dBx': 3, 'dBy': 4, 'dBz': 5}

    units = {'E': 'mV/m', 'd': 'nT/s'}
    scaling = {'E': 1e3, 'd': 1e9}

    x = pos[:, axis]

    if ti % nlabel == 0:
        label = f'{tag}_T (s): {time:.2e}'
    else:
        label = '_nolegend_'
        kwargs.setdefault('color', 'k')
        kwargs.setdefault('linewidth', 0.5)
        kwargs.setdefault('linestyle', '-')
        kwargs['marker'] = None

    for i, component in enumerate(cmp):
        row = 0 if component.startswith('E') else 1
        col = i if row == 0 else i - 3

        data = field[ti, :, indices[component]] * scaling[component[0]]
        reference = ref[ti, :, indices[component]] * scaling[component[0]]

        # Percentage misfit
        misfit = (data - reference) / reference * 100.

        unit = units[component[0]]

        ax[row, col].plot(x, misfit, label=label, **kwargs)
        ax[row, col].set_xlabel('Distance [m]')
        ax[row, col].set_ylabel('Misfit [%]')
        ax[row, col].set_ylim(-lim, lim)

        if i == 0:
            ax[row, col].legend()

    # Consistent symlog scale within each row
    for row in range(2):
        limits = np.concatenate([
            line.get_ydata()
            for axi in ax[row, :]
            for line in axi.lines
        ])

        linthresh = np.nanmax(np.abs(limits)) * 1e-3

        for axi in ax[row, :]:
            axi.set_yscale('symlog', linthresh=linthresh)

    return ax


def plot_slice(pos: np.ndarray, field: np.ndarray, cmp: list[str],
               ax: np.ndarray, fi: int = 0, freq: float = 0.,
               r: float | None = None, clim: list[float] | None = None,
               scale: str = 'symlog',
               cmap: str = 'Spectral_r', cbar: object | None = None,
               **kwargs: object) -> tuple[np.ndarray, object]:
    """Plot real and imaginary electromagnetic field components."""

    indices = {'Ex': 0, 'Ey': 1, 'Ez': 2, 'Hx': 3, 'Hy': 4, 'Hz': 5}
    units = {'E': 'V/m', 'H': 'A/m'}
    data = np.column_stack([field[fi, :, indices[c]] for c in cmp])

    if r is None:
        r = np.linalg.norm(pos[0, :2] - pos[1, :2]) * 0.4

    patches = [Circle((x, y), r) for x, y in pos[:, :2]]

    if clim is None:
        clim = [np.nanmin(np.abs(data)), np.nanmax(np.abs(data))]

    if scale == 'symlog':
        linthresh = clim[0]
        norm = SymLogNorm(linthresh=linthresh, vmin=-clim[1],
                        vmax=clim[1])
    elif scale == 'log':
        norm = LogNorm(vmin=clim[0], vmax=clim[1])
    else:
        norm = Normalize(vmin=-clim[1], vmax=clim[1])

    for i, component in enumerate(cmp):
        unit = units[component[0]]
        cmap = 'magma' if component[0] == 'E' else 'viridis'
        for row, values in enumerate([data[:, i].real, data[:, i].imag]):
            pc = collections.PatchCollection(patches, cmap=cmap, norm=norm,
                                            linewidths=0, **kwargs)
            pc.set_array(values)
            ax[row, i].add_collection(pc)
            ax[row, i].set_aspect('equal')
            ax[row, i].set_ylabel(f'[{unit}]')

        pc.set_array(values)
        ax[row, i].add_collection(pc)
        ax[row, i].set_aspect('equal')
        ax[row, i].set_ylabel(f'[{unit}]')


    for axi in ax.flat:
        axi.set_xlim(pos[:, 0].min() - r, pos[:, 0].max() + r)
        axi.set_ylim(pos[:, 1].min() - r, pos[:, 1].max() + r)

    ax[0, 0].set_title(f'{cmp[0]} Real')
    ax[1, 0].set_title(f'{cmp[0]} Imag')

    cbar = ax[0, 0].figure.colorbar(
        pc, ax=ax.ravel().tolist(), orientation='horizontal',
        location='bottom', shrink=0.95, pad=0.08)

    return ax, cbar


def plot_slice_quiver(pos: np.ndarray, field: np.ndarray,
                      ax: np.ndarray, fi: int = 0, vlength: float = 1.,
                      freq: float = 0., clim: list[float] | None = None,
                      scale: str = 'symlog', tag: str = '',
                      **kwargs: object) -> np.ndarray:
    """Plot normalized E and H field directions with magnitude background."""

    x, y = pos[:, 0], pos[:, 1]
    labels = ['E Real', 'H Real', 'E Imag', 'H Imag']
    components = [(0, 1, 2), (3, 4, 5)]
    cmaps = ['magma', 'viridis']
    pcs = []

    for j, (ix, iy, iz) in enumerate(components):
        pc = None

        for row, part in enumerate([np.real, np.imag]):
            i = row * 2 + j
            data = field[fi]

            u = part(data[:, ix])
            v = part(data[:, iy])
            w = part(data[:, iz])

            magnitude = np.sqrt(u**2 + v**2 + w**2)
            direction = np.hypot(u, v)

            if clim is None:
                clim_j = [np.nanmin(magnitude), np.nanmax(magnitude)]
            else:
                clim_j = clim

            if scale == 'symlog':
                norm = SymLogNorm(linthresh=clim_j[0],
                                  vmin=0., vmax=clim_j[1])
            elif scale == 'log':
                norm = LogNorm(vmin=clim_j[0], vmax=clim_j[1])
            else:
                norm = Normalize(vmin=clim_j[0], vmax=clim_j[1])

            u_norm = np.divide(u, direction, out=np.zeros_like(u),
                               where=direction > 0)
            v_norm = np.divide(v, direction, out=np.zeros_like(v),
                               where=direction > 0)

            pc = ax[row, j].tripcolor(x, y, magnitude, shading='gouraud',
                                      cmap=cmaps[j], norm=norm)

            ax[row, j].quiver(x, y, u_norm * vlength, v_norm * vlength,
                              color='black', angles='xy',
                              scale_units='xy', scale=1., **kwargs)

            ax[row, j].set_title(labels[i])
            ax[row, j].set_aspect('equal')

        pcs.append(pc)

    ax[1, 0].set_xlabel('Distance [m]')
    ax[1, 1].set_xlabel('Distance [m]')

    for axi in ax.flat:
        axi.set_xlim(x.min(), x.max())
        axi.set_ylim(y.min(), y.max())

    fig = ax[0, 0].figure

    cbar_e = fig.colorbar(pcs[0], ax=ax[:, 0].tolist(),
                          orientation='horizontal', location='bottom',
                          shrink=0.9, pad=0.12)

    cbar_h = fig.colorbar(pcs[1], ax=ax[:, 1].tolist(),
                          orientation='horizontal', location='bottom',
                          shrink=0.9, pad=0.12)

    cbar_e.set_label(f'{tag} E magnitude [V/m]'.strip())
    cbar_h.set_label(f'{tag} H magnitude [A/m]'.strip())

    return ax


def plot_slice_quiver_misfit(pos: np.ndarray, field: np.ndarray,
                             ref: np.ndarray, ax: np.ndarray,
                             fi: int = 0, freq: float = 0.,
                             vlength: float = 1.,
                             clim: list[float] | None = None,
                             scale: str = 'symlog',
                             tag: str = '', **kwargs: object
                             ) -> np.ndarray:
    """Plot E and H magnitude and direction misfits."""

    x, y = pos[:, 0], pos[:, 1]
    labels = ['E Real', 'E Imag', 'H Real', 'H Imag']
    components = [(0, 1, 2), (3, 4, 5)]
    cmaps = ['RdBu_r', 'RdBu_r']
    pcs = []

    for j, (ix, iy, iz) in enumerate(components):
        for row, part in enumerate([np.real, np.imag]):
            i = 2 * j + row

            data = field[fi]
            reference = ref[fi]

            u, v, w = part(data[:, ix]), part(data[:, iy]), part(data[:, iz])
            ur = part(reference[:, ix])
            vr = part(reference[:, iy])
            wr = part(reference[:, iz])

            magnitude = np.sqrt(u**2 + v**2 + w**2)
            magnitude_ref = np.sqrt(ur**2 + vr**2 + wr**2)

            misfit = 100. * (magnitude - magnitude_ref) / magnitude_ref
            direction = np.hypot(u, v)
            direction_ref = np.hypot(ur, vr)

            dot = u * ur + v * vr
            cross = u * vr - v * ur

            angle = np.degrees(np.arctan2(cross, dot))

            if clim is None:
                clim = [np.nanmin(np.abs(misfit)),
                        np.nanmax(np.abs(misfit))]

            if scale == 'symlog':
                norm = SymLogNorm(linthresh=clim[0], vmin=-clim[1],
                                  vmax=clim[1])
            elif scale == 'log':
                norm = LogNorm(vmin=clim[0], vmax=clim[1])
            else:
                norm = Normalize(vmin=-clim[1], vmax=clim[1])

            pc = ax.flat[i].tripcolor(x, y, misfit, shading='gouraud',
                                      cmap=cmaps[j], norm=norm)

            ax.flat[i].quiver(x, y, ur / np.maximum(direction_ref, 1e-30),
                              vr / np.maximum(direction_ref, 1e-30),
                              color='black', angles='xy',
                              scale_units='xy', scale=1., **kwargs)

            ax.flat[i].set_title(labels[i])
            ax.flat[i].set_aspect('equal')
            pcs.append(pc)

    ax[1, 0].set_xlabel('Distance [m]')
    ax[1, 1].set_xlabel('Distance [m]')

    for axi in ax.flat:
        axi.set_xlim(x.min(), x.max())
        axi.set_ylim(y.min(), y.max())

    fig = ax[0, 0].figure

    cbar_e = fig.colorbar(pcs[0], ax=ax[:, 0].tolist(),
                          orientation='horizontal', location='bottom',
                          shrink=0.9, pad=0.12)
    cbar_h = fig.colorbar(pcs[2], ax=ax[:, 1].tolist(),
                          orientation='horizontal', location='bottom',
                          shrink=0.9, pad=0.12)

    cbar_e.set_label(f'{tag} E magnitude misfit [%]'.strip())
    cbar_h.set_label(f'{tag} H magnitude misfit [%]'.strip())

    return ax
