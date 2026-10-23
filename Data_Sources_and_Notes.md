# Data sources and interpretation notes

The original CSV files and Excel reading copy are preserved byte for byte. No source values or missing answers have been changed.

## Main dataset

HRI CUES means Human-Robot Interaction Conversational User Enjoyment Scale. The Exchanges file has 590 turns from 25 people and uses semicolon separators. Overall has 25 participant rows and uses commas. Turn duration is end time minus start time and includes both speakers. Observer means are averages of three ratings. The three-positive-item user mean is exploratory, not a validated scale. P21 has no satisfaction answer, so the paired comparison uses 24 people.

## Figure crosswalk

| Figure | Subject | Report page |
| --- | --- | --- |
| 7 | Hong Kong population aged 65+ (2023 projection) | 3 |
| 1 | Dialogue turns per participant | 5 |
| 2 | Dialogue turn duration distribution | 5 |
| 3 | Observed enjoyment across dialogue turns | 6 |
| 4 | User questionnaire and observer ratings | 6 |
| 5 | 24 complete pairs (Spearman = -0.10) | 7 |
| 6 | Observer score spread (590 turns) | 7 |
| 8 | ElliQ activity categories | 8 |
| 9 | ElliQ self-reported feedback | 8 |
| 10 | PIO loneliness scores before and after | 9 |
| 11 | PIO observed score decrease | 9 |
| 12 | PARO change at Weeks 6 and 10 | 10 |
| 13 | Hyodol outcomes in the original cohort | 10 |
| 14 | Hyodol return reasons after four months | 11 |
| 16 | IC3 2023 complaints: six selected categories, age over 60 | 12 |
| 15 | Hobbit prototype feature availability | 12 |

## Figure 7 Hong Kong population aged 65+ (2023 projection)

The 2023 projection rises from 26% in 2026 to 36% in 2046, a rise of 10 percentage points. This does not measure demand for robots. Foreign domestic helpers are excluded.

Source: Census and Statistics Department (2023), Appendix B, Table B1.

## Figure 1 Dialogue turns per participant

590 turns from 25 people. Participants have 12-29 turns, averaging 23.6. Turns are repeated observations and do not establish willingness to continue.

Source: Irfan et al. (2024), Exchanges.

## Figure 2 Dialogue turn duration distribution

Mean duration: 17.73 seconds. Five-second bins and a KDE describe this sample. A turn includes both speakers and does not measure system latency.

Source: Irfan et al. (2024), Exchanges. Author calculations.

## Figure 3 Observed enjoyment across dialogue turns

The box shows the middle 50% of scores and the solid line is the median. In this interactive version, the dashed line marks the mean. Points beyond the whiskers are outliers under the boxplot rule. Repeated turns are not independent people.

Source: Irfan et al. (2024), Exchanges. Author calculations.

## Figure 4 User questionnaire and observer ratings

Four questionnaire items and one separate overall observer measure. Higher strangeness means feeling more strange. P21 satisfaction remains missing. The observer measure is not a fifth survey item.

Source: Irfan et al. (2024), Overall. Author calculations.

## Figure 5 24 complete pairs (Spearman = -0.10)

24 complete participants. Spearman is about -0.10. The orange line is a descriptive linear fit, not a Spearman line. No causal interpretation or individual prediction is supported.

Source: Irfan et al. (2024), Overall. Author calculations.

## Figure 6 Observer score spread (590 turns)

147 turns have identical ratings, 331 differ by one point and 112 differ by at least two. Blue: gaps 0-1, 478 turns (81.0%). Orange: gaps at least 2, 112 turns (19.0%). This is not a formal inter-rater reliability measure.

Source: Irfan et al. (2024), Exchanges. Author calculations.

## Figure 8 ElliQ activity categories

Companionship accounts for 40.1% of reported activities. The shares total 99.9% due to published rounding. Activity shares do not measure treatment effects.

Source: Intuition Robotics (2026), p. 6.

## Figure 9 ElliQ self-reported feedback

94% reported feeling less lonely. Per-item respondent counts are unspecified. This does not mean a 94% fall in a loneliness score.

Source: Intuition Robotics (2026), p. 3.

## Figure 10 PIO loneliness scores before and after

PIO activity group: 31 people. Control group: 33. Lower scores mean less loneliness. The non-randomised programme also included staff-led activities.

Source: Lim (2023), Table 4.

## Figure 11 PIO observed score decrease

The activity group decreased by 11.26 points and the control group by 0.55, a difference of 10.71. This observed difference is not an isolated causal effect of the robot.

Source: Lim (2023), Table 4. Author calculations.

## Figure 12 PARO change at Weeks 6 and 10

PARO activity group: 58 people. Control: 60. Negative change means less loneliness. The Week 10 between-group change result, p=.07, is statistically inconclusive.

Source: Chen et al. (2024), Table 4.

## Figure 13 Hyodol outcomes in the original cohort

All percentages use the original 41 participants. 24 kept the robot, 11 returned it after four months and 6 within one week. Free retention is not a purchase rate.

Source: Lee et al. (2024), Methods 2.2 and Results 3.4.

## Figure 14 Hyodol return reasons after four months

11 four-month returners could give multiple reasons. Reason counts must not be added as unique people. Blank cells in the published table are not treated as zero.

Source: Lee et al. (2024), Table 4.

## Figure 16 IC3 2023 complaints: six selected categories, age over 60

US administrative complaints in 2023, age group Over 60, six selected categories only. These are not Hong Kong fraud rates or evidence of robot prevention.

Source: FBI (2024), 2023 Elder Fraud Report, p. 7.

## Figure 15 Hobbit prototype feature availability

The authors' Working over days in use availability indicator includes partial days. Users experienced Device first, then Companion. These were sequential conditions, not randomised parallel groups. These values are not detection accuracy, rescue success or Guardian targets.

Source: Bajones et al. (2018), Table 2.

## Data dictionary

The CSV headers name the original variables. Supplementary labels ending in `_en` are English display labels. `source_url`, table locators and related note columns record source provenance. Population percentages are percentages, fraud observations are complaint counts, loneliness observations are group means or mean changes, retention is a count of people, and return reasons are counts of mentions. Do not combine these units.

## Scope

HRI CUES workshop evidence does not establish local demand, long-term outcomes or safety performance. Support features require separate supervised testing. Source URLs and study details are retained in `sources/`. The HRI CUES scale paper citation follows the 2026 journal issue used in the final report. The supplied report is authoritative for the conclusions.
