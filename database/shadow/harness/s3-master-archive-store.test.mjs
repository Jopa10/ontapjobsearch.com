import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {createS3MasterArchiveStore} from './s3-master-archive-store.mjs';
class Put{constructor(input){this.input=input;}}
class Get{constructor(input){this.input=input;}}
const bucket='ontap-jobg8-archive-179402568934-eu-west-2-an';
const sha=b=>createHash('sha256').update(b).digest('hex');
const payload=Buffer.from('fixture archive');
const key='ontap-shadow/advert-versions/'+'a'.repeat(8)+'-'+'a'.repeat(4)+'-'+'a'.repeat(4)+'-'+'a'.repeat(4)+'-'+'a'.repeat(12)+'/'+'b'.repeat(64)+'/'+sha(payload)+'.json.gz';
function make(initial=null){
 let saved=initial;const commands=[];
 const client={send:async command=>{
  commands.push(command);
  if(command instanceof Put){
   assert.equal(command.input.IfNoneMatch,'*');
   if(saved){const e=new Error('exists');e.$metadata={httpStatusCode:412};throw e;}
   saved=Buffer.from(command.input.Body);return {};
  }
  if(!saved)throw new Error('NoSuchKey');
  return {ContentLength:saved.length,VersionId:'fixture-object-version',Body:{transformToByteArray:async()=>saved}};
 }};
 return {store:createS3MasterArchiveStore({client,PutObjectCommand:Put,GetObjectCommand:Get,bucket}),commands};
}
test('conditional archive put verifies owner encryption checksum and fresh readback',async()=>{
 const {store,commands}=make();
 const r=await store.putIfAbsent(key,payload);
 assert.equal(r.durable,true);assert.equal(r.sha256,sha(payload));assert.equal(r.versionId,'fixture-object-version');
 const p=commands[0].input;assert.equal(p.ExpectedBucketOwner,'179402568934');assert.equal(p.ServerSideEncryption,'AES256');assert.ok(p.ChecksumSHA256);
 assert.deepEqual(await store.get(key),payload);
});
test('identical existing object is reusable and never overwritten',async()=>{
 const {store,commands}=make(payload);
 assert.equal((await store.putIfAbsent(key,payload)).durable,true);
 assert.equal(commands.filter(x=>x instanceof Put).length,1);
});
test('different existing object blocks reuse without a second write',async()=>{
 const {store,commands}=make(Buffer.from('corrupt existing archive'));
 await assert.rejects(store.putIfAbsent(key,payload));
 assert.equal(commands.filter(x=>x instanceof Put).length,1);
});
test('archive paths outside the approved version prefix are rejected',async()=>{
 const {store,commands}=make();
 await assert.rejects(store.putIfAbsent('jobg8/raw/fixture.zip',payload));
 assert.equal(commands.length,0);
});
