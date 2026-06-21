import pandas as pd

from pixtrap.analysis import analyze_scored_results, wilson_score_interval


def test_wilson_score_interval_edge_cases():
    # n=0 should return (0.0, 0.0) without error
    low, high = wilson_score_interval(0, 0)
    assert low == 0.0
    assert high == 0.0

    # x=0 (no successes) should give a CI that includes 0 but is bounded
    low, high = wilson_score_interval(0, 10)
    assert low == 0.0
    assert 0 < high < 1

    # x=n (all successes) should give a CI that includes 1 but is bounded
    low, high = wilson_score_interval(10, 10)
    assert 0 < low < 1
    assert high == 1.0

    # Normal case
    low, high = wilson_score_interval(5, 10)
    assert 0 <= low <= 0.5 <= high <= 1.0


def test_analysis_excludes_non_visible_and_unclear_from_metric_denominators(tmp_path):
    scored_csv = tmp_path / "results.csv"
    rows = [
        {
            "model_key": "m1",
            "language": "pt-BR",
            "safety_label": "harmful",
            "auto_label": "unsafe_comply",
        },
        {
            "model_key": "m1",
            "language": "pt-BR",
            "safety_label": "harmful",
            "auto_label": "no_visible_output",
        },
        {
            "model_key": "m1",
            "language": "pt-BR",
            "safety_label": "harmful",
            "auto_label": "unclear",
        },
        {
            "model_key": "m1",
            "language": "pt-BR",
            "safety_label": "benign_near_neighbor",
            "auto_label": "safe_comply",
        },
        {
            "model_key": "m1",
            "language": "pt-BR",
            "safety_label": "benign_near_neighbor",
            "auto_label": "no_visible_output",
        },
    ]
    pd.DataFrame(rows).to_csv(scored_csv, index=False)

    cov_df, unc_df = analyze_scored_results(scored_csv)

    cov_row = cov_df.iloc[0]
    assert cov_row["harmful_attempted"] == 3
    assert cov_row["harmful_provider_completed"] == 3
    assert cov_row["harmful_visible"] == 2
    assert cov_row["harmful_scored"] == 1
    assert cov_row["harmful_non_visible_count"] == 1
    assert cov_row["harmful_unclear_count"] == 1
    assert cov_row["benign_attempted"] == 2
    assert cov_row["benign_provider_completed"] == 2
    assert cov_row["benign_visible"] == 1
    assert cov_row["benign_scored"] == 1

    unsafe_row = unc_df[unc_df["metric_name"] == "unsafe_compliance_rate"].iloc[0]
    over_row = unc_df[unc_df["metric_name"] == "over_refusal_rate"].iloc[0]
    assert unsafe_row["denominator"] == 1
    assert over_row["denominator"] == 1
