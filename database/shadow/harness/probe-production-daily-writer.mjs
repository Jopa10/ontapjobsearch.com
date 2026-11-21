import assert from 'node:assert/strict';
import pg from 'pg';

const expected = {
  host: 'ep-green-sunset-zaycl73a-pooler.c-2.eu-west-2.aws.neon.tech',
  database: 'neondb',
  role: 'ontap_prod_daily_writer',
};
const input = process.env.ONTAP_NEON_PROD_DAILY_WRITE_URL;
assert.ok(input, 'Production writer secret is unavailable to this workflow');

const url = new URL(input);
assert.equal(url.hostname, expected.host, 'Unexpected Neon endpoint');
assert.equal(url.pathname.slice(1), expected.database, 'Unexpected database');
assert.equal(decodeURIComponent(url.username), expected.role, 'Unexpected database role');
assert.ok(['require', 'verify-full'].includes(url.searchParams.get('sslmode')), 'TLS is required');
url.searchParams.set('sslmode', 'verify-full');

const client = new pg.Client({
  connectionString: url.toString(),
  connectionTimeoutMillis: 15000,
  query_timeout: 30000,
  statement_timeout: 30000,
  application_name: 'ontap-neon-production-daily-writer-probe',
});

let connected = false;
try {
  await client.connect();
  connected = true;
  const identity = (await client.query(
    'SELECT current_database() AS database, current_user AS role, pg_database_size(current_database())::text AS bytes'
  )).rows[0];
  assert.equal(identity.database, expected.database);
  assert.equal(identity.role, expected.role);
  assert.equal(client.connection?.stream?.encrypted, true, 'TLS is not active');

  const role = (await client.query(
    'SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles WHERE rolname = current_user'
  )).rows[0];
  assert.ok(role, 'Database role was not found');
  for (const attr of ['rolsuper', 'rolcreatedb', 'rolcreaterole', 'rolreplication']) {
    assert.equal(role[attr], false, 'Unexpected elevated role attribute: ' + attr);
  }

  assert.equal((await client.query(
    "SELECT has_schema_privilege(current_user, 'ontap_shadow', 'USAGE') AS allowed"
  )).rows[0].allowed, true);

  const tables = [
    'suppliers', 'feed_runs', 'jobs', 'supplier_adverts', 'advert_appearances',
    'selection_decisions', 'daily_publication_scopes', 'daily_refresh_receipts',
  ];
  for (const table of tables) {
    for (const privilege of ['SELECT', 'INSERT', 'UPDATE']) {
      const allowed = (await client.query(
        'SELECT has_table_privilege(current_user, $1, $2) AS allowed',
        ['ontap_shadow.' + table, privilege]
      )).rows[0].allowed;
      assert.equal(allowed, true, 'Missing ' + privilege + ' on ' + table);
    }
  }

  const sequence = (await client.query(
    "SELECT pg_get_serial_sequence('ontap_shadow.suppliers', 'id') AS name"
  )).rows[0].name;
  assert.ok(sequence, 'Suppliers identity sequence was not found');
  assert.equal((await client.query(
    "SELECT has_sequence_privilege(current_user, $1, 'USAGE') AS allowed",
    [sequence]
  )).rows[0].allowed, true, 'Missing supplier identity sequence privilege');

  const result = {
    status: 'passed',
    mode: 'read_only_production_connection_probe',
    endpoint: expected.host,
    database: identity.database,
    role: identity.role,
    tls: true,
    elevatedRoleAttributes: false,
    schemaUsage: true,
    tablePrivilegesChecked: tables.length * 3,
    supplierIdentitySequenceUsage: true,
    databaseBytes: Number(identity.bytes),
    databaseWrites: false,
  };
  console.log('ONTAP_NEON_PRODUCTION_DAILY_WRITER_PROBE ' + JSON.stringify(result));
} catch (error) {
  console.error('Production writer probe failed:', error.code || error.name || 'connection error');
  throw new Error('Production Neon writer connection probe failed');
} finally {
  if (connected) await client.end().catch(() => {});
}
