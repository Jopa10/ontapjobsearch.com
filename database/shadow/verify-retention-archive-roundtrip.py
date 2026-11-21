"""Recover all simulated adverts from the uploaded/downloaded evidence archive."""
import gzip,hashlib,json
from pathlib import Path
root=Path('retention-evidence')
report=json.loads((root/'retention-test-report.json').read_text())
manifest=json.loads((root/'retention-archive-manifest.json').read_text())
assert report['status']=='passed' and report['testCount']==4
assert report['actualPayloadsPurged']==0 and report['existingPublicationUnchanged']
assert manifest['fixturesOnly'] is True and len(manifest['archives'])==2
versions=[]
for item in manifest['archives']:
 packed=(root/'retention-archives'/item['key']).read_bytes()
 assert hashlib.sha256(packed).hexdigest()==item['compressedSha256']
 envelope=json.loads(gzip.decompress(packed))
 assert envelope['publicId']==item['publicId']
 assert envelope['versionSha256']==item['versionSha256']
 payload=json.dumps(envelope['payload'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
 assert hashlib.sha256(payload).hexdigest()==item['versionSha256']
 versions.append(envelope)
assert versions[0]['publicId']==versions[1]['publicId']
assert versions[0]['versionSha256']!=versions[1]['versionSha256']
assert not versions[0]['payload']['/Job/Position'].endswith('[simulated later advert revision]')
assert versions[1]['payload']['/Job/Position'].endswith('[simulated later advert revision]')
result={'status':'passed','downloadedArchiveVersionsVerified':2,'originalAndLaterVersionDistinguished':True,'fixtureArchivesOnly':True,'productionPurgeEnabled':False}
(root/'archive-roundtrip-report.json').write_text(json.dumps(result,indent=2)+'\n')
print('ONTAP_RETENTION_ARCHIVE_ROUNDTRIP '+json.dumps(result))
