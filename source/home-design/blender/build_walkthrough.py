"""Bind explicit model geometry/config to the first-person engine, without network IO."""
import argparse
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('scene', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
data = json.loads(args.scene.read_text())
if not data.get('walkthrough'):
    raise SystemExit('Refusing to infer navigation or elevator placement from the old concept scene. Add explicit walkthrough config.')
template = (BASE / 'walkthrough-template.html').read_text()
core = (BASE / 'walkthrough-core.mjs').read_text()
core = re.sub(r'^export ', '', core, flags=re.M)
template = template.replace('/* WALKTHROUGH_CORE_BEGIN */\n/* WALKTHROUGH_CORE_END */', core)
serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
template = template.replace('<script type="application/json" id="family-house-walkthrough-data">null</script>', '<script type="application/json" id="family-house-walkthrough-data">' + serialized + '</script>')
if len(template.encode()) > 1_000_000:
    raise SystemExit('Inline viewer exceeds 1 MB. Simplify scene objects before binding.')
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(template)
print(f'Bound {len(data.get("objects", []))} objects into {args.output}')
