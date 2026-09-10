"""Make a local, script-free image gallery from the actual camera manifest."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, default=ROOT.parent/'output'/'unit6-professional')
args = parser.parse_args()
gallery = args.out/'图册'
record = json.loads((gallery/'视角清单.json').read_text())
groups = {}
for view in record['views']:
    path = gallery/view['image']
    if not path.is_file():
        raise SystemExit('Missing rendered view: '+str(path))
    groups.setdefault(view['group'], []).append(view)
sections = []
for group, views in groups.items():
    figures = []
    for view in views:
        source = html.escape(view['image'], quote=True)
        title = html.escape(view['title'])
        figures.append(f'<figure><a href="{source}"><img src="{source}" alt="{title}" loading="lazy"></a><figcaption><span>{view["id"]}</span> {title}</figcaption></figure>')
    sections.append(f'<section><h2>{html.escape(group)}</h2><div class="grid">'+''.join(figures)+'</div></section>')
page = (ROOT/'professional-gallery-template.html').read_text().replace('{{SECTIONS}}', '\n'.join(sections)).replace('{{COUNT}}', str(len(record['views'])))
(gallery/'全部视角.html').write_text(page)
print('Gallery ready:', len(record['views']), 'local images')
