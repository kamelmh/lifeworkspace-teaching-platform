#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taallim pilot — automated §4 analysis
=====================================

Ingests the pilot dataset and produces the Results (§4) tables.
OUTCOME = English GRAMMAR scores (pretest / posttest / delayed). RQ mapping:
  §4.1  Descriptive statistics + assumption checks + baseline equivalence
  §4.2  RQ2 — ANCOVA on the immediate GRAMMAR post-test (covariate = pretest) + adjusted means
  §4.3  RQ2 — 2x3 mixed ANOVA (Condition x Time): GRAMMAR retention
  §4.4  Exploratory — usage->gain correlations + regression (experimental group)
  §4.5  RQ3 — TEACHER-questionnaire descriptives (+ Cronbach alpha if item-level data)

Outputs: one CSV per table in ./outputs/ plus a combined results_tables.md
that drops straight into the manuscript's §4.

--------------------------------------------------------------------------
EXPECTED INPUT  (wide, one row per student).  Use --make-sample to generate a
template you can open in Excel and overwrite with real data.

  student_id            e.g. S001
  group                 "Experimental" | "Control"
  pretest               0-20
  posttest              0-20
  delayed               0-20      (delayed post-test)
  cards_reviewed        int       ] usage metrics
  review_regularity     0-1       ] (Experimental group only;
  mcq_accuracy          0-1       ]  leave blank for Control)
  maps_completed        int       ]
  time_on_task_min      minutes   ]
  usability             1-5       ] questionnaire subscale means
  engagement            1-5       ] (Experimental group only)
  usefulness            1-5       ]
  bilingual_design      1-5       ]

Run:
  python3 taallim_analysis.py --make-sample          # write sample_pilot_data.csv
  python3 taallim_analysis.py                         # run on the sample
  python3 taallim_analysis.py --input my_pilot.csv    # run on real data
--------------------------------------------------------------------------
"""

import argparse
import os
import sys
import textwrap
import numpy as np
import pandas as pd

try:
    import pingouin as pg
except ImportError:
    sys.exit("pingouin is required:  pip install pingouin")
import statsmodels.formula.api as smf
import statsmodels.api as sm

GROUPS = ["Experimental", "Control"]
TIMES = ["pretest", "posttest", "delayed"]
USAGE = ["cards_reviewed", "review_regularity", "mcq_accuracy",
         "maps_completed", "time_on_task_min"]
SUBSCALES = ["usability", "engagement", "usefulness", "bilingual_design"]


# --------------------------------------------------------------------------- #
# Sample-data generator (also documents the required schema)
# --------------------------------------------------------------------------- #
def make_sample(path="sample_pilot_data.csv", n_per_group=60, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_per_group * 2):
        grp = "Experimental" if i < n_per_group else "Control"
        pre = float(np.clip(rng.normal(9.5, 2.3), 0, 20))
        # experimental group gets a boost + better retention; usage drives gain
        if grp == "Experimental":
            usage_quality = rng.uniform(0.3, 1.0)          # latent engagement
            post = np.clip(pre + rng.normal(3.2, 1.4) + 2.0 * usage_quality, 0, 20)
            delayed = np.clip(post - rng.normal(0.8, 0.9), 0, 20)
            row = dict(
                cards_reviewed=int(rng.normal(180, 45) * usage_quality + 40),
                review_regularity=round(float(np.clip(usage_quality + rng.normal(0, .08), 0, 1)), 3),
                mcq_accuracy=round(float(np.clip(rng.normal(0.72, 0.1) + 0.1 * usage_quality, 0, 1)), 3),
                maps_completed=int(np.clip(rng.normal(8, 3) * usage_quality + 1, 0, 30)),
                time_on_task_min=int(np.clip(rng.normal(320, 80) * usage_quality + 60, 0, 900)),
                usability=round(float(np.clip(rng.normal(4.1, 0.5), 1, 5)), 2),
                engagement=round(float(np.clip(rng.normal(4.0, 0.6), 1, 5)), 2),
                usefulness=round(float(np.clip(rng.normal(4.2, 0.5), 1, 5)), 2),
                bilingual_design=round(float(np.clip(rng.normal(4.4, 0.5), 1, 5)), 2),
            )
        else:
            post = np.clip(pre + rng.normal(1.4, 1.3), 0, 20)
            delayed = np.clip(post - rng.normal(1.6, 1.0), 0, 20)
            row = {k: np.nan for k in USAGE + SUBSCALES}
        row.update(student_id=f"S{i+1:03d}", group=grp,
                   pretest=round(pre, 2), posttest=round(float(post), 2),
                   delayed=round(float(delayed), 2))
        rows.append(row)
    cols = ["student_id", "group"] + TIMES + USAGE + SUBSCALES
    df = pd.DataFrame(rows)[cols]
    df.to_csv(path, index=False)
    print(f"[+] wrote sample dataset -> {path}  ({len(df)} rows)")
    return path


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _round(df, n=3):
    return df.round(n)


def load(path):
    df = pd.read_csv(path)
    missing = [c for c in ["student_id", "group"] + TIMES if c not in df.columns]
    if missing:
        sys.exit(f"Input is missing required columns: {missing}")
    df["group"] = pd.Categorical(df["group"], categories=GROUPS)
    return df


# --------------------------------------------------------------------------- #
# §4.1 Descriptives + assumptions
# --------------------------------------------------------------------------- #
def descriptives(df):
    d = (df.melt(id_vars=["group"], value_vars=TIMES, var_name="measure", value_name="score")
           .groupby(["measure", "group"], observed=True)["score"]
           .agg(n="count", M="mean", SD="std").reset_index())
    d["measure"] = pd.Categorical(d["measure"], categories=TIMES, ordered=True)
    return _round(d.sort_values(["measure", "group"]))


def assumptions(df):
    out = []
    # normality of posttest by group
    norm = pg.normality(df, dv="posttest", group="group")
    for grp, r in norm.iterrows():
        out.append(dict(check=f"Normality (posttest) – {grp}",
                        stat=round(r["W"], 3), p=round(r["pval"], 3),
                        met=bool(r["normal"])))
    # homogeneity of variance
    lev = pg.homoscedasticity(df, dv="posttest", group="group")
    out.append(dict(check="Homogeneity of variance (Levene)",
                    stat=round(float(lev["W"].iloc[0]), 3),
                    p=round(float(lev["pval"].iloc[0]), 3),
                    met=bool(lev["equal_var"].iloc[0])))
    # homogeneity of regression slopes (group x pretest interaction F-test)
    m = smf.ols("posttest ~ C(group) * pretest", data=df).fit()
    at = sm.stats.anova_lm(m, typ=2)
    irow = at.loc["C(group):pretest"]
    inter_F, inter_p = float(irow["F"]), float(irow["PR(>F)"])
    out.append(dict(check="Homogeneity of regression slopes (group x pretest)",
                    stat=round(inter_F, 3), p=round(inter_p, 3),
                    met=bool(inter_p > .05)))
    return pd.DataFrame(out)


def baseline(df):
    a = df.loc[df.group == "Experimental", "pretest"].dropna()
    b = df.loc[df.group == "Control", "pretest"].dropna()
    t = pg.ttest(a, b, paired=False)
    return dict(t=round(float(t["T"].iloc[0]), 3), dof=int(t["dof"].iloc[0]),
                p=round(float(t["p-val"].iloc[0]), 3),
                d=round(float(t["cohen-d"].iloc[0]), 3),
                equivalent=bool(t["p-val"].iloc[0] > .05))


# --------------------------------------------------------------------------- #
# §4.2 ANCOVA + adjusted means
# --------------------------------------------------------------------------- #
def ancova_table(df):
    aov = pg.ancova(data=df, dv="posttest", covar="pretest", between="group")
    return _round(aov)


def adjusted_means(df):
    m = smf.ols("posttest ~ C(group) + pretest", data=df).fit()
    grand_pre = df["pretest"].mean()
    pred = pd.DataFrame({"group": GROUPS, "pretest": grand_pre})
    sf = m.get_prediction(pred).summary_frame(alpha=0.05)
    out = pd.DataFrame({
        "group": GROUPS,
        "adjusted_M": sf["mean"].round(3),
        "SE": sf["mean_se"].round(3),
        "CI_low": sf["mean_ci_lower"].round(3),
        "CI_high": sf["mean_ci_upper"].round(3),
    })
    return out


# --------------------------------------------------------------------------- #
# §4.3 Mixed ANOVA + retention simple effects
# --------------------------------------------------------------------------- #
def mixed_anova_table(df):
    long = df.melt(id_vars=["student_id", "group"], value_vars=TIMES,
                   var_name="time", value_name="score")
    long["time"] = pd.Categorical(long["time"], categories=TIMES, ordered=True)
    aov = pg.mixed_anova(data=long, dv="score", within="time",
                         between="group", subject="student_id")
    # Mauchly sphericity on the within factor
    try:
        sp = pg.sphericity(long, dv="score", subject="student_id", within="time")
        ok = bool(getattr(sp, "spher", sp[0]))
        W = float(getattr(sp, "W", sp[1]))
        pv = float(getattr(sp, "pval", sp[4]))
        sph_note = (f"Mauchly W={W:.3f}, p={pv:.3f} — sphericity "
                    f"{'met' if ok else 'violated; Greenhouse-Geisser (p-GG-corr) applies'}")
    except Exception as e:
        sph_note = f"(sphericity check skipped: {e})"
    return _round(aov), sph_note


def retention_simple_effects(df):
    out = []
    for grp in GROUPS:
        sub = df[df.group == grp]
        t = pg.ttest(sub["delayed"], sub["posttest"], paired=True)
        out.append(dict(group=grp,
                        post_M=round(sub["posttest"].mean(), 2),
                        delayed_M=round(sub["delayed"].mean(), 2),
                        change=round(sub["delayed"].mean() - sub["posttest"].mean(), 2),
                        t=round(float(t["T"].iloc[0]), 3),
                        p=round(float(t["p-val"].iloc[0]), 3),
                        d=round(float(t["cohen-d"].iloc[0]), 3)))
    # between-group at delayed
    a = df.loc[df.group == "Experimental", "delayed"]
    b = df.loc[df.group == "Control", "delayed"]
    bt = pg.ttest(a, b, paired=False)
    between = dict(group="Exp vs Control @ delayed",
                   post_M=np.nan, delayed_M=np.nan,
                   change=round(a.mean() - b.mean(), 2),
                   t=round(float(bt["T"].iloc[0]), 3),
                   p=round(float(bt["p-val"].iloc[0]), 3),
                   d=round(float(bt["cohen-d"].iloc[0]), 3))
    out.append(between)
    return pd.DataFrame(out)


# --------------------------------------------------------------------------- #
# §4.4 Usage -> gain (experimental group)
# --------------------------------------------------------------------------- #
def usage_analysis(df):
    exp = df[df.group == "Experimental"].copy()
    preds = [c for c in USAGE if c in exp.columns and exp[c].notna().any()]
    if not preds:
        return None, None
    exp = exp.dropna(subset=preds + ["pretest", "posttest"])
    exp["gain"] = exp["posttest"] - exp["pretest"]

    corr_rows = []
    for p in preds:
        c = pg.corr(exp[p], exp["gain"])
        corr_rows.append(dict(predictor=p, r=round(float(c["r"].iloc[0]), 3),
                              p=round(float(c["p-val"].iloc[0]), 3),
                              n=int(c["n"].iloc[0])))
    corr = pd.DataFrame(corr_rows)

    # standardized betas via z-scored regression
    z = exp[preds + ["gain"]].apply(lambda s: (s - s.mean()) / s.std(ddof=1))
    reg = pg.linear_regression(z[preds], z["gain"])
    reg = reg.rename(columns={"names": "predictor", "coef": "beta"})
    keep = [c for c in ["predictor", "beta", "se", "T", "pval", "r2", "adj_r2"] if c in reg.columns]
    reg = _round(reg[keep])
    return corr, reg


# --------------------------------------------------------------------------- #
# §4.5 Questionnaire
# --------------------------------------------------------------------------- #
def questionnaire(df):
    exp = df[df.group == "Experimental"]
    subs = [c for c in SUBSCALES if c in exp.columns and exp[c].notna().any()]
    if not subs:
        return None
    rows = []
    for s in subs:
        v = exp[s].dropna()
        rows.append(dict(subscale=s, n=int(v.count()), M=round(v.mean(), 2),
                         SD=round(v.std(ddof=1), 2),
                         pct_agree=round(float((v >= 4).mean() * 100), 1)))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def run(df, outdir):
    os.makedirs(outdir, exist_ok=True)
    md = ["# §4 Results — auto-generated tables\n"]

    def emit(title, obj, fname=None, note=None):
        print("\n" + "=" * 78 + f"\n{title}\n" + "=" * 78)
        md.append(f"\n## {title}\n")
        if isinstance(obj, pd.DataFrame):
            print(obj.to_string(index=False))
            md.append("\n" + obj.to_markdown(index=False) + "\n")
            if fname:
                obj.to_csv(os.path.join(outdir, fname), index=False)
        else:
            print(obj)
            md.append(f"\n{obj}\n")
        if note:
            print("  " + note)
            md.append(f"\n_{note}_\n")

    emit("§4.1  Descriptive statistics", descriptives(df), "t1_descriptives.csv")
    emit("§4.1  Assumption checks", assumptions(df), "t2_assumptions.csv")
    b = baseline(df)
    emit("§4.1  Baseline equivalence (pretest t-test)",
         f"t({b['dof']}) = {b['t']}, p = {b['p']}, d = {b['d']}  ->  "
         f"groups {'equivalent' if b['equivalent'] else 'NOT equivalent'} at baseline")

    emit("§4.2  RQ2 — Grammar ANCOVA (post-test; covariate = pretest)", ancova_table(df), "t3_ancova.csv")
    emit("§4.2  RQ2 — Pretest-adjusted grammar means", adjusted_means(df), "t4_adjusted_means.csv")

    aov, sph = mixed_anova_table(df)
    emit("§4.3  RQ2 — Grammar retention: Mixed ANOVA (Condition x Time)", aov, "t5_mixed_anova.csv", note=sph)
    emit("§4.3  RQ2 — Grammar retention: simple effects", retention_simple_effects(df), "t6_retention.csv")

    corr, reg = usage_analysis(df)
    if corr is not None:
        emit("§4.4  Exploratory — Usage x gain correlations", corr, "t7_correlations.csv")
        emit("§4.4  Exploratory — Usage regression (standardized betas)", reg, "t8_regression.csv")
    else:
        emit("§4.4  Exploratory — Usage analysis", "skipped (no usage columns with data)")

    q = questionnaire(df)
    if q is not None:
        emit("§4.5  RQ3 — Teacher questionnaire subscales", q, "t9_questionnaire.csv")
    else:
        emit("§4.5  RQ3 — Teacher questionnaire", "skipped (no subscale columns with data)")

    with open(os.path.join(outdir, "results_tables.md"), "w") as f:
        f.write("\n".join(md))
    print("\n" + "-" * 78)
    print(f"[+] CSV tables + results_tables.md written to  {outdir}/")


def main():
    ap = argparse.ArgumentParser(description="Taallim pilot §4 analysis")
    ap.add_argument("--input", help="path to pilot CSV (wide format)")
    ap.add_argument("--outdir", default="outputs")
    ap.add_argument("--make-sample", action="store_true",
                    help="write sample_pilot_data.csv and exit")
    args = ap.parse_args()

    if args.make_sample:
        make_sample()
        return
    path = args.input
    if not path:
        path = make_sample()  # generate + use sample for a self-contained demo
        print("[i] no --input given; running on the generated sample.\n")
    df = load(path)
    run(df, args.outdir)


if __name__ == "__main__":
    main()
