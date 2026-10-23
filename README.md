# Data Analysis for the Development of Companion Robots for Older Adults

Interaction experience, continued use and the Guardian proposal

Class: CT2985013  
Student Name: Wong Chei Oi (Alice)

English submission edition - 23 October 2026

## Start here

1. Read **Companion_Robot_Report_English.pdf**, the final 21-page report with the approved layout.
2. Open **Guardian_Presentation_English.pptx**, the final 29-slide presentation. Its cover title and subtitle match the report. It contains 13 editable charts and 4 editable tables.
3. Open **Companion_Robot_Analysis.ipynb** for the analysis code and freshly executed outputs. **Notebook_View.html** is a convenient offline reading copy.
4. Open **interactive/All_Charts_Offline.html** for 16 English interactive charts. Extract the entire ZIP before opening files. No internet connection is needed to view the charts.
5. **interactive/Guardian_Demo.html** is an optional fictional scenario demonstration. It does not detect fraud, make calls, send messages or provide rescue.

## Files

| File or folder | Contents |
| --- | --- |
| Companion_Robot_Analysis.ipynb | English notebook, 47 executed code cells |
| Companion_Robot_Analysis.py | Script version of the notebook analysis |
| data/ | 11 original CSVs: 2 HRI CUES files and 9 supplementary files |
| sources/ | Source manifest and reference details |
| Data_Sources_and_Notes.md | Definitions, interpretation limits and report/figure crosswalk |
| HRI_CUES_Source.txt | Dataset DOI and licence |
| Companion_Robot_Report_English.pdf | Final English report |
| Guardian_Presentation_English.pptx | Final editable English presentation |
| Notebook_View.html | Offline notebook reading copy with outputs |
| interactive/ | English chart dashboard, three individual Plotly views and optional concept demo |
| code/ | Bundled Plotly JavaScript, saved chart definitions and rebuild script |
| charts/ | 16 English static chart images |
| assets/ | Concept illustrations used in the materials |
| HRI_CUES_Excel_Readable.xlsx | Original Excel reading copy, not a replacement for the CSVs |
| Submission_Checks.md | Checks completed and verification limits |
| SHA256SUMS.txt | File integrity hashes, excluding this checksum file itself |

Superseded report Word and presentation PDF copies are excluded to avoid mixing revisions. The submitted report PDF and presentation PPTX are the authoritative versions. Chinese presentation/report versions and the mixed-language reference template are excluded. Original CSV source labels and Swedish conversation text are preserved as source records. All analysis explanations and chart display labels are English.

## Run the analysis

Use Python 3.12 or a compatible Python 3 environment. From this unzipped folder:

```bash
python -m pip install -r requirements.txt
jupyter notebook Companion_Robot_Analysis.ipynb
```

Trust this notebook if your Jupyter installation asks before displaying its saved interactive outputs. Restart the kernel and run the cells from the top. The `data/` folder must remain beside the notebook. The three Plotly outputs embed their JavaScript for offline viewing.

Alternatively, run:

```bash
python Companion_Robot_Analysis.py
```

The script uses paths relative to its own location. It exports 13 Matplotlib chart PNGs and three individual offline Plotly HTML views. The three other PNGs in `charts/` are the supplied static report figures for the Plotly analyses. Visual styles can differ between the report, notebook and interactive views, while their values and definitions agree.

To rebuild the dashboard from the saved English figure definitions:

```bash
python code/rebuild_interactive_charts.py
```

This command uses the Python standard library. The dashboard is a checked snapshot of the included CSVs. It does not automatically recalculate after CSV edits. If source values change, rerun the analysis and update the saved dashboard definitions before issuing revised materials.

The notebook HTML reading copy is saved with outputs, so it does not require Python to read. Installing the analysis dependencies requires internet access unless they are already available.

## Interpretation

The main data contain 590 repeated dialogue turns from 25 participants and 25 questionnaire records. P21 satisfaction remains missing. The paired comparison uses 24 complete participants. The nine supplementary CSVs contain 61 aggregate records from different studies and sources, not 61 additional HRI CUES participants.

Studies differ in participants, setting, period and outcome measure. Their results support separate design questions rather than a robot effectiveness ranking. Guardian is a proposed concept. The four-week procedure, five volunteers and 20 scripted cases are proposed, not completed research. Price information is historical source context, not a current quotation.
