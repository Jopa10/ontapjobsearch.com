import base64
import copy
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import verify_archive_transport as m

class PreconditionFailed(Exception):
    response = {'Error': {'Code': 'PreconditionFailed'}, 'ResponseMetadata': {'HTTPStatusCode': 412}}

class FakeS3:
    def __init__(self):
        self.rules = copy.deepcopy(m.EXPECTED_RULES)
        self.data = None
        self.writes = 0
        self.corrupt = False
    def get_bucket_location(self, **kwargs):
        return {'LocationConstraint': 'eu-west-2'}
    def get_bucket_lifecycle_configuration(self, **kwargs):
        return {'Rules': self.rules}
    def put_object(self, **kwargs):
        assert kwargs['IfNoneMatch'] == '*'
        assert kwargs['ExpectedBucketOwner'] == m.OWNER
        assert kwargs['Key'] == m.FIXTURE['receipt']['key']
        self.writes += 1
        if self.data is not None:
            raise PreconditionFailed()
        self.data = kwargs['Body']
        return {'ChecksumSHA256': kwargs['ChecksumSHA256']}
    def get_object(self, **kwargs):
        data = b'corrupt' if self.corrupt else self.data
        return {'ContentLength': len(data), 'Body': io.BytesIO(data)}

class Tests(unittest.TestCase):
    def test_create_repeat_recovery_and_second_invocation(self):
        s3 = FakeS3()
        result = m.execute(s3, {'Account': m.OWNER, 'Arn': 'test'})
        self.assertTrue(result['createdOnThisInvocation'])
        self.assertTrue(result['conditionalRepeatRejected'])
        self.assertFalse(result['fullSnapshotS3RecoveryProven'])
        self.assertFalse(m.execute(s3, {'Account': m.OWNER})['createdOnThisInvocation'])
        self.assertEqual(s3.writes, 4)
    def test_account_and_policy_guards_write_nothing(self):
        s3 = FakeS3()
        with self.assertRaises(ValueError): m.execute(s3, {'Account': 'wrong'})
        s3.rules[0]['Filter'] = {}
        with self.assertRaises(ValueError): m.execute(s3, {'Account': m.OWNER})
        self.assertEqual(s3.writes, 0)
    def test_corrupt_readback_and_wrong_key_rejected(self):
        s3 = FakeS3(); s3.corrupt = True
        with self.assertRaises(ValueError): m.execute(s3, {'Account': m.OWNER})
        with self.assertRaises(ValueError):
            m.S3ArchiveStore(s3).put_if_absent('outside', base64.b64decode(m.FIXTURE['base64']))
    def test_unexpected_errors_not_treated_as_existing_object(self):
        s3 = FakeS3()
        def denied(**kwargs): raise PermissionError('denied')
        s3.put_object = denied
        with self.assertRaises(PermissionError): m.execute(s3, {'Account': m.OWNER})

if __name__ == '__main__': unittest.main()
