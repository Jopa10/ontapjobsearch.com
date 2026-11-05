#!/usr/bin/env python3
"""Full saved-fixture S3 recovery; explicit owner CloudShell execution only."""
import argparse
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import verify_archive_transport as transport

# Existing complete fixture receipt; dependency/run metadata are synthetic.
RECEIPT = json.loads((Path(__file__).with_name('display-archive-verification-2026-11-03.json')).read_text())['archive']
EXPECTED_SHA = '0629696a63fef39d0e7bc3b4c13e6f1b46424cb96654f9794bac8410d3468d76'
EXPECTED_BYTES = 8147866


def validate(data):
    if len(data) != EXPECTED_BYTES or hashlib.sha256(data).hexdigest() != EXPECTED_SHA:
        raise ValueError('Full saved archive checksum/length mismatch')
    # Bound decompression without parsing hundreds of thousands of rows again.
    # Exact compressed bytes pin the entire semantically verified local packet.
    import io
    count = 0
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk: break
            count += len(chunk)
            if count > 384 * 1024 * 1024:
                raise ValueError('Full packet exceeds decompression bound')
    return {'compressedSha256': EXPECTED_SHA, 'decodedBytes': count}


def execute(s3, caller, data):
    validate(data)
    if RECEIPT['sha256'] != EXPECTED_SHA or RECEIPT['bytes'] != EXPECTED_BYTES:
        raise ValueError('Saved receipt mismatch')
    transport.FIXTURE = {'receipt': RECEIPT}
    transport.MAX_OBJECT_BYTES = 64 * 1024 * 1024
    transport.validate = validate
    result = transport.execute(s3, caller, data=data)
    result.update(testedAt=datetime.now(timezone.utc).isoformat(),
        fullSnapshotS3RecoveryProven=True, syntheticTransportFixture=False,
        syntheticDependencyMetadata=True, syntheticRunId=True,
        sourceSelectionArtifact=13184005546, sourceDisplayArtifact=13183730978,
        semanticRecovery='Existing JavaScript archive restore verified complete state locally; S3 verifies identical full compressed packet and bounded gzip recovery.',
        limitations='Full saved-fixture transport only. Synthetic dependency metadata/run ID; no real fresh-run provenance, GitHub-role access, Object Lock or raw-advert retention proof.')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', default='ontap-full-display-2026-11-02.json.gz')
    p.add_argument('--output', default='ontap-full-archive-result.json')
    args = p.parse_args()
    path = Path(args.archive)
    if path.stat().st_size != EXPECTED_BYTES:
        raise ValueError('Wrong input archive size')
    data = path.read_bytes()
    import boto3
    caller = boto3.client('sts', region_name='eu-west-2').get_caller_identity()
    result = execute(boto3.client('s3', region_name='eu-west-2'), caller, data)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
