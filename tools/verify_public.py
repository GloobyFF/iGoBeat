"""Anonymous mirror validation, run on a GitHub-hosted Linux runner."""
import concurrent.futures,hashlib,json,pathlib,time,urllib.request,urllib.parse,zipfile,tempfile,os
repo=os.environ.get('GITHUB_REPOSITORY','GloobyFF/iGoBeat')
base=f'https://raw.githubusercontent.com/{repo}/main/'
start=time.monotonic()
def get(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=60) as response:return response.read()
  except Exception:
   if attempt==2:raise
   time.sleep(2*(attempt+1))
assert get(base+'version').strip()==b'2'
url=base+'config1.1.1';rows=[];seen=set()
while url:
 assert url not in seen;seen.add(url)
 p=json.loads(get(url));rows+=p['datas'];url=urllib.parse.urljoin(base,p['nextPage']) if p.get('nextPage') else None
assert len({e['guid'] for e in rows})==len(rows)
def package(e):
 data=get(e['packagePath'])
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],e['guid']
 import io
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  assert z.testzip() is None
  cfg=json.loads(z.read(e['guid']+'/config'))
  assert cfg['guid']==e['guid'] and cfg['mode']==e['mode'] and bool(cfg.get('isVip'))==bool(e.get('vipOnly'))
 return len(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:total=sum(pool.map(package,rows))
images={urllib.parse.urljoin(base,e['coverPath']) for e in rows if e.get('coverPath')}
notices=json.loads(get(base+'announcements.json'))
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='imagePath' and x:images.add(urllib.parse.urljoin(base,x))
   elif isinstance(x,(list,dict)):walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(notices)
def image(url):
 data=get(url);assert data.startswith(b'\x89PNG\r\n\x1a\n') or data.startswith(b'\xff\xd8\xff')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(image,images))
assert all(e['packagePath'].startswith(f'https://github.com/{repo}/releases/download/') for e in rows)
r={'runnerOS':os.environ.get('RUNNER_OS'),'runnerArchitecture':os.environ.get('RUNNER_ARCH'),'songs':len(rows),'vip':sum(e.get('vipOnly',False) for e in rows),'anonymousFullPackages':len(rows),'packageBytes':total,'anonymousImages':len(images),'elapsedSeconds':round(time.monotonic()-start,2),'baseURL':base}
pathlib.Path('verification-report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
