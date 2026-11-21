import pg from 'pg';

const expected = {
  host: 'ep-green-sunset-zaycl73a-pooler.c-2.eu-west-2.aws.neon.tech',
  database: 'neondb',
  role: 'ontap_prod_daily_writer',
};

class ProbeCheckError extends Error {
  constructor(check) {
    super(check);
    this.check = check;
  }
}

function requireCheck(condition, check) {
  if (!condition) throw new ProbeCheckError(check);
}

const input = process.env.ONTAP_NEON_PROD_DAILY_WRITE_URL;
requireCheck(Boolean(input), 'GitHub secret is available to the workflow');

let url;
try {
  url = new URL(input);
} catch {
  throw new ProbeCheckError('connection string format');
}

requireCheck(url.hostname === expected.host, 'Neon endpoint host matches Production');
requireCheck(url.pathname.slice(1) === expected.database, 'database name matches Production');
let roleName;
try {
  roleName = decodeURIComponent(url.username);
} catch {
  throw new ProbeCheckError('database role name format');
}
requireCheck(roleName === expected.role, 'database role is the limited daily writer');
requireCheck(
  ['require', 'verify-full'].includes(url.searchParams.get('sslmode')),
  'TLS is required by the connection string',
);
url.searchParams.set('sslmode', 'verify-full');

const client = new pg.Client({
  connectionString: url.toString(),
  connectionTimeoutMillis: 15000,
  query_timeout: 30000,
  statement_timeout: 30000,
  application_name: 'ontap-neon-production-daily-writer-probe',
});

let connected = false;
let stage = 'database connection';
try {
  await client.connect();
  connected = true;

  stage = 'database identity query';
  const identity = (await client.query(
    'SELECT current_database() AS database, current_user AS role, pg_database_size(current_database())::text AS bytes'
  )).rows[0];
  requireCheck(identity.database === expected.database, 'connected database identity');
  requireCheck(identity.role === expected.role, 'connected role identity');
  requireCheck(client.connection?.stream?.encrypted === true, 'TLS is active');

  stage = 'role safety query';
  const role = (await client.query(
    'SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles WHERE rolname = current_user'
  )).rows[0];
  requireCheck(Boolean(role), 'daily writer role exists');
  for (const attr of ['rolsuper', 'rolcreatedb', 'rolcreaterole', 'rolreplication']) {
    requireCheck(role[attr] === false, `role is not elevated (${attr})`);
  }

  stage = 'schema privilege query';
  const schemaUsage = (await client.query(
    "SELECT has_schema_privilege(current_user, 'ontap_shadow', 'USAGE') AS allowed"
  )).rows[0].allowed;
  requireCheck(schemaUsage === true, 'USAGE on ontap_shadow schema');

  const tables = [
    'suppliers', 'feed_runs', 'jobs', 'supplier_adverts', 'advert_appearances',
    'selection_decisions', 'daily_publication_scopes', 'daily_refresh_receipts',
  ];
  for (const table of tables) {
    for (const privilege of ['SELECT', 'INSERT', 'UPDATE']) {
      stage = `table privilege query: ${privilege} on ontap_shadow.${table}`;
      const allowed = (await client.query(
        'SELECT has_table_privilege(current_user, $1, $2) AS allowed',
        ['ontap_shadow.' + table, privilege]
      )).rows[0].allowed;
      requireCheck(allowed === true, `${privilege} on ontap_shadow.${table}`);
    }
  }

  stage = 'supplier identity sequence query';
  const sequence = (await client.query(
    "SELECT pg_get_serial_sequence('ontap_shadow.suppliers', 'id') AS name"
  )).rows[0].name;
  requireCheck(Boolean(sequence), 'suppliers identity sequence exists');
  const sequenceUsage = (await client.query(
    "SELECT has_sequence_privilege(current_user, $1, 'USAGE') AS allowed",
    [sequence]
  )).rows[0].allowed;
  requireCheck(sequenceUsage === true, 'USAGE on suppliers identity sequence');

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
  if (error instanceof ProbeCheckError) {
    console.error('Production writer probe failed at check:', error.check);
  } else {
    console.error('Production writer probe failed during:', stage, error.code || error.name || 'query error');
  }
  throw new Error('Production Neon writer connection probe failed');
} finally {
  if (connected) await client.end().catch(() => {});
}
