import assert from 'node:assert/strict';
import test from 'node:test';
import {
  broadCityDefinitions,
  distanceMiles,
  getBroadCityDefinition,
  getRegionSearchPath,
  isExactCityJob,
  locationCandidates,
} from '../lib/broad-city-pages';

test('registers the forty-one approved permanent broad city routes', () => {
  assert.equal(broadCityDefinitions.length, 41);
  assert.deepEqual(
    broadCityDefinitions.map((city) => city.route),
    [
      "/nottingham/jobs",
      "/wakefield/jobs",
      "/bolton/jobs",
      "/reading/jobs",
      "/chester/jobs",
      "/durham/jobs",
      "/gateshead/jobs",
      "/northallerton/jobs",
      "/norwich/jobs",
      "/salford/jobs",
      "/redditch/jobs",
      "/guildford/jobs",
      "/carlisle/jobs",
      "/preston/jobs",
      "/witney/jobs",
      "/yeovil/jobs",
      "/hertford/jobs",
      "/leatherhead/jobs",
      "/rugby/jobs",
      "/colchester/jobs",
      "/hereford/jobs",
      "/stafford/jobs",
      "/ipswich/jobs",
      "/solihull/jobs",
      "/derby/jobs",
      "/cheltenham/jobs",
      "/bracknell/jobs",
      "/canterbury/jobs",
      "/blackburn/jobs",
      "/corby/jobs",
      "/crewe/jobs",
      "/stevenage/jobs",
      "/chesterfield/jobs",
      "/woking/jobs",
      "/abingdon/jobs",
      "/kings-lynn/jobs",
      "/newport/jobs",
      "/oldham/jobs",
      "/redhill/jobs",
      "/sittingbourne/jobs",
      "/wrexham/jobs"
    ]
  );
  assert.ok(broadCityDefinitions.every((city) => city.lifecycle_state === 'active'));
});

test('matches exact localities conservatively while accepting a trailing hybrid qualifier', () => {
  const nottingham = getBroadCityDefinition('nottingham');
  assert.ok(nottingham);
  assert.equal(isExactCityJob({ location: 'Nottingham' }, nottingham), true);
  assert.equal(isExactCityJob({ location: 'Nottingham (Hybrid Working)' }, nottingham), true);
  assert.equal(isExactCityJob({ location: 'Nottinghamshire' }, nottingham), false);
  assert.deepEqual(locationCandidates('Reading, Berkshire'), ['Reading, Berkshire', 'Reading']);
});

test('regional breadcrumb target preserves the governed region label', () => {
  assert.equal(
    getRegionSearchPath('Greater Manchester - Wigan & Bolton'),
    '/jobs/search?location=Greater%20Manchester%20-%20Wigan%20%26%20Bolton'
  );
});

test('nearby distance enforcement uses a fifteen-mile straight-line ceiling', () => {
  assert.ok(distanceMiles({ latitude: 51.5074, longitude: -0.1278 }, { latitude: 51.5155, longitude: -0.0922 }) < 15);
  assert.ok(distanceMiles({ latitude: 51.5074, longitude: -0.1278 }, { latitude: 51.752, longitude: -1.2577 }) > 15);
});
