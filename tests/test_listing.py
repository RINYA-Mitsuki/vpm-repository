import copy,hashlib,io,json,sys,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from listing import release_manifest,preserve,build

class ListingTests(unittest.TestCase):
    def setUp(self):
        self.repo='owner/tool'
        self.base='https://github.com/owner/tool/releases/download/v1.0.0/'
        self.m={'name':'com.example.tool','version':'1.0.0','displayName':'Tool','author':{'name':'Owner'},'unity':'2022.3','license':'MIT','url':self.base+'com.example.tool-1.0.0.zip'}
        self.release={'tag_name':'v1.0.0','prerelease':False,'draft':False,'assets':[{'name':n,'browser_download_url':self.base+n} for n in ('package.json','com.example.tool-1.0.0.zip')]}
        self.files={self.base+'package.json':json.dumps(self.m).encode()}
        self.zip(self.m)
    def zip(self,m,extra=None):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:
            z.writestr('package.json',json.dumps(m))
            if extra:z.writestr(extra,'x')
        self.files[self.m['url']]=data.getvalue()
    def get(self,url,api=False):return self.files[url]
    def test_verified_hash(self):
        result=release_manifest(self.repo,self.release,self.get)
        self.assertEqual(result['zipSHA256'],hashlib.sha256(self.files[self.m['url']]).hexdigest())
    def test_manifest_mismatch_stops_publish(self):
        self.zip(dict(self.m,version='2.0.0'))
        with self.assertRaises(ValueError):release_manifest(self.repo,self.release,self.get)
    def test_path_traversal_stops_publish(self):
        self.zip(self.m,'../outside')
        with self.assertRaises(ValueError):release_manifest(self.repo,self.release,self.get)
    def test_release_without_zip_stops_publish(self):
        self.release['assets'].pop()
        with self.assertRaises(ValueError):release_manifest(self.repo,self.release,self.get)
    def test_published_version_cannot_disappear_or_change(self):
        previous={'id':'test','packages':{'com.example.tool':{'versions':{'1.0.0':self.m}}}}
        preserve(previous,copy.deepcopy(previous))
        for altered in ({'id':'test','packages':{}},{'id':'different','packages':previous['packages']}):
            with self.assertRaises(ValueError):preserve(previous,altered)
        altered=copy.deepcopy(previous);altered['packages']['com.example.tool']['versions']['1.0.0']['url']='changed'
        with self.assertRaises(ValueError):preserve(previous,altered)
    def test_pagination_and_drafts(self):
        source={'name':'Test','id':'test','author':'Owner','url':'https://example.com/index.json','githubRepos':[self.repo]}
        def get(url,api=False):
            if api:
                if url.endswith('&page=1'): return json.dumps([dict(self.release,draft=True)]*100).encode()
                return json.dumps([self.release]).encode()
            return self.get(url)
        result=build(source,get)
        self.assertEqual(len(result['packages']['com.example.tool']['versions']),1)

if __name__=='__main__':unittest.main()
