import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import pg from 'pg';

const expectedRole = 'ontap_prod_readonly_probe';
const maxDatabaseBytes = 1024 ** 3;
const connectionString = process.env.ONTAP_NEON_PROD_READONLY_URL;

function safeFailure(code) {
  console.error('ONTAP_PROD_NEON_READONLY_CHECK_FAILED', code);
  process.exitCode = 1;
}

if (!connectionString) {
  safeFailure('missing_readonly_connection');
} else {
  let url;
  try {
    url = new URL(connectionString);
  } catch {
    safeFailure('invalid_connection_format');
  }

  if (url) {
    if (!url.hostname.endsWith('.neon.tech')) safeFailure('unexpected_database_host');
    if (!['require', 'verify-full'].includes(url.searchParams.get('sslmode'))) {
      safeFailure('ssl_required');
    }
    url.searchParams.set('sslmode', 'verify-full');

    const client = new pg.Client({
      connectionString: url.toString(),
      connectionTimeoutMillis: 15000,
      query_timeout: 30000,
      statement_timeout: 15000,
      application_name: 'ontap-neon-prod-readonly-connection-check',
      options: '-c default_transaction_read_only=on',
    });

    let connected = false;
    try {
      await client.connect();
      connected = true;
      await client.query('BEGIN READ ONLY');

      const identity = (await client.query(
        'SELECT current_database() AS database_name, current_user AS role_name, pg_database_size(current_database())::text AS database_bytes'
      )).rows[0];
      assert.equal(identity.role_name, expectedRole, 'Unexpected read-only role');

      const role = (await client.query(
        'SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles WHERE rolname = current_user'
      )).rows[0];
      assert.ok(role, 'Read-only role is missing');
      assert.equal(role.rolsuper, false);
      assert.equal(role.rolcreatedb, false);
      assert.equal(role.rolcreaterole, false);
      assert.equal(role.rolreplication, false);

      const privileges = (await client.query(
        "SELECT has_database_privilege(current_user, current_database(), 'CREATE') AS can_create_in_database"
      )).rows[0];
      assert.equal(privileges.can_create_in_database, false);

      const schema = (await client.query(
        "SELECT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'ontap_shadow') AS exists, " +
        "count(*)::int AS table_count FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace " +
        "WHERE n.nspname = 'ontap_shadow' AND c.relkind IN ('r','p','v','m','f')"
      )).rows[0];

      const databaseBytes = Number(identity.database_bytes);
      assert.ok(Number.isSafeInteger(databaseBytes) && databaseBytes >= 0);
      assert.ok(databaseBytes < maxDatabaseBytes, 'Database is at or above the 1 GB ceiling');
      assert.equal(schema.table_count, 0, 'Production shadow schema is not empty; stop before any write');

      await client.query('ROLLBACK');
      connected = false;

      const report = {
        status: 'passed',
        projectLabel: 'ontap-production (connection supplied from this Neon project)',
        databaseName: identity.database_name,
        endpointHost: url.hostname,
        roleName: identity.role_name,
        tls: true,
        roleIsNonPrivileged: true,
        databaseCreatePrivilege: false,
        shadowSchemaExists: schema.exists,
        shadowSchemaTableCount: schema.table_count,
        databaseBytes,
        databaseGiB: Number((databaseBytes / (1024 ** 3)).toFixed(6)),
        neonOneGiBCeilingBytes: maxDatabaseBytes,
        writesPerformed: false,
        productionSiteDeployed: false,
      };
      const reportJson = JSON.stringify(report, null, 2) + '\n';
      if (process.env.RUNNER_TEMP) {
        await fs.writeFile(`${process.env.RUNNER_TEMP}/production-readonly-check-report.json`, reportJson);
      }
      console.log('ONTAP_PROD_NEON_READONLY_CHECK', JSON.stringify(report));
    } catch (error) {
      if (connected) {
        try { await client.query('ROLLBACK'); } catch {}
      }
      safeFailure(error?.code || (error instanceof assert.AssertionError ? 'preflight_assertion_failed' : 'connection_or_read_check_failed'));
    } finally {
      try { await client.end(); } catch {}
    }
  }
}
