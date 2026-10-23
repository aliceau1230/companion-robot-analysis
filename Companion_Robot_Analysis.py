"""English companion robot analysis. Run from the unzipped project folder."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
Path("charts").mkdir(exist_ok=True)
Path("interactive").mkdir(exist_ok=True)
import matplotlib
matplotlib.use("Agg")

# # Data Analysis for the Development of Companion Robots for Older Adults
# ## Interaction experience, continued use and the Guardian proposal
# 
# Class: CT2985013  
# Student Name: Wong Chei Oi (Alice)
# 
# Main question: What do conversation records and ratings reveal about interaction experience, and which improvements should a product team examine next?
# 
# **HRI CUES** stands for **Human-Robot Interaction Conversational User Enjoyment Scale**. Observers use it to assess enjoyment during robot conversations. The user questionnaire gives a separate self-reported perspective.
# 
# The main dataset contains 590 repeated dialogue turns from 25 participants. The nine supplementary CSVs contain published summaries from separate sources. They are not extra HRI CUES participants. Guardian and the four-week test plan are proposals, not completed trials.
# 
# Source: [HRI CUES dataset, Irfan et al. (2024)](https://doi.org/10.5281/zenodo.12588810). Scale paper: [Irfan et al. (2026)](https://doi.org/10.1109/TAFFC.2025.3590359).

# ## 1. Import analysis libraries
# Pandas works with tables. NumPy supports numeric calculations. Matplotlib, Seaborn and Plotly create charts.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ## 2. Read the CSV files
# The turn file uses a semicolon separator. The survey file uses a comma separator.

df = pd.read_csv("data/HRICUES_Dataset_Exchanges.csv", sep=";")
df_survey = pd.read_csv("data/HRICUES_Dataset_Overall.csv")

# ### View the first five rows
# `head()` lets us check column names and example values.

df.head()

df_survey.head()

# ### Check table size
# `shape` returns the number of rows and columns.

df.shape

df_survey.shape

# ### View data information
# `info()` shows column types and non-missing counts.

df.info()

df_survey.info()

# ### View summary statistics
# `describe()` summarises numeric columns. Its count is a row count, not the number of independent participants.

df.describe().round(2)

df_survey.describe().round(2)

# ### Inspect text columns and participant IDs
# Use object summaries, unique IDs and a transposed preview to inspect the data.

df.describe(include="O")

df["Participant"].unique()

df_survey.head(3).T

# ## 3. Check missing and duplicate records
# P21 has a missing satisfaction answer. Keep it missing. Do not invent an answer.

df.isnull().sum()

df_survey.isnull().sum()

print("Duplicate turn rows:", df.duplicated().sum())
print("Duplicate participant-turn keys:", df.duplicated(["Participant", "Turn"]).sum())
print("Duplicate survey IDs:", df_survey["Participant"].duplicated().sum())
print("Participants:", df["Participant"].nunique())

# ### Create a small DataFrame
# Each row below summarises one input file. The original CSV files stay unchanged.

data_check = pd.DataFrame({
    "Dataset": ["Dialogue turns", "Survey"],
    "Rows": [len(df), len(df_survey)],
    "Columns": [len(df.columns), len(df_survey.columns)],
    "Missing cells": [df.isna().sum().sum(), df_survey.isna().sum().sum()]
})
data_check

# ## 4. Calculate turn duration and mean rating
# Convert the start and end times into seconds, then subtract them. A turn includes both robot and user responses. It is not robot waiting time.

df["start_seconds"] = pd.to_timedelta(df["Start Time"].str.replace(",", ".", regex=False)).dt.total_seconds()
df["end_seconds"] = pd.to_timedelta(df["End Time"].str.replace(",", ".", regex=False)).dt.total_seconds()
df["duration_seconds"] = df["end_seconds"] - df["start_seconds"]
df[["Participant", "Turn", "duration_seconds"]].head()

# ### Average the three ratings within each turn
# `axis=1` means calculate across the selected columns in the same row. Ratings use a 1-5 scale.

rating_columns = ["Annotator 1 Score", "Annotator 2 Score", "Annotator 3 Score"]
df["turn_observer_mean"] = df[rating_columns].mean(axis=1)
df[["Participant", "Turn", "turn_observer_mean"]].head()

# ## 5. Count turns by participant
# `groupby()` collects rows with the same participant ID. `count()` counts their turns.

turn_counts = df.groupby("Participant")["Turn"].count().reset_index()
turn_counts = turn_counts.rename(columns={"Turn": "turn_count"})
turn_counts["participant_number"] = turn_counts["Participant"].str.replace("P", "", regex=False).astype(int)
turn_counts = turn_counts.sort_values("participant_number")
turn_counts.head()

# ### Chart 1: Turns per participant
# Participants had 12-29 turns, averaging 23.6. A workshop time limit means more turns do not prove greater willingness to continue.

plt.figure(figsize=(11, 4.5))
sns.countplot(x="Participant", data=df, order=turn_counts["Participant"], color="steelblue")
plt.title("Dialogue turns per participant")
plt.xlabel("Participant")
plt.ylabel("Number of turns")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("charts/chart_01.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 6. Summarise turn duration
# The mean is 17.73 seconds and the median is 17 seconds.

df["duration_seconds"].describe().round(2)

print("Mean seconds:", np.round(df["duration_seconds"].mean(), 2))
print("Coded minutes:", np.round(df["duration_seconds"].sum() / 60, 2))

# ### Chart 2: Turn duration distribution
# Use equal five-second bins and a smooth density estimate to show where turn durations cluster. The curve follows the sample and is not an assumed normal distribution. Turns include both speakers, not just system response time.

plt.figure(figsize=(10, 4.5))
sns.histplot(data=df, x="duration_seconds", bins=14, binrange=(0, 70),
             kde=True, kde_kws={"cut": 0}, line_kws={"linewidth": 2.5}, color="steelblue")
plt.title("Dialogue turn duration distribution")
plt.xlabel("Seconds per turn")
plt.ylabel("Number of turns")
plt.xlim(0, 70)
plt.tight_layout()
plt.savefig("charts/chart_02.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 7. Compare enjoyment across participants
# Keep the participant means and use a boxplot to show variation across each person's turns.

participant_scores = df.groupby("Participant")["turn_observer_mean"].mean().reset_index()
participant_scores = participant_scores.sort_values("turn_observer_mean")
participant_scores.round(2)

# ### Chart 3: Enjoyment distributions by participant
# The box shows the middle 50% of turn scores. The line is the median and the white diamond is the mean. Whiskers extend within 1.5 times the interquartile range; circles beyond them are not necessarily errors. Turns from the same person are repeated observations.

plt.figure(figsize=(13, 5.5))
sns.boxplot(data=df, x="Participant", y="turn_observer_mean",
            order=turn_counts["Participant"], color="lightblue", showmeans=True,
            medianprops={"color": "#173438", "linewidth": 2},
            meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": "black", "markersize": 4})
plt.title("Observed enjoyment across dialogue turns", pad=38)
plt.text(0.5, 1.03, "Box: middle 50% | Line: median | Diamond: mean | Circles: outliers",
         transform=plt.gca().transAxes, ha="center", fontsize=10)
plt.xlabel("Participant")
plt.ylabel("Mean observer score per turn (1-5)")
plt.ylim(1, 5)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("charts/chart_03.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 8. Summarise four questionnaire items
# The original questionnaire has four items, not five. Show the overall observer mean separately as a fifth measure from a different source. Higher strangeness means feeling more strange, not greater satisfaction.

positive_items = ["user_satisfaction_ratings", "it_was_fun_talking_ratings", "interesting_conversation_ratings"]
questionnaire_items = positive_items + ["it_felt_strange_ratings"]
df_survey[questionnaire_items].describe().round(2)

survey_summary = pd.DataFrame({
    "Item": ["Satisfaction", "Fun", "Interest", "Strangeness"],
    "Mean": df_survey[questionnaire_items].mean().values,
    "Answers": df_survey[questionnaire_items].count().values
})
observer_columns = ["annotator1_overal_ratings", "annotator2_overal_ratings", "annotator3_overal_ratings"]
observer_overall_mean = df_survey[observer_columns].mean(axis=1).mean()
survey_summary.round(2)

# ### Chart 4: Four user items and one observer measure
# User means are 3.29, 4.00, 3.20 and 3.00. The overall observer mean is 3.69. These are five measures, not five questionnaire items. Do not combine them into one score.

fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True,
                         gridspec_kw={"width_ratios": [4, 1.8]})
axes[0].bar(["Satisfaction\n(n=24)", "Fun\n(n=25)", "Interest\n(n=25)", "Strangeness\n(n=25)"],
            survey_summary["Mean"], color=["steelblue", "darkorange", "seagreen", "gray"])
axes[0].set_title("Four user questionnaire items\nHigher strangeness = feeling more strange")
axes[0].set_ylabel("Mean rating (1-5)")
axes[0].set_ylim(0, 5)
axes[1].bar(["Overall observer\n(n=25)"], [observer_overall_mean], color="mediumpurple")
axes[1].set_title("Overall observer rating\nDifferent source")
axes[1].set_ylim(0, 5)
for ax in axes:
    ax.bar_label(ax.containers[0], fmt="%.2f", padding=3)
plt.tight_layout()
plt.savefig("charts/chart_04.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 9. Compare user and observer ratings
# Use complete answers for the three positive items. This exploratory three-item average is not a validated scale. Exclude the strangeness item and the published composite.
# 
# `merge()` joins the turn counts and survey by matching participant IDs.

paired = df_survey.dropna(subset=positive_items).copy()
paired["positive_item_mean"] = paired[positive_items].mean(axis=1)
overall_rating_columns = ["annotator1_overal_ratings", "annotator2_overal_ratings", "annotator3_overal_ratings"]
paired["overall_observer_mean"] = paired[overall_rating_columns].mean(axis=1)
paired = turn_counts.merge(paired, on="Participant")
print("Complete participants:", len(paired))
paired[["Participant", "positive_item_mean", "overall_observer_mean"]].head()

# ### Chart 5: User and observer ratings with a fitted line
# Each point is one participant; some overlap. The orange line is a descriptive linear fit. Its slight downward slope and the scattered points do not establish causation or support reliable individual predictions. No confidence band is shown.

plt.figure(figsize=(9, 5.5))
sns.regplot(data=paired, x="positive_item_mean", y="overall_observer_mean", ci=None,
            scatter_kws={"alpha": 0.75},
            line_kws={"color": "darkorange", "label": "Descriptive linear fit"})
rank_correlation = paired["positive_item_mean"].corr(paired["overall_observer_mean"], method="spearman")
plt.title("User and observer ratings with a fitted line")
plt.text(0.03, 0.96, f"n = {len(paired)} people; Spearman = {rank_correlation:.2f}",
         transform=plt.gca().transAxes, va="top")
plt.xlabel("User positive-item mean (1-5)")
plt.ylabel("Overall observer mean (1-5)")
plt.xlim(0.8, 5.2)
plt.ylim(0.8, 5.2)
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig("charts/chart_05.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Optional analysis: Rank correlation
# Spearman correlation describes the ordering of two scores. Here it is about -0.10 for 24 complete pairs. This descriptive value does not establish causation.

rank_correlation = paired["positive_item_mean"].corr(paired["overall_observer_mean"], method="spearman")
print("Spearman rank correlation:", np.round(rank_correlation, 3))

# ## 10. Compare the three observers within each turn
# Subtract the lowest rating from the highest rating. This describes score spread, not formal inter-rater reliability.

df["rater_range"] = df[rating_columns].max(axis=1) - df[rating_columns].min(axis=1)
rater_spread = df["rater_range"].value_counts().sort_index()
rater_spread

# ### Chart 6: Observer score spread
# Scores are identical in 147 turns. They differ by one point in 331 turns and by at least two points in 112 turns.

plt.figure(figsize=(8, 4.5))
colors = ["steelblue" if gap <= 1 else "darkorange" for gap in rater_spread.index]
bars = plt.bar(rater_spread.index, rater_spread.values, color=colors)
for bar, count in zip(bars, rater_spread.values):
    plt.text(bar.get_x() + bar.get_width()/2, count + 6,
             f"{count}\n({count / len(df):.1%})", ha="center", fontsize=10)
plt.ylim(0, 400)
plt.title("Observer score spread within a dialogue turn\nBlue: gap 0-1; orange: gap 2 or more")
plt.xlabel("Highest rating minus lowest rating")
plt.ylabel("Number of turns")
plt.xticks([0, 1, 2, 3, 4])
plt.tight_layout()
plt.savefig("charts/chart_06.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 11. Main findings
# User and observer ratings describe different perspectives. Ask users directly about their experience.
# 
# This small Swedish workshop sample does not measure long-term use, local demand or safety performance.

# ## 12. Supplementary evidence
# The following ten charts preserve the earlier project evidence. Different samples and measures must be interpreted separately.

projection = pd.read_csv("data/01_hk_projection.csv")
activities = pd.read_csv("data/02_elliq_activities.csv")
feedback = pd.read_csv("data/03_elliq_feedback.csv")
pio = pd.read_csv("data/04_pio_loneliness.csv")
paro = pd.read_csv("data/05_paro_loneliness_change.csv")
retention = pd.read_csv("data/06_hyodol_retention.csv")
reasons = pd.read_csv("data/07_hyodol_return_reasons.csv")
hobbit = pd.read_csv("data/08_hobbit_availability.csv")
fraud = pd.read_csv("data/09_ic3_fraud_2023.csv")

# ### Chart 7: Hong Kong population projection
# The 2023 projection rises from 26% in 2026 to 36% in 2046. This is not observed robot demand.
# 
# All five values are projections published in 2023 and exclude foreign domestic helpers.

plt.figure(figsize=(9, 4.5))
plt.bar(projection["year"].astype(str), projection["older_share_pct"], color=["steelblue", "lightgray", "lightgray", "lightgray", "darkorange"])
plt.title("Hong Kong population aged 65+ (2023 projection)")
plt.xlabel("Year")
plt.ylabel("Population share (%)")
plt.ylim(0, 50)
plt.tight_layout()
plt.savefig("charts/chart_07.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 8: ElliQ activities with Plotly
# Activity shares describe reported use. They do not measure treatment effects.

activity_plot = activities.sort_values("reported_share_pct")
fig_activities = px.bar(activity_plot, x="reported_share_pct", y="activity_en", orientation="h",
                        color="activity_en", text="reported_share_pct",
                        title="ElliQ reported activity categories",
                        labels={"reported_share_pct": "Reported share (%)", "activity_en": "Activity"})
fig_activities.update_layout(showlegend=False, template="plotly_white", height=500)
fig_activities.write_html("interactive/Figure_08.html", include_plotlyjs="../code/plotly.min.js")

# ### Chart 9: ElliQ user feedback
# The reported 94% means users said they felt less lonely. It is not a 94% reduction in a loneliness score. Per-item respondent counts are not provided.

feedback_plot = feedback.sort_values("reported_pct")
plt.figure(figsize=(10, 4.5))
plt.barh(feedback_plot["feedback_en"], feedback_plot["reported_pct"], color=["mediumpurple", "seagreen", "darkorange", "steelblue"])
plt.title("ElliQ self-reported feedback")
plt.xlabel("Positive responses (%)")
plt.xlim(0, 105)
plt.tight_layout()
plt.savefig("charts/chart_09.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 10: PIO before and after
# Compare group means in this non-randomised study. Lower scores indicate less loneliness.

pio_table = pio.pivot(index="group_en", columns="week", values="mean_score")
pio_table = pio_table.reindex(["PIO activity group", "Control group"])
pio_table

pio_table.plot(kind="bar", figsize=(9, 4.5), color=["steelblue", "darkorange"], rot=0)
plt.title("PIO loneliness scores before and after")
plt.xlabel("Group")
plt.ylabel("Mean loneliness score")
plt.ylim(0, 60)
plt.legend(["Before", "Week 6"])
plt.tight_layout()
plt.savefig("charts/chart_10.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 11: PIO observed decrease
# The observed decrease difference is 10.71 points. It is not a causal effect estimate.

pio_decrease = pio_table[0] - pio_table[6]
print("Observed decrease difference:", np.round(pio_decrease.iloc[0] - pio_decrease.iloc[1], 2))
plt.figure(figsize=(9, 4.5))
plt.bar(pio_decrease.index, pio_decrease.values, color=["steelblue", "gray"])
plt.title("PIO observed loneliness score decrease")
plt.xlabel("Group")
plt.ylabel("Score decrease")
plt.tight_layout()
plt.savefig("charts/chart_11.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 12: PARO follow-up
# Negative changes indicate lower loneliness. The Week 10 between-group change result was not statistically conclusive (p=.07).

paro_table = paro.pivot(index="group_en", columns="week", values="mean_change")
paro_table = paro_table.reindex(["PARO activity group", "Control group"])
paro_table.plot(kind="bar", figsize=(9, 4.5), color=["steelblue", "darkorange"], rot=0)
plt.title("PARO change in loneliness from baseline")
plt.xlabel("Group")
plt.ylabel("Score change")
plt.ylim(-12, 12)
plt.legend(["Week 6", "Week 10"])
plt.axhline(0, color="gray", linewidth=0.8)
plt.tight_layout()
plt.savefig("charts/chart_12.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 13: Hyodol retention with Plotly
# 24 of 41 original participants kept the robot after four months (58.5%). This was free use, not a purchase rate.

fig_retention = px.pie(retention, names="outcome_en", values="people", hole=0.6,
                       title="Hyodol outcomes in the original cohort (n=41)",
                       color="outcome_en",
                       color_discrete_map={"Kept after 4 months": "steelblue", "Returned after 4 months": "darkorange", "Returned within 1 week": "lightgray"})
fig_retention.update_traces(textposition="inside", textinfo="value+percent", hovertemplate="%{label}<br>%{value} people (%{percent})<extra></extra>")
fig_retention.update_layout(showlegend=True, height=550, margin={"l":40, "r":40, "t":90, "b":50}, legend={"orientation":"h", "y":-0.15, "x":0})
fig_retention.write_html("interactive/Figure_13.html", include_plotlyjs="../code/plotly.min.js")

# ### Chart 14: Hyodol return reasons
# Eleven four-month returners could give multiple reasons. Counts must not be added as unique people.

reason_plot = reasons.sort_values("mentions")
fig_reasons = px.bar(reason_plot, x="mentions", y="reason_en", orientation="h",
                     color="reason_en", text="mentions",
                     title="Hyodol return reasons (11 returners, multiple responses)",
                     labels={"mentions": "People mentioning a reason", "reason_en": "Reason"})
fig_reasons.update_layout(showlegend=False, template="plotly_white", height=550)
fig_reasons.update_xaxes(dtick=1, range=[0, 6])
fig_reasons.write_html("interactive/Figure_14.html", include_plotlyjs="../code/plotly.min.js")

# ### Chart 15: Hobbit availability with Seaborn
# Use `pivot()` to put modes in columns and features in rows. The percentages describe a 2018 prototype's feature availability, not detection accuracy or rescue success.
# 
# Users experienced Device first, then Companion. The conditions were sequential, not randomised parallel groups. The Working over days in use measure includes partial working days.

availability = hobbit.pivot(index="feature_en", columns="mode_en", values="reported_availability_pct")
availability

plt.figure(figsize=(9, 6))
sns.heatmap(availability, annot=True, fmt=".2f", cmap="YlGnBu", vmin=0, vmax=100,
            cbar_kws={"label": "Reported availability (%)"})
plt.title("Hobbit prototype feature availability")
plt.xlabel("Mode")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("charts/chart_15.png", dpi=200, bbox_inches="tight")
plt.close()

# ### Chart 16: Fraud context
# These are US complaints from people over 60 in six selected categories. They do not measure Hong Kong fraud risk or robot prevention success.

fraud_plot = fraud.sort_values("complaints")
plt.figure(figsize=(10, 5))
plt.barh(fraud_plot["crime_type_original"], fraud_plot["complaints"],
         color=["lightgray", "lightgray", "lightgray", "lightgray", "lightgray", "darkorange"])
plt.title("IC3 2023 complaints: six selected categories, age over 60")
plt.xlabel("Number of complaints")
plt.xlim(0, 21000)
plt.tight_layout()
plt.savefig("charts/chart_16.png", dpi=200, bbox_inches="tight")
plt.close()

# ## 13. Sources and scope
# Main dataset: [HRI CUES, Irfan et al. (2024)](https://doi.org/10.5281/zenodo.12588810).
# Scale paper: [Irfan et al. (2026), HRI CUES](https://doi.org/10.1109/TAFFC.2025.3590359).
# 
# Supplementary CSVs include source URLs and table locators. Interpret each study separately.

print("Analysis complete. Static charts and three offline Plotly views saved.")
