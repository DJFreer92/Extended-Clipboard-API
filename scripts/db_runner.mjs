#!/usr/bin/env node
/**
 * JSON-over-stdin DB runner using better-sqlcipher3 for SQLCipher encryption.
 *
 * Input JSON schema (stdin):
 * {
 *   op: 'sql' | 'file' | 'exec',
 *   sql?: string,        // for op=sql/exec
 *   file?: string,       // for op=file
 *   params?: any[]|object,
 *   dbPath: string,      // absolute path to DB
 *   key: string          // SQLCipher key
 * }
 *
 * Output JSON schema (stdout):
 * { ok: true, rows?: any[] } | { ok: false, error: string }
 */

import fs from 'node:fs';
import { EOL } from 'node:os';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);

async function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => (data += chunk));
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

function loadDriver() {
  try {
    // Prefer encryption-enabled build if available
    try {
      // eslint-disable-next-line import/no-extraneous-dependencies
      const enc = require('better-sqlite3-multiple-ciphers');
      return { Database: enc, driver: 'mc' };
    } catch (_e) {
      // Fallback to standard better-sqlite3
      // eslint-disable-next-line import/no-extraneous-dependencies
      const lib = require('better-sqlite3');
      return { Database: lib, driver: 'b3' };
    }
  } catch (err) {
    throw new Error('better-sqlite3 is not installed. Run `npm install` in repo root.');
  }
}

function openDb(Database, dbPath, key, driver) {
  const db = new Database(dbPath);
  if (!key || key.length === 0) {
    db.close();
    throw new Error('No encryption key supplied. Set CLIPBOARD_DB_KEY.');
  }
  // Prefer the SQLCipher backend in multi-cipher builds
  try {
    db.pragma('cipher = "sqlcipher"');
  } catch (_) {
    // ignore if not supported
  }
  // Apply SQLCipher key; works with sqlcipher-enabled builds
  // Escape backslashes, double quotes, and single quotes in the key
  const safeKey = key.replace(/\\/g, '\\\\').replace(/"/g, '""').replace(/'/g, "''");
  db.pragma(`key = "${safeKey}"`);
  // Verify key by touching the database and reading cipher_version
  db.pragma('journal_mode = WAL');
  if (driver !== 'mc') {
    let cipherVersion = undefined;
    try { cipherVersion = db.pragma('cipher_version', { simple: true }); } catch (_) {}
    if (!cipherVersion || (Array.isArray(cipherVersion) && cipherVersion.length === 0)) {
      db.close();
      throw new Error('SQLCipher not available. Ensure better-sqlite3 is built against SQLCipher.');
    }
  }
  return db;
}

function run() {
  readStdin()
    .then(raw => {
      const input = JSON.parse(raw || '{}');
  const { op, sql, file, params, dbPath, key } = input;
  const { Database, driver } = loadDriver();
  const db = openDb(Database, dbPath, key, driver);

      try {
        const isSelectLike = (text) => {
          if (!text) return false;
          const t = String(text).trim().toLowerCase();
          return t.startsWith('select') || t.startsWith('with');
        };
        if (op === 'file') {
          const text = fs.readFileSync(file, 'utf8');
          const stmt = db.prepare(text);
          if (isSelectLike(text)) {
            const s = stmt.raw(true);
            const rows = Array.isArray(params) || typeof params === 'object'
              ? s.all(params)
              : s.all();
            return { ok: true, rows };
          } else {
            if (Array.isArray(params) || typeof params === 'object') {
              stmt.run(params);
            } else {
              stmt.run();
            }
            return { ok: true, rows: [] };
          }
        }
        if (op === 'sql') {
          const stmt = db.prepare(sql);
          if (isSelectLike(sql)) {
            const s = stmt.raw(true);
            const rows = Array.isArray(params) || typeof params === 'object'
              ? s.all(params)
              : s.all();
            return { ok: true, rows };
          } else {
            if (Array.isArray(params) || typeof params === 'object') {
              stmt.run(params);
            } else {
              stmt.run();
            }
            return { ok: true, rows: [] };
          }
        }
        if (op === 'exec') {
          db.exec(sql);
          return { ok: true };
        }
        return { ok: false, error: `Unknown op: ${op}` };
      } finally {
        db.close();
      }
    })
    .then(res => {
      process.stdout.write(JSON.stringify(res) + EOL);
    })
    .catch(err => {
      process.stdout.write(JSON.stringify({ ok: false, error: String(err && err.message || err) }) + EOL);
      process.exitCode = 1;
    });
}

run();
