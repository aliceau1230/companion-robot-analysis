"""Rebuild the English offline chart page from the saved figure snapshot.
Run: python code/rebuild_interactive_charts.py
No extra Python packages are needed. CSV changes do not update this snapshot.
"""
from pathlib import Path
import json
import html

root = Path(__file__).resolve().parent.parent
figures = json.loads((root / 'code/interactive_figures.json').read_text())
vendor = (root / 'code/plotly.min.js').read_text()
parts = ['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Companion Robot Analysis - Offline Charts</title><style>body{font:17px/1.6 Arial,sans-serif;color:#173438;margin:0;background:#fbfaf6}main{max-width:1160px;margin:auto;padding:28px}h1{font-size:36px}h2{font-size:25px}a{color:#176f73}nav{columns:2;line-height:2}nav a{display:block}section{margin:60px 0;scroll-margin-top:16px}p{max-width:1050px}.chart{width:100%;min-height:560px;background:white}.source{font-size:14px;color:#53656c}</style><main id="top"><h1>Companion Robot Analysis</h1><p>Offline interactive charts in English. Figure numbers follow the notebook. Hover for values, drag to zoom, and double-click to reset. The JavaScript is included, so the charts work offline.</p><p>HRI CUES means Human-Robot Interaction Conversational User Enjoyment Scale. Studies involve different participants, settings and measures and should be interpreted separately.</p><nav>''']
for f in figures:
    title = html.escape(f['layout']['title']['text'])
    parts.append(f'<a href="#figure-{f["figure"]}">Figure {f["figure"]}: {title}</a>')
parts.append('</nav>')
for f in figures:
    n = f['figure']
    title = html.escape(f['layout']['title']['text'])
    parts.append(f'<section id="figure-{n}"><h2>Figure {n}: {title}</h2><p>{html.escape(f["note"])}</p><div class="chart" id="chart-{n}"></div><p class="source">Source: {html.escape(f["source"])}</p><a href="#top">Back to contents</a></section>')
parts.append('</main><script>' + vendor + '</script><script>')
for f in figures:
    parts.append('Plotly.newPlot(' + json.dumps('chart-' + str(f['figure'])) + ',' + json.dumps(f['data']) + ',' + json.dumps(f['layout']) + ',{"responsive":true,"displaylogo":false});')
parts.append('</script></html>')
output = root / 'interactive/All_Charts_Offline.html'
output.write_text('\n'.join(parts), encoding='utf-8')
print('Rebuilt', output.name, 'with', len(figures), 'English interactive charts.')
