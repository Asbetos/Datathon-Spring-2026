"""Causal inference utilities for food waste policy analysis."""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.optimize import minimize


def load_policy_timeline(path='data/policy_timeline.csv'):
    return pd.read_csv(path)


def build_state_year_panel(state_parquet='outputs/analysis/cleaned_data/state_summary.parquet',
                           policy_path='data/policy_timeline.csv'):
    state_df = pd.read_parquet(state_parquet)
    policy = pd.read_csv(policy_path)

    state_year = state_df.groupby(['state', 'year']).agg(
        tons_surplus=('tons_surplus', 'sum'),
        tons_waste=('tons_waste', 'sum'),
        tons_landfill=('tons_landfill', 'sum'),
        tons_composting=('tons_composting', 'sum'),
        tons_donations=('tons_donations', 'sum'),
        tons_anaerobic_digestion=('tons_anaerobic_digestion', 'sum'),
        tons_animal_feed=('tons_animal_feed', 'sum'),
        us_dollars_surplus=('us_dollars_surplus', 'sum'),
        co2e=('surplus_total_100_year_mtco2e_footprint', 'sum'),
        water=('gallons_water_footprint', 'sum'),
        meals_wasted=('meals_wasted', 'sum')
    ).reset_index()

    state_year['landfill_rate'] = state_year['tons_landfill'] / state_year['tons_waste']
    state_year['diversion_rate'] = (
        state_year['tons_composting'] + state_year['tons_donations'] +
        state_year['tons_anaerobic_digestion'] + state_year['tons_animal_feed']
    ) / state_year['tons_waste']

    state_year = state_year.merge(policy[['state', 'ban_year']], on='state', how='left')
    state_year['ban_year'] = state_year['ban_year'].fillna(9999).astype(int)
    state_year['ban_active'] = (state_year['year'] >= state_year['ban_year']).astype(int)
    state_year['is_ban_state'] = state_year['state'].isin(policy['state'].values)

    return state_year, policy


def run_twfe_did(state_year, outcomes=None):
    if outcomes is None:
        outcomes = {'landfill_rate': 'Landfill rate', 'diversion_rate': 'Diversion rate',
                    'tons_landfill': 'Tons to landfill'}

    state_dummies = pd.get_dummies(state_year['state'], prefix='st', drop_first=True).astype(float)
    year_dummies = pd.get_dummies(state_year['year'], prefix='yr', drop_first=True).astype(float)
    X = pd.concat([state_year[['ban_active']].astype(float), state_dummies, year_dummies], axis=1)
    X = sm.add_constant(X)

    results = {}
    for outcome, label in outcomes.items():
        y = state_year[outcome].values.astype(float)
        model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': state_year['state']})
        results[outcome] = {
            'beta': float(model.params['ban_active']),
            'se': float(model.bse['ban_active']),
            'tstat': float(model.tvalues['ban_active']),
            'pvalue': float(model.pvalues['ban_active']),
            'ci_lower': float(model.conf_int().loc['ban_active', 0]),
            'ci_upper': float(model.conf_int().loc['ban_active', 1]),
            'r_squared': float(model.rsquared),
            'n_obs': int(model.nobs),
            'label': label
        }
    return results


def run_event_study(state_year, outcome='landfill_rate', window=(-5, 8)):
    ban_states_df = state_year[state_year['is_ban_state']].copy()
    ban_states_df['event_time'] = ban_states_df['year'] - ban_states_df['ban_year']
    control_df = state_year[~state_year['is_ban_state']].copy()
    control_df['event_time'] = -999
    combined = pd.concat([ban_states_df, control_df])

    event_window = list(range(window[0], window[1] + 1))
    for t in event_window:
        if t == -1:
            continue
        combined[f'et_{t}'] = (combined['event_time'] == t).astype(float)

    et_cols = [f'et_{t}' for t in event_window if t != -1]
    state_dummies = pd.get_dummies(combined['state'], prefix='st', drop_first=True).astype(float)
    year_dummies = pd.get_dummies(combined['year'], prefix='yr', drop_first=True).astype(float)
    X = pd.concat([combined[et_cols], state_dummies, year_dummies], axis=1)
    X = sm.add_constant(X)
    y = combined[outcome].values.astype(float)
    model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': combined['state']})

    results = []
    for t in event_window:
        if t == -1:
            results.append({'event_time': t, 'coef': 0, 'se': 0, 'ci_lo': 0, 'ci_hi': 0})
        else:
            col = f'et_{t}'
            results.append({
                'event_time': t,
                'coef': float(model.params[col]),
                'se': float(model.bse[col]),
                'ci_lo': float(model.conf_int().loc[col, 0]),
                'ci_hi': float(model.conf_int().loc[col, 1])
            })
    return results


def run_synthetic_control(state_year, target_state, treatment_year, policy):
    target_ts = state_year[state_year['state'] == target_state].set_index('year')['landfill_rate']
    non_ban = [s for s in state_year['state'].unique() if s not in policy['state'].values]
    all_years = sorted(state_year['year'].unique())
    pre_years = [y for y in all_years if y < treatment_year]

    donors = {}
    for s in non_ban:
        ts = state_year[state_year['state'] == s].set_index('year')['landfill_rate']
        if len(ts) == len(all_years):
            donors[s] = ts

    donor_names = list(donors.keys())
    donor_pre = np.array([donors[s].loc[pre_years].values for s in donor_names])
    target_pre = target_ts.loc[pre_years].values

    n = len(donor_names)
    result = minimize(lambda w: np.sum((target_pre - w @ donor_pre) ** 2),
                      np.ones(n) / n, bounds=[(0, 1)] * n,
                      constraints=[{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}])
    w = result.x

    donor_all = np.array([donors[s].loc[all_years].values for s in donor_names])
    synthetic = w @ donor_all

    return {
        'actual': target_ts.loc[all_years].values,
        'synthetic': synthetic,
        'years': all_years,
        'weights': dict(zip(donor_names, w.tolist())),
        'treatment_year': treatment_year
    }
