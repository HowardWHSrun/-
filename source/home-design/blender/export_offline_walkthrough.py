"""Export the existing walkthrough as a self-contained, double-clickable HTML.

The production artifact makes no network requests and needs no local web server.
Three.js is MIT licensed; its pinned source and license are vendored beside this script.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = Path('/Users/howardwang/.codex/plugins/cache/openai-bundled/visualize/1.0.32/skills/visualize')
parser = argparse.ArgumentParser()
parser.add_argument('--scene', type=Path, default=ROOT / 'unit6-professional-scene.json')
parser.add_argument('--out', type=Path, default=ROOT.parent / 'output' / 'unit6-professional')
parser.add_argument('--pdf', default='设计图册.pdf')
parser.add_argument('--blend', default='模型/第6户_三层住宅.blend')
parser.add_argument('--glb', default='模型/第6户_三层住宅.glb')
args = parser.parse_args()
out = args.out.resolve()
walk = out / '漫游'
walk.mkdir(parents=True, exist_ok=True)
staging = ROOT / 'qa' / 'offline-export'
staging.mkdir(parents=True, exist_ok=True)
fragment = staging / 'walkthrough-fragment.html'
wrapped = staging / 'walkthrough-host-export.html'
subprocess.run([sys.executable, str(ROOT / 'build_walkthrough.py'), str(args.scene.resolve()), str(fragment)], check=True)
# Use the documented export flow before removing host-only helpers and inlining Three.
subprocess.run([sys.executable, str(SKILL / 'scripts' / 'render.py'), str(fragment), str(wrapped), '--force'], check=True)


class FrameReader(HTMLParser):
    content = None

    def handle_starttag(self, tag, attrs):
        if tag == 'iframe':
            self.content = dict(attrs).get('srcdoc')


reader = FrameReader()
reader.feed(wrapped.read_text())
if not reader.content:
    raise RuntimeError('The documented host export did not contain its source frame.')
head = reader.content.split('<body>', 1)[0]
# Only local inline resources are permitted. This policy is also tested with networking disabled.
policy = "default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval'; style-src 'unsafe-inline'; img-src data: blob: file:; font-src 'none'; connect-src 'none'; worker-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
head = re.sub(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">', '<meta http-equiv="Content-Security-Policy" content="' + policy + '">', head)
head = head.replace('lang="en"', 'lang="zh-CN"').replace('<title>Walkthrough Fragment</title>', '<title>第6户住宅 · 离线漫游</title>')
source = (ROOT / 'vendor' / 'three-0.170.0.module.min.js').read_text()
if re.search(r'(^|;)\s*import\s', source):
    raise RuntimeError('The pinned Three build unexpectedly has external imports.')
match = re.search(r'export\{([^}]+)\};?\s*$', source)
if not match:
    raise RuntimeError('The pinned Three module export shape changed.')
exports = []
for item in match.group(1).split(','):
    parts = item.strip().split(' as ')
    if not all(re.fullmatch(r'[A-Za-z_$][A-Za-z0-9_$]*', part.strip()) for part in parts):
        raise RuntimeError('Unsupported Three export declaration: ' + item)
    local, public = parts[0].strip(), parts[-1].strip()
    exports.append(json.dumps(public) + ':' + local)
three = 'const THREE = (()=>{\n' + source[:match.start()] + '\nreturn {' + ','.join(exports) + '};\n})();'
content = fragment.read_text()
import_statement = "const THREE = await import('https://esm.sh/three@0.170.0');"
if content.count(import_statement) != 1:
    raise RuntimeError('Walkthrough Three import not found exactly once.')
content = content.replace(import_statement, three)
content = content.replace('<h3>屋内第一人称漫游</h3>', '<h3>第6户 · 屋内与花园漫游</h3>')
if re.search(r'<script[^>]+src=', content) or "await import('https:" in content:
    raise RuntimeError('An external script remains in the offline export.')
nav = '<nav class="offline-nav" aria-label="交付文件"><a href="../开始查看.html">← 返回开始页</a><a href="../' + escape(args.pdf, quote=True) + '">设计图册 PDF</a><a href="../图册/全部视角.html">全部视角</a></nav>'
style = '<style>body{max-width:1600px;margin:0 auto;padding:16px;box-sizing:border-box}.offline-nav{display:flex;gap:20px;flex-wrap:wrap;margin:0 0 16px}.offline-nav a{color:var(--foreground)}#family-house-walkthrough [data-stage]{height:clamp(430px,72vh,880px)}@media(max-width:560px){body{padding:10px}#family-house-walkthrough [data-stage]{height:64vh}}</style>'
document = head + '<body>' + style + nav + content + '</body></html>'
target = walk / '住宅漫游.html'
target.write_text(document)
(walk / '第三方许可.txt').write_text('Three.js 0.170.0\nSource: https://github.com/mrdoob/three.js/tree/r170\n\n' + (ROOT / 'vendor' / 'three-LICENSE.txt').read_text())

# The start page is deliberately plain HTML: file:// links work after extracting the whole ZIP.
start = (ROOT / 'offline-start-template.html').read_text()
for key, value in {'PDF_PATH': args.pdf, 'BLEND_PATH': args.blend, 'GLB_PATH': args.glb}.items():
    start = start.replace('{{' + key + '}}', escape(value, quote=True))
(out / '开始查看.html').write_text(start)
(out / '打开说明.txt').write_text('第6户住宅设计包\n\n1. 先把 ZIP 完整解压。\n2. 双击「开始查看.html」。\n3. 选择三维漫游、PDF 或多角度图册。\n\n漫游离线可用，无需安装运行环境。进入漫游后：拖动看四周，W/A/S/D 或方向键走动；走进电梯后选择楼层。触屏可长按前进、后退、左移、右移。Esc 暂停。\n\n请保留文件夹结构，勿只取出开始页。Blender 文件可继续编辑；PDF 和图册可独立查看。\n')
manifest = {'scene': args.scene.name, 'scene_sha256': hashlib.sha256(args.scene.read_bytes()).hexdigest(), 'objects': len(json.loads(args.scene.read_text())['objects']), 'offline_html': str(target.relative_to(out)), 'bytes': target.stat().st_size, 'three': '0.170.0', 'network_required': False}
(walk / '离线构建记录.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print(json.dumps(manifest, ensure_ascii=False))
