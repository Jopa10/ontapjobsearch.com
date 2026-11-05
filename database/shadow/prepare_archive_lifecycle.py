#!/usr/bin/env python3
"""Plan by default; --apply narrows the existing 93-day rule to jobg8/raw/.
Never modifies IAM, objects, encryption, versioning or object lock.
"""
import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
BUCKET='ontap-jobg8-archive-179402568934-eu-west-2-an'
OWNER='179402568934'
EXPECTED={'Rules':[{'Expiration':{'Days':93},'ID':'Delete JobG8 archive after 93 days','Filter':{},'Status':'Enabled'}]}

def proposal(config):
    rules=config.get('Rules')
    if rules != EXPECTED['Rules']:
        raise ValueError('Live lifecycle differs from audited single 93-day rule; stop for review')
    result=copy.deepcopy(EXPECTED)
    result['Rules'][0]['Filter']={'Prefix':'jobg8/raw/'}
    return result

def check_prefixes(s3):
    # Fail closed if narrowing the global rule would affect unrelated content.
    for prefix,allowed in [('',{'jobg8/','ontap-shadow/'}),('jobg8/',{'jobg8/raw/'})]:
        pages=s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET,ExpectedBucketOwner=OWNER,Prefix=prefix,Delimiter='/')
        for page in pages:
            unknown={x['Prefix'] for x in page.get('CommonPrefixes',[])}-allowed
            loose=[x['Key'] for x in page.get('Contents',[]) if x['Key']!=prefix]
            if unknown or loose:
                raise ValueError('Unrelated bucket keys/prefixes present; stop for review')

def execute(s3,apply=False,backup_dir=Path('.')):
    before=s3.get_bucket_lifecycle_configuration(Bucket=BUCKET,ExpectedBucketOwner=OWNER)
    proposed=proposal(before);check_prefixes(s3)
    report={'bucket':BUCKET,'before':{'Rules':before['Rules']},'proposed':proposed,'applied':False,
      'effect':'Raw JobG8 expiry remains 93 days. ontap-shadow/ has no automatic expiry until a separate verified inactivity-based cleanup policy exists.',
      'limits':'Does not provide Object Lock/immutability or verify GitHub write access. Future archive storage continues accumulating; monitor usage. No object deletion is performed.'}
    if apply:
        backup_dir.mkdir(parents=True,exist_ok=True)
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup=backup_dir/('ontap-lifecycle-before-'+stamp+'.json')
        backup.write_text(json.dumps(report['before'],indent=2)+'\n')
        s3.put_bucket_lifecycle_configuration(Bucket=BUCKET,ExpectedBucketOwner=OWNER,LifecycleConfiguration=proposed)
        after=s3.get_bucket_lifecycle_configuration(Bucket=BUCKET,ExpectedBucketOwner=OWNER)
        if after.get('Rules')!=proposed['Rules']:
            raise RuntimeError('Lifecycle readback differs; inspect bucket; no automatic rollback attempted')
        report.update(applied=True,readback_verified=True,backup_file=str(backup))
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');args=p.parse_args()
    import boto3
    print(json.dumps(execute(boto3.client('s3',region_name='eu-west-2'),args.apply),indent=2))
if __name__=='__main__':main()
