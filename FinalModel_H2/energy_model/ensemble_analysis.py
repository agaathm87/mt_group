"""Analyses of the scenario ensemble (the slide: GSA, scatter plots, scenario discovery, multi-objective
trade-offs, robustness, vulnerability, adaptive pathways/tipping points, clustering).

All functions take the ensemble table from ensemble.load_ensemble(): one row per future x policy,
with the uncertainties (inputs), 'policy' (S1/S2/S3), 'scenario' (future id) and the outcomes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from .ensemble import UNCERTAINTIES, POLICIES
from .h2_plots import SCEN_COLORS, INK, INK2, MUTED, GRID, _style

BLUES = LinearSegmentedColormap.from_list(
    'blues', ['#f4f8fe', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#2a78d6', '#1c5cab', '#104281', '#0d366b'])
LABELS = {
    'green_share_2050': 'Green share 2050 (%)', 'green_share_2040': 'Green share 2040 (%)',
    'green_twh_2050': 'Green H$_2$ 2050 (TWh)', 'blue_twh_2050': 'Blue H$_2$ 2050 (TWh)',
    'grey_twh_2050': 'Grey H$_2$ 2050 (TWh)', 'system_cost_bn': 'System cost (bn €, discounted)',
    'cum_co2_mt': 'Cumulative CO$_2$ (Mt)', 'co2_2050': 'CO$_2$ 2050 (Mt/yr)', 'water_2050': 'Water 2050 (Mm$^3$/yr)',
    'h2_price_2050': 'H$_2$ price 2050 (€/kg)', 'lcoh_green_2050': 'Green LCOH 2050 (€/kg)',
    'ely_gw_2050': 'Electrolysers 2050 (GW)', 'ely_flh_2050': 'Electrolyser hours 2050 (h)',
    'gas_2050': 'Gas use 2050 (TWh)', 'electricity_price_2050': 'Electricity price 2050 (€/MWh)',
    'cost_regret_bn': 'Cost regret (bn €)', 'co2_regret_mt': 'CO$_2$ regret (Mt)',
}
INPUTS = list(UNCERTAINTIES)


def label(c):
    return LABELS.get(c, c)


# --------------------------------------------------------------------------
# Global sensitivity analysis: extra-trees feature scoring (Jaxa-Rozen & Kwakkel, 2018)
# --------------------------------------------------------------------------

def feature_scores(df, outcomes, policy=None):
    """Feature scores (share of explained variation, sums to 1 per outcome) of each input for each outcome."""
    from ema_workbench.analysis import feature_scoring
    d = df if policy is None else df[df.policy == policy]
    x = d[INPUTS].copy()
    if policy is None:
        x['policy'] = d['policy'].astype('category')
    y = {o: d[o].fillna(d[o].median()).values for o in outcomes}
    return feature_scoring.get_feature_scores_all(x, y)


def plot_feature_scores(scores, ax=None, title='Global sensitivity analysis (extra-trees feature scores)'):
    if ax is None:
        fig, ax = plt.subplots(figsize=(1.2 + 0.9 * scores.shape[1], 0.35 * scores.shape[0] + 1.2))
    im = ax.imshow(scores.values, cmap=BLUES, aspect='auto', vmin=0, vmax=max(0.5, scores.values.max()))
    ax.set_xticks(range(scores.shape[1]), [label(c) for c in scores.columns], rotation=35, ha='right', fontsize=7.5)
    ax.set_yticks(range(scores.shape[0]), scores.index, fontsize=8)
    for i in range(scores.shape[0]):
        for j in range(scores.shape[1]):
            v = scores.values[i, j]
            ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=7,
                    color='white' if v > 0.3 else INK)
    ax.set_title(title, loc='left')
    plt.colorbar(im, ax=ax, fraction=0.03, label='influence (0-1)')
    for s in ax.spines.values():
        s.set_visible(False)
    return ax


# --------------------------------------------------------------------------
# Scatter plots
# --------------------------------------------------------------------------

def plot_pairs(df, outcomes, policies=POLICIES, size=2.2):
    """Scatter matrix of outcomes, coloured by policy (S1/S2/S3)."""
    k = len(outcomes)
    fig, axes = plt.subplots(k, k, figsize=(size * k, size * k))
    for i, oy in enumerate(outcomes):
        for j, ox in enumerate(outcomes):
            ax = axes[i, j]
            if i == j:
                for p in policies:
                    v = df.loc[df.policy == p, ox].dropna()
                    ax.hist(v, bins=20, color=SCEN_COLORS[p], alpha=0.55, histtype='stepfilled')
            else:
                for p in policies:
                    d = df[df.policy == p]
                    ax.scatter(d[ox], d[oy], s=9, color=SCEN_COLORS[p], alpha=0.75, linewidths=0, label=p)
            if i == k - 1:
                ax.set_xlabel(label(ox), fontsize=7)
            if j == 0:
                ax.set_ylabel(label(oy), fontsize=7)
            ax.tick_params(labelsize=6.5)
            ax.spines[['top', 'right']].set_visible(False)
    axes[0, 1].legend(title='Scenario', fontsize=7, loc='upper right')
    fig.suptitle('Scatter plot analyses: outcomes of all futures, per scenario', x=0.01, ha='left',
                 fontweight='bold', fontsize=10)
    fig.tight_layout()
    return fig


def plot_driver_scatter(df, outcome, drivers, policies=POLICIES):
    """Outcome against its main drivers, coloured by policy."""
    fig, axes = plt.subplots(1, len(drivers), figsize=(4.2 * len(drivers), 3.2), sharey=True)
    axes = np.atleast_1d(axes)
    for ax, x in zip(axes, drivers):
        for p in policies:
            d = df[df.policy == p]
            ax.scatter(d[x], d[outcome], s=12, color=SCEN_COLORS[p], alpha=0.8, linewidths=0, label=p)
        ax.set_xlabel(x)
        _style(ax)
    axes[0].set_ylabel(label(outcome))
    axes[0].legend(title='Scenario', fontsize=7)
    fig.suptitle(f'{label(outcome)} against its main drivers', x=0.01, ha='left', fontweight='bold', fontsize=10)
    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------
# Scenario discovery and vulnerability: PRIM (Bryant & Lempert, 2010)
# --------------------------------------------------------------------------

def run_prim(df, condition, policy=None, threshold=0.8, inputs=INPUTS):
    """PRIM on the rows of `policy` (or all rows); condition is a boolean Series (cases of interest)."""
    from ema_workbench.analysis import prim
    d = df if policy is None else df[df.policy == policy]
    y = condition.loc[d.index].values.astype(bool)
    p = prim.Prim(d[[c for c in inputs if c != 'dummy']].reset_index(drop=True), y, threshold=threshold)
    box = p.find_box()
    return p, box, y


def plot_prim(box, y, title, choose=None):
    """Two panels: the peeling trade-off (coverage vs density) and the limits of the chosen box."""
    traj = box.peeling_trajectory
    if choose is not None:
        i = choose
    else:   # densest box that still covers at least half of the cases (ties: the larger coverage)
        cand = traj[traj['coverage'] >= 0.5]
        cand = cand[cand['density'] >= cand['density'].max() - 1e-9]
        i = int(cand['coverage'].idxmax())
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={'width_ratios': [1, 1.4]})
    sc = axes[0].scatter(traj['coverage'], traj['density'], c=traj['res_dim'], cmap=BLUES, s=22,
                         edgecolors=MUTED, linewidths=0.4)
    axes[0].scatter([traj.at[i, 'coverage']], [traj.at[i, 'density']], s=90, facecolors='none',
                    edgecolors='#eb6834', linewidths=2, label=f'chosen box ({i})')
    plt.colorbar(sc, ax=axes[0], label='restricted inputs')
    axes[0].set_xlabel('Coverage (share of all cases of interest inside the box)')
    axes[0].set_ylabel('Density (share of the box that are cases)')
    axes[0].set_title('PRIM trade-off', loc='left')
    axes[0].legend(fontsize=7)
    _style(axes[0])
    box.select(i)
    lims = box.box_lims[i]
    init = box.prim.box_init
    rows = [c for c in lims.columns if not np.isclose(lims.at[0, c], init.at[0, c])
            or not np.isclose(lims.at[1, c], init.at[1, c])]
    ax = axes[1]
    for k, c in enumerate(rows):
        lo, hi = UNCERTAINTIES[c][:2]
        a, b = (lims.at[0, c] - lo) / (hi - lo), (lims.at[1, c] - lo) / (hi - lo)
        ax.barh(k, 1, left=0, color=GRID, height=0.5)
        ax.barh(k, b - a, left=a, color='#2a78d6', height=0.5)
        fmt = (lambda v: f'{v:.0f}') if hi >= 10 else (lambda v: f'{v:.2f}')   # no scientific notation
        ax.text(a, k + 0.33, fmt(lims.at[0, c]), ha='center', fontsize=7, color=INK2)
        ax.text(b, k + 0.33, fmt(lims.at[1, c]), ha='center', fontsize=7, color=INK2)
    ax.set_yticks(range(len(rows)), rows)
    ax.set_xlim(-0.05, 1.05)
    ax.set_xticks([0, 1], ['low end of range', 'high end of range'])
    ax.invert_yaxis()
    ax.set_title(f'{title}\ncoverage {traj.at[i, "coverage"]:.0%}, density {traj.at[i, "density"]:.0%}, '
                 f'{int(y.sum())} of {len(y)} cases', loc='left', fontsize=9)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    return fig, lims[rows]


# --------------------------------------------------------------------------
# Multi-objective trade-offs: parallel coordinates
# --------------------------------------------------------------------------

def plot_parcoords(df, outcomes, better=None, policies=POLICIES, title='Trade-offs across all futures'):
    """Parallel coordinates; each line is one future under one scenario. better[o] = 'low' or 'high'."""
    better = better or {}
    d = df[outcomes + ['policy']].dropna()
    lo, hi = d[outcomes].min(), d[outcomes].max()
    z = (d[outcomes] - lo) / (hi - lo).replace(0, 1)
    for o in outcomes:                    # 'better' is drawn at the bottom for every axis
        if better.get(o, 'low') == 'high':
            z[o] = 1 - z[o]
    fig, ax = plt.subplots(figsize=(1.6 * len(outcomes) + 1, 4.2))
    xs = np.arange(len(outcomes))
    for p in policies:
        zz = z[d.policy == p]
        for _, r in zz.iterrows():
            ax.plot(xs, r.values, color=SCEN_COLORS[p], alpha=0.25, lw=0.8)
        ax.plot([], [], color=SCEN_COLORS[p], lw=2, label=p)
    for i, o in enumerate(outcomes):
        ax.axvline(i, color=MUTED, lw=1)
        top, bot = (lo[o], hi[o]) if better.get(o, 'low') == 'high' else (hi[o], lo[o])
        fmt = lambda v: f'{v:,.0f}' if abs(v) >= 100 else f'{v:.2f}'
        ax.text(i, 1.03, fmt(top), ha='center', fontsize=7, color=INK2)
        ax.text(i, -0.07, fmt(bot), ha='center', fontsize=7, color=INK2)
    ax.set_xticks(xs, [label(o) for o in outcomes], fontsize=7.5)
    ax.set_yticks([0, 1], ['better', 'worse'])
    ax.set_ylim(-0.12, 1.1)
    ax.set_title(title, loc='left')
    ax.legend(title='Scenario', fontsize=7, loc='upper left', bbox_to_anchor=(1, 1))
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------
# Robustness: regret and satisficing (McPhail et al., 2018)
# --------------------------------------------------------------------------

def add_regret(df):
    """Regret per future: outcome minus the best outcome of any scenario in the SAME future."""
    d = df.copy()
    d['cost_regret_bn'] = d['system_cost_bn'] - d.groupby('scenario')['system_cost_bn'].transform('min')
    d['co2_regret_mt'] = d['cum_co2_mt'] - d.groupby('scenario')['cum_co2_mt'].transform('min')
    return d


def robustness_table(df, cost_tol_bn=10.0, co2_cap=None):
    """Robustness metrics per scenario: mean, 90th percentile and maximum regret, and a satisficing share."""
    d = add_regret(df)
    rows = {}
    for p in POLICIES:
        s = d[d.policy == p]
        ok = s['cost_regret_bn'] <= cost_tol_bn
        if co2_cap is not None:
            ok &= s['cum_co2_mt'] <= co2_cap
        rows[p] = {
            'mean cost regret (bn €)': s['cost_regret_bn'].mean(),
            '90th pct cost regret (bn €)': s['cost_regret_bn'].quantile(0.9),
            'max cost regret (bn €)': s['cost_regret_bn'].max(),
            'mean cumulative CO2 (Mt)': s['cum_co2_mt'].mean(),
            '90th pct cumulative CO2 (Mt)': s['cum_co2_mt'].quantile(0.9),
            'mean water 2050 (Mm3/yr)': s['water_2050'].mean(),
            'satisficing share (%)': 100 * ok.mean(),
        }
    return pd.DataFrame(rows)


def plot_robustness(df, outcomes=('cost_regret_bn', 'co2_regret_mt', 'green_share_2050', 'water_2050')):
    """Box plots per scenario across all futures."""
    d = add_regret(df)
    fig, axes = plt.subplots(1, len(outcomes), figsize=(3.3 * len(outcomes), 3.4))
    for ax, o in zip(axes, outcomes):
        data = [d.loc[d.policy == p, o].dropna().values for p in POLICIES]
        bp = ax.boxplot(data, patch_artist=True, widths=0.55, medianprops=dict(color=INK, lw=1.5),
                        whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
                        flierprops=dict(marker='o', ms=3, markerfacecolor=MUTED, markeredgecolor='none'))
        for patch, p in zip(bp['boxes'], POLICIES):
            patch.set_facecolor(SCEN_COLORS[p])
            patch.set_alpha(0.85)
            patch.set_edgecolor('white')
        ax.set_xticks(range(1, len(POLICIES) + 1), POLICIES)
        ax.set_title(label(o), loc='left', fontsize=9)
        _style(ax)
    fig.suptitle('Robustness across all futures (regret = difference with the best scenario in the same future)',
                 x=0.01, ha='left', fontweight='bold', fontsize=10)
    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------
# Adaptive pathways: tipping points (when does the water limit start to matter?)
# --------------------------------------------------------------------------

def plot_tipping_map(df, x='co2_index', y='ely_capex_index', z='green_share_2050', policy='S1', threshold=50.0,
                     title=None):
    """Futures of one scenario on two inputs, coloured by an outcome; ringed = outcome above threshold.
    For S1 (Base, no limit) and z = green share: the futures in which electrolysis is cost-optimal for more than half
    of the hydrogen, i.e. where a water limit (S2, S3) takes away the most."""
    d = df[df.policy == policy]
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    sc = ax.scatter(d[x], d[y], c=d[z], cmap=BLUES, s=34, edgecolors='none')
    over = d[d[z] > threshold]
    ax.scatter(over[x], over[y], s=60, facecolors='none', edgecolors='#eb6834', linewidths=1.2,
               label=f'{label(z)} > {threshold:g}')
    plt.colorbar(sc, ax=ax, label=label(z))
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title or f'Tipping points in {policy}: where would a water limit bind?', loc='left', fontsize=9.5)
    ax.legend(fontsize=7, loc='upper left', bbox_to_anchor=(0, -0.15))
    _style(ax, ygrid=False)
    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------
# Clustering: archetypes of hydrogen systems
# --------------------------------------------------------------------------

def cluster_outcomes(df, outcomes, k=4, seed=1):
    """k-means on standardised outcomes; returns the table with a 'cluster' column and cluster profiles."""
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    d = df.dropna(subset=outcomes).copy()
    z = StandardScaler().fit_transform(d[outcomes])
    d['cluster'] = KMeans(n_clusters=k, n_init=20, random_state=seed).fit_predict(z)
    order = d.groupby('cluster')[outcomes[0]].mean().sort_values().index
    d['cluster'] = d['cluster'].map({c: i + 1 for i, c in enumerate(order)})
    prof_out = d.groupby('cluster')[outcomes].mean()
    prof_in = d.groupby('cluster')[[c for c in INPUTS if c != 'dummy']].mean()
    prof_pol = pd.crosstab(d['cluster'], d['policy'], normalize='index') * 100
    return d, prof_out, prof_in, prof_pol


def plot_clusters(d, x='green_share_2050', y='system_cost_bn'):
    from .h2_plots import CATEGORICAL
    fig, ax = plt.subplots(figsize=(5.8, 4))
    for c in sorted(d.cluster.unique()):
        dd = d[d.cluster == c]
        ax.scatter(dd[x], dd[y], s=14, color=CATEGORICAL[(c - 1) % 8], alpha=0.85, linewidths=0,
                   label=f'cluster {c} (n={len(dd)})')
    ax.set_xlabel(label(x))
    ax.set_ylabel(label(y))
    ax.set_title('Clusters of futures (k-means on the outcomes)', loc='left')
    ax.legend(fontsize=7)
    _style(ax)
    fig.tight_layout()
    return fig
