"""Build a VPM listing from public GitHub release assets. Standard library only."""
import argparse, hashlib, io, json, os, re, zipfile
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse

def fetch(url, api=False):
    headers={'User-Agent':'MitsuboshiStudio-VPM','Accept':'application/vnd.github+json' if api else '*/*'}
    # The token is used only for the GitHub API, never for release/CDN/Pages downloads.
    if api:
        if urlparse(url).hostname!='api.github.com': raise ValueError('Unexpected API host')
        if os.environ.get('GITHUB_TOKEN'): headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request(url,headers=headers),timeout=60) as r: return r.read()

def semver(value):
    match=re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?',value)
    if not match or (match[4] and any(p.isdigit() and len(p)>1 and p[0]=='0' for p in match[4].split('.'))):
        raise ValueError('Invalid release version: '+value)

def release_manifest(repo,release,download=fetch):
    assets={a['name']:a['browser_download_url'] for a in release['assets']}
    if 'package.json' not in assets: return None # Non-VPM historical releases are not indexed.
    prefix=f'https://github.com/{repo}/releases/download/{release["tag_name"]}/'
    if any(not u.startswith(prefix) for u in assets.values()): raise ValueError('Release asset URL outside its release')
    manifest=json.loads(download(assets['package.json']).decode('utf-8-sig'))
    for key in ('name','version','displayName','author','url','unity','license'):
        if not manifest.get(key): raise ValueError('Missing manifest field: '+key)
    if not manifest['author'].get('name'): raise ValueError('Missing author name')
    name,version=manifest['name'],manifest['version']
    if not re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)+',name): raise ValueError('Invalid package ID')
    semver(version)
    if release['tag_name']!='v'+version: raise ValueError('Tag/version mismatch')
    if bool(release['prerelease'])!=('-' in version): raise ValueError('Prerelease flag/version mismatch')
    archive_name=f'{name}-{version}.zip'
    if archive_name not in assets: raise ValueError('Missing VPM ZIP')
    if manifest['url']!=assets[archive_name]: raise ValueError('Manifest URL differs from release asset')
    data=download(assets[archive_name])
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        paths=z.namelist()
        if len(paths)!=len(set(paths)): raise ValueError('Duplicate ZIP entries')
        if any(PurePosixPath(p).is_absolute() or '..' in PurePosixPath(p).parts or '\\' in p for p in paths):
            raise ValueError('Unsafe ZIP path')
        if 'package.json' not in paths: raise ValueError('Manifest must be at ZIP root')
        if sum(i.file_size for i in z.infolist())>256*1024*1024: raise ValueError('Unexpected uncompressed package size')
        if json.loads(z.read('package.json').decode('utf-8-sig'))!=manifest: raise ValueError('ZIP/asset manifest mismatch')
        if z.testzip() is not None: raise ValueError('ZIP CRC failure')
    result=dict(manifest)
    result['zipSHA256']=hashlib.sha256(data).hexdigest()
    return result

def preserve(previous,current):
    if previous.get('id')!=current['id']: raise ValueError('Listing ID changed')
    for name,package in previous.get('packages',{}).items():
        for version,old in package['versions'].items():
            new=current['packages'].get(name,{}).get('versions',{}).get(version)
            if new is None: raise ValueError(f'Previously published version disappeared: {name} {version}')
            if old!=new: raise ValueError(f'Published version mutated: {name} {version}')

def build(source,get=fetch):
    result={k:source[k] for k in ('name','id','author','url')}
    result['packages']={}
    seen=set()
    for repo in source['githubRepos']:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or repo in seen: raise ValueError('Invalid/duplicate repository')
        seen.add(repo)
        page=1
        while True:
            releases=json.loads(get(f'https://api.github.com/repos/{repo}/releases?per_page=100&page={page}',api=True))
            for release in releases:
                if release['draft']: continue
                m=release_manifest(repo,release,download=get)
                if m is None: continue
                versions=result['packages'].setdefault(m['name'],{'versions':{}})['versions']
                if m['version'] in versions: raise ValueError('Duplicate package version across releases/repositories')
                versions[m['version']]=m
            if len(releases)<100: break
            page+=1
    if not result['packages']: raise ValueError('No VPM releases found; refusing empty listing')
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',default='source.json');p.add_argument('--out',default='dist')
    args=p.parse_args()
    source=json.loads(Path(args.source).read_text(encoding='utf-8'))
    result=build(source)
    try: previous=json.loads(fetch(source['url']))
    except HTTPError as e:
        if e.code!=404: raise
    else: preserve(previous,result)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/'index.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'.nojekyll').touch()
    print('Validated listing:',sum(len(p['versions']) for p in result['packages'].values()),'versions')

if __name__=='__main__': main()
