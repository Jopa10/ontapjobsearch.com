import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

test('a city page does not hide LIVE regional inventory; an established static slice still owns its data', async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ontap-slice-collision-'));
  const previous = process.cwd();
  const write = (relative: string, value: string) => {
    const target = path.join(root, relative);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, value);
  };
  try {
    write('pipeline/config/job_slice_catalog.json', JSON.stringify({
      categories: { admin_service: { route_slug: 'service-administrator-jobs', display_label: 'Admin', output_dir: 'output-admin-service', file_suffix: 'admin-service', category_label: 'Admin' } },
      regions: { Glasgow: { slug: 'glasgow', anchor_town: 'Glasgow' }, London: { slug: 'london', anchor_town: 'London' }, Empty: { slug: 'empty', anchor_town: 'Empty' }, Inactive: { slug: 'inactive', anchor_town: 'Inactive' } },
    }));
    write('pipeline/registers/region_category_slice_register.csv', 'region,category,status\nGlasgow,admin_service,LIVE\nLondon,admin_service,LIVE\nEmpty,admin_service,LIVE\nInactive,admin_service,ASSESS\n');
    for (const slug of ['glasgow', 'london', 'empty', 'inactive']) {
      write(`app/_city-pages/configured-slices/${slug}/service-administrator-jobs.json`, slug === 'empty' ? '[]' : '[{"job_id":"approved"}]');
    }
    write('app/glasgow/service-administrator-jobs/page.tsx', '// derived city page');
    write('app/london/service-administrator-jobs/page.tsx', '// established regional page');
    write('app/london/service-administrator-jobs.json', '[{"job_id":"static"}]');
    process.chdir(root);
    const { getPublishedDynamicSlices } = await import('../lib/configured-job-slices');
    const slices = getPublishedDynamicSlices();
    assert.deepEqual(slices.map(slice => slice.regionSlug), ['glasgow']);
    assert.equal(slices[0].route, '/job-search/glasgow/service-administrator-jobs');
  } finally {
    process.chdir(previous);
    fs.rmSync(root, { recursive: true, force: true });
  }
});
