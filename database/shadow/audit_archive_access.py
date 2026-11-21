#!/usr/bin/env python3
"""Read-only AWS archive audit. Never retrieves credentials or modifies resources.

Run in an already authenticated AWS environment. Output is metadata only.
"""
import argparse
import json
from datetime import date

BUCKET = 'ontap-jobg8-archive-179402568934-eu-west-2-an'
ROLE = 'arn:aws:iam::179402568934:role/OntapJobG8ArchiveGitHubRole'


def audit(s3, sts, iam, days):
    results = {'bucket': BUCKET, 'region_expected': 'eu-west-2',
               'mode': 'read-only', 'checks': {},
               'limitations': [
                   'No write was attempted: immutable PutObject and remote archive roundtrip remain unproved.',
                   'IAM simulation alone does not prove effective access under bucket policies, SCPs, KMS or retention constraints.',
                   'Expiration from object creation is not 90 days after advert inactivity; active lifespan must also be covered.',
                   'CloudShell caller permissions differ from the GitHub OIDC role; inspect both results.',
               ]}

    def check(name, fn):
        try:
            results['checks'][name] = {'status': 'read', 'result': fn()}
        except Exception as exc:
            response = getattr(exc, 'response', {})
            results['checks'][name] = {'status': 'unverified', 'error_code': response.get('Error', {}).get('Code', type(exc).__name__)}

    check('caller', lambda: {k: v for k, v in sts.get_caller_identity().items() if k != 'ResponseMetadata'})
    check('location', lambda: s3.get_bucket_location(Bucket=BUCKET).get('LocationConstraint'))
    check('lifecycle', lambda: s3.get_bucket_lifecycle_configuration(Bucket=BUCKET).get('Rules', []))
    check('versioning', lambda: {k: v for k,v in s3.get_bucket_versioning(Bucket=BUCKET).items() if k != 'ResponseMetadata'})
    check('object_lock', lambda: s3.get_object_lock_configuration(Bucket=BUCKET).get('ObjectLockConfiguration'))
    check('encryption', lambda: s3.get_bucket_encryption(Bucket=BUCKET).get('ServerSideEncryptionConfiguration'))
    check('github_role_trust', lambda: iam.get_role(RoleName=ROLE.rsplit('/',1)[-1])['Role']['AssumeRolePolicyDocument'])
    resource = f'arn:aws:s3:::{BUCKET}/ontap-shadow/display-v1/read-only-policy-simulation/object.json.gz'
    check('github_role_object_policy_simulation', lambda: [
        {'action': x['EvalActionName'], 'decision': x['EvalDecision'], 'missing_context': x.get('MissingContextValues', [])}
        for x in iam.simulate_principal_policy(PolicySourceArn=ROLE,
            ActionNames=['s3:GetObject', 's3:PutObject'], ResourceArns=[resource]).get('EvaluationResults', [])])
    for day in days:
        key = f'jobg8/raw/{day}.zip'
        def metadata(key=key):
            obj = s3.head_object(Bucket=BUCKET, Key=key)
            return {k: obj[k] for k in ['ContentLength','LastModified','Expiration','VersionId','ServerSideEncryption','ObjectLockMode','ObjectLockRetainUntilDate'] if k in obj}
        def read_probe(key=key):
            obj = s3.get_object(Bucket=BUCKET, Key=key, Range='bytes=0-0')
            try:
                return {'bytes_read': len(obj['Body'].read(1)), 'payload_logged': False}
            finally:
                obj['Body'].close()
        check('raw_head_' + day, metadata)
        check('raw_get_' + day, read_probe)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', action='append', default=[], help='Existing raw feed date; may repeat')
    args = parser.parse_args()
    days = args.date or ['2026-11-02', '2026-11-03']
    for day in days:
        if date.fromisoformat(day).isoformat() != day:
            parser.error('Use ISO calendar dates')
    import boto3
    result = audit(boto3.client('s3',region_name='eu-west-2'), boto3.client('sts',region_name='eu-west-2'), boto3.client('iam'), days)
    print(json.dumps(result, default=str, indent=2))


if __name__ == '__main__':
    main()
