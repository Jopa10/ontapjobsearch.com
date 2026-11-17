import subprocess,json,re,html,os
from pathlib import Path
cli=os.environ['VERCEL_CLI'];url='https://ontapjobsearch-a45l04pus-ontap1.vercel.app'
out=Path(os.environ['RUNNER_TEMP'])/'routes';out.mkdir()
def fetch(path,label):
    p=subprocess.run([cli,'curl',path,'--deployment',url,'--scope','ontap1','--','-i','--max-time','90'],text=True,capture_output=True)
    (out/(label+'.http')).write_text(p.stdout)
    assert p.returncode==0,(path,p.stderr[-500:])
    statuses=re.findall(r'HTTP/[0-9.]+\s+(\d+)',p.stdout)
    assert statuses and statuses[-1]=='200',(path,statuses,p.stdout[:300])
    assert re.search(r'x-robots-tag:\s*noindex',p.stdout,re.I),(path,'missing Preview noindex')
    return p.stdout
results=[]
home=fetch('/','homepage')
for path,label in [('/','homepage'),('/north-east/service-administrator-jobs','region'),('/newcastle/service-administrator-jobs','city'),('/newcastle','broad-city')]:
    text=home if path=='/' else fetch(path,label)
    assert '<h1' in text,(path,'no server HTML h1')
    assert 'canonical' in text,(path,'no canonical')
    results.append({'path':path,'status':200,'serverHtml':True,'canonicalPresent':True,'previewNoindex':True})
jobs=re.findall(r'href="(/jobs/[^"#?]+)"',home)
assert jobs,'No job detail links in rendered homepage'
job=html.unescape(jobs[0])
text=fetch(job,'job')
assert 'application/ld+json' in text and 'JobPosting' in text,'Missing JobPosting SSR structured data'
assert 'canonical' in text
results.append({'path':job,'status':200,'jobPostingStructuredData':True,'canonicalPresent':True,'previewNoindex':True})
site=fetch('/sitemap.xml','sitemap')
assert '<urlset' in site and 'https://www.ontapjobsearch.com/' in site
results.append({'path':'/sitemap.xml','status':200,'productionCanonicalUrls':True,'previewNoindex':True})
report={'status':'passed','previewUrl':url,'checks':results,'productionChanged':False,'applyLinksFollowed':False}
(out/'route-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('ONTAP_PREVIEW_ROUTES '+json.dumps(report))
