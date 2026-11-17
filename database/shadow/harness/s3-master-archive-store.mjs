// AWS SDK v3 transport is injected by the approved archive runtime.
// Conditional writes: https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const sha=b=>createHash('sha256').update(b).digest('hex');
export function createS3MasterArchiveStore({client,PutObjectCommand,GetObjectCommand,bucket,expectedOwner='179402568934'}){
 assert.equal(bucket,'ontap-jobg8-archive-179402568934-eu-west-2-an');
 assert.equal(expectedOwner,'179402568934');
 function validKey(key){assert.match(key,/^ontap-shadow\/advert-versions\/[a-f0-9-]{36}\/[a-f0-9]{64}\/[a-f0-9]{64}\.json\.gz$/,'Archive key outside approved version prefix');}
 async function read(key){
  validKey(key);
  const result=await client.send(new GetObjectCommand({Bucket:bucket,Key:key,ExpectedBucketOwner:expectedOwner}));
  assert.ok(!result.ContentLength||result.ContentLength<=32*1024*1024);
  const bytes=Buffer.from(await result.Body.transformToByteArray());
  assert.ok(bytes.length<=32*1024*1024);return {bytes,versionId:result.VersionId||null};
 }
 return {provider:'s3-immutable',
  get:async key=>(await read(key)).bytes,
  putIfAbsent:async(key,bytes)=>{
   validKey(key);assert.ok(Buffer.isBuffer(bytes)&&bytes.length<=32*1024*1024);
   const digest=sha(bytes);assert.ok(key.endsWith('/'+digest+'.json.gz'),'Archive key and checksum differ');
   try{
    await client.send(new PutObjectCommand({Bucket:bucket,Key:key,ExpectedBucketOwner:expectedOwner,Body:bytes,IfNoneMatch:'*',ContentType:'application/gzip',ServerSideEncryption:'AES256',ChecksumSHA256:Buffer.from(digest,'hex').toString('base64')}));
   }catch(e){
    if(e.$metadata?.httpStatusCode!==412&&e.name!=='PreconditionFailed')throw e;
   }
   const saved=await read(key);assert.equal(saved.bytes.length,bytes.length);assert.equal(sha(saved.bytes),digest,'Existing S3 archive differs; overwrite forbidden');
   return {provider:'s3-immutable',durable:true,bucket,key,versionId:saved.versionId,sha256:digest};
  }};
}
