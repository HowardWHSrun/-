from pathlib import Path
import json,math,collections
from PIL import Image,ImageDraw,ImageFont
base=Path('/Users/howardwang/Desktop/Quick Projects/家装/home-design');out=base/'audit/unit6'
for fid in ['F1','F2']:
 ss=json.load(open(out/f'{fid}-segments-local.json'))
 lines=[]
 for s in ss:
  l=s['layer'].upper()
  if not (l=='WALL' or l.endswith('A-WALL')) or 'WALL-TYPE' in l or 'DZ-3-PLAN' in l:continue
  a=[round(v,3) for v in s['a']];b=[round(v,3) for v in s['b']]
  if max(a[0],b[0])<-.121 or min(a[0],b[0])>9.721 or max(a[1],b[1])<.979 or min(a[1],b[1])>15.5:continue
  if abs(a[0]-b[0])<.002 and abs(a[1]-b[1])>.03:lines.append(dict(axis='v',c=a[0],lo=min(a[1],b[1]),hi=max(a[1],b[1]),source=s['source_handle'],layer=s['layer']))
  elif abs(a[1]-b[1])<.002 and abs(a[0]-b[0])>.03:lines.append(dict(axis='h',c=a[1],lo=min(a[0],b[0]),hi=max(a[0],b[0]),source=s['source_handle'],layer=s['layer']))
 boxes={}
 for i,a in enumerate(lines):
  for b in lines[i+1:]:
   if a['axis']!=b['axis']:continue
   delta=round(abs(a['c']-b['c']),3)
   if delta not in [.12,.24]:continue
   lo=max(a['lo'],b['lo']);hi=min(a['hi'],b['hi'])
   if hi-lo<.025:continue
   c0=min(a['c'],b['c']);c1=max(a['c'],b['c'])
   bounds=[c0,lo,c1,hi] if a['axis']=='v' else [lo,c0,hi,c1]
   if bounds[0]<-.121 or bounds[2]>9.721 or bounds[1]<.97:continue
   k=tuple(bounds);boxes[k]={'bounds':bounds,'source':sorted(set([a['source'],b['source']])),'layers':sorted(set([a['layer'],b['layer']])),'method':'intersection of parallel source wall skins at exact 120/240 mm spacing'}
 # Remove contained duplicate rectangles, retaining longer exact source spans.
 bs=list(boxes.values());bs=[a for i,a in enumerate(bs) if not any(i!=j and a['bounds'][0]>=b['bounds'][0] and a['bounds'][1]>=b['bounds'][1] and a['bounds'][2]<=b['bounds'][2] and a['bounds'][3]<=b['bounds'][3] and a['bounds']!=b['bounds'] for j,b in enumerate(bs))]
 print(fid,'wall lines',len(lines),'boxes',len(bs),flush=True)
 (out/f'{fid}-wall-box-candidates.json').write_text(json.dumps(bs,ensure_ascii=False,indent=2));(out/f'{fid}-wall-lines.json').write_text(json.dumps(lines,ensure_ascii=False,indent=2))
 im=Image.open(out/f'{fid}-unit6-grid.png').convert('RGBA');ov=Image.new('RGBA',im.size);d=ImageDraw.Draw(ov);sc=150;xmin=-.8;ymax=18.1
 def pt(x,y):return ((x-xmin)*sc,(ymax-y)*sc)
 f=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',20)
 for i,a in enumerate(bs):
  x0,y0,x1,y1=a['bounds'];p0=pt(x0,y1);p1=pt(x1,y0);d.rectangle([p0,p1],fill='#e7545488',outline='#9f1414',width=2);d.text(pt((x0+x1)/2,(y0+y1)/2),str(i),font=f,fill='#8f0000')
 Image.alpha_composite(im,ov).convert('RGB').save(out/f'{fid}-wall-box-review.png')
