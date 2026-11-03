#!/usr/bin/env python3
"""Explicit S3 transport probe: one synthetic display archive; no DB/policy/delete calls.
CloudShell permissions prove only that caller, not the main-only GitHub role.
"""
import argparse
import base64
import gzip
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

BUCKET = 'ontap-jobg8-archive-179402568934-eu-west-2-an'
OWNER = '179402568934'
FIXTURE = {'receipt': {'version': 1, 'key': 'ontap-shadow/display-v1/22222222-2222-5222-8222-222222222222/ea880d24c110812dd67361eca072de5a47d5ff2e05f0f3a675c6304269d48f9a.json.gz', 'sha256': 'ea880d24c110812dd67361eca072de5a47d5ff2e05f0f3a675c6304269d48f9a', 'bytes': 922, 'runId': '22222222-2222-5222-8222-222222222222', 'feedDate': '2026-11-03', 'selectionStateSha256': '66439a8b55bdf8017d3601feabbc193c9be3ec872b0fea2d8cb1b844018f2085', 'outputsSha256': '0b60bc5b549ca4ad95e6a73862104d6874fffd32eb9b2b9fa519ced933aa26c7'}, 'base64': 'H4sIAAAAAAACA82W227bOBCGXyWY2ypYnU+LvUjcHOzETX1obacIjBE1shnLokJSju3C776Q3Dhd7BbYrbdA/guCJEbDj8MRh19hRVJxUUBsGSCrop1CDPY3nTaNVzfhy/BFYEBGlL5HTfUXpu2fWtap6YABSjeTX0FSKaSue7RGpi95TneVLiv9ESXXG4i1rMiAqlgU4rlQEJs1Q06qTyu+pwL8lwIDULI5X9FgjrbnQwzZkQIDRIOrDi7NxDcT5iWeGzF0MY088jFwQt+2TDf1w8DNsix1bEqixE6iDD0rYpRGjoNo+ywAA1hOWPSJCZkqiK2dAUwUmtZNnBTlxLSQPxcASTOuNMlX3uRIgQEzEjOJ5XxzcMqOFDRbzviskqi5KA6O0yNV5x4TJfWbOMhXYjpSYIDmS2q9HBQMJh+G1xfDdutk4JxoiYWqM/2klCKhE1Hkm99PCtGM04rVe6y7KyqwYAQ7A5SoJKNrVHNSEH/5Agcfp40PMMA8UvDwYEBKrMmjepH6f8wg/oelmqBBDK+4MaZLXkwVyRVntcmLI4iBFyyvUmryDVUzNdgUek6as+9ikfG1rmRtNtvfEQejb5m6p4IhKQ0PO+M/4bFKabEkOVWYk/orH63/T76fJ9vHblr/3cj0lFGhJb0l1Iw3+ThFxkRV6DcVxrmcSmKy4npJhX5LZDnNMJ+iUlxpLPS0RInN3FuCXKJckObF7C1BqaqsTabPQi5I/lqyh50BKVdljpu6rn7/ymEiJQYxzLa8PE1Qke/+mkq/L+Z1gasfRAfPvu86EYaJ5yVpFppWkDq+aWWEScKsyGFRQg6xMLATMyO005AlVhK6rmmFmW2GHhhQ4iYXWD/Vrl3VPturdbYdd3s92eqen1+5WF2McHXvrUurs75ZBqMzjv32cuWP5tGdz8270fvHgA235qq7EsuK9TtO/ny/efQcus/6684i7W2fzNE6+fx0NflUzduzhXf1KK4+XfQ6YdefJ/zmrjceL6X8DVud6zN8/DAaqOR2O+5Ierwtnrz1pDJJVdfOOy/rnCOet4fddPuuezscf7ya+Bc18x91McSyJJT1VaT+flZVoZueOhxMwJAlqW37AVqmZ7kJ+anpWmYYIIsCZme2awdkZZj5zI8Clnme6/mWx1iWOWYKP8qAHwTV1aMbnt9sW6ratMInc2CKzSK6+TwRl2eXcrWa9Ia1Iex2fwK9bSe9TQsAAA==', 'packetSha256': 'ec4d6b895c97781118416cfb133eee50696d45c2b5140d1fd0c461a7e173dd6f'}
EXPECTED_RULES = [{'Expiration': {'Days': 93}, 'ID': 'Delete JobG8 archive after 93 days',
                   'Filter': {'Prefix': 'jobg8/raw/'}, 'Status': 'Enabled'}]


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def validate(data):
    receipt = FIXTURE['receipt']
    if len(data) != receipt['bytes'] or hashlib.sha256(data).hexdigest() != receipt['sha256']:
        raise ValueError('Archive size/checksum mismatch')
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        decoded = stream.read(1024 * 1024 + 1)
    if len(decoded) > 1024 * 1024:
        raise ValueError('Oversized probe packet')
    packet = json.loads(decoded)
    if canonical_hash(packet) != FIXTURE['packetSha256']:
        raise ValueError('Recovered packet differs')
    if packet['runId'] != receipt['runId'] or packet['feedDate'] != receipt['feedDate']:
        raise ValueError('Recovered identity differs')
    return packet


class S3ArchiveStore:
    """Conditional creation plus exact verification on both create and replay.
    No unconditional writes, deletes, permissions or policy mutations exist here.
    """
    def __init__(self, s3):
        self.s3 = s3

    def get(self, key):
        obj = self.s3.get_object(Bucket=BUCKET, ExpectedBucketOwner=OWNER, Key=key)
        try:
            if obj.get('ContentLength', 0) > 1024 * 1024:
                raise ValueError('Oversized probe object')
            data = obj['Body'].read(1024 * 1024 + 1)
        finally:
            obj['Body'].close()
        if len(data) > 1024 * 1024 or obj.get('Expiration'):
            raise ValueError('Oversized or lifecycle-expiring probe object')
        validate(data)
        return data

    def put_if_absent(self, key, data):
        # Narrow allowlist: this executable may write ONLY its pinned test key.
        if key != FIXTURE['receipt']['key']:
            raise ValueError('Unapproved probe key')
        validate(data)
        digest = base64.b64encode(hashlib.sha256(data).digest()).decode()
        created = True
        try:
            result = self.s3.put_object(Bucket=BUCKET, ExpectedBucketOwner=OWNER,
                Key=key, Body=data, IfNoneMatch='*', ChecksumSHA256=digest,
                ServerSideEncryption='AES256', ContentType='application/gzip',
                Metadata={'purpose': 'synthetic-shadow-archive-transport-probe',
                          'sha256': FIXTURE['receipt']['sha256']})
            if result.get('ChecksumSHA256') != digest:
                raise ValueError('S3 did not confirm upload checksum')
        except Exception as exc:
            response = getattr(exc, 'response', {})
            if (response.get('Error', {}).get('Code') not in ('PreconditionFailed', '412')
                    or response.get('ResponseMetadata', {}).get('HTTPStatusCode') != 412):
                raise
            created = False
        if self.get(key) != data:
            raise ValueError('Exact readback differs')
        return created


def execute(s3, caller):
    if caller.get('Account') != OWNER:
        raise ValueError('Wrong AWS account; no upload attempted')
    location = s3.get_bucket_location(Bucket=BUCKET, ExpectedBucketOwner=OWNER)
    if location.get('LocationConstraint') != 'eu-west-2':
        raise ValueError('Wrong bucket region')
    config = s3.get_bucket_lifecycle_configuration(Bucket=BUCKET, ExpectedBucketOwner=OWNER)
    if config.get('Rules') != EXPECTED_RULES:
        raise ValueError('Lifecycle differs from saved applied policy; no upload attempted')
    data = base64.b64decode(FIXTURE['base64'], validate=True)
    packet = validate(data)
    key = FIXTURE['receipt']['key']
    store = S3ArchiveStore(s3)
    created = store.put_if_absent(key, data)
    # A second REAL conditional PutObject must receive 412. Unexpected success
    # is reported as failure, never represented as immutability proof.
    if store.put_if_absent(key, data):
        raise ValueError('Repeat conditional write was not rejected')
    recovered = store.get(key)
    if validate(recovered) != packet:
        raise ValueError('Standalone recovery differs')
    return {'testedAt': datetime.now(timezone.utc).isoformat(), 'status': 'passed',
        'bucket': BUCKET, 'region': 'eu-west-2', 'callerArn': caller.get('Arn'),
        'archive': FIXTURE['receipt'], 'createdOnThisInvocation': created,
        'conditionalRepeatRejected': True, 'exactByteRecovery': True,
        'exactPacketRecovery': True, 'lifecycleExcludesArchive': True,
        'syntheticTransportFixture': True, 'fullSnapshotS3RecoveryProven': False,
        'githubRoleWriteProven': False, 'objectLockProven': False,
        'databaseChanged': False, 'cleanupExecuted': False,
        'productionChanged': False,
        'limitations': 'Caller-specific transport proof only. No Object Lock or policy-enforced immutability; unconditional privileged overwrites remain possible. Full real archive/provenance and inactive raw-advert retention remain pending.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='ontap-archive-transport-result.json')
    args = parser.parse_args()
    import boto3
    caller = boto3.client('sts', region_name='eu-west-2').get_caller_identity()
    result = execute(boto3.client('s3', region_name='eu-west-2'), caller)
    # Save before displaying, so CloudShell interruptions retain the receipt.
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
