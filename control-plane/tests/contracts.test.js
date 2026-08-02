import test from 'node:test';
import assert from 'node:assert/strict';
import request from 'supertest';
import { createApp } from '../src/server.js';

async function app() { return createApp(); }

test('health response conforms to contract', async () => {
  const response = await request(await app()).get('/health');
  assert.equal(response.status, 200);
  assert.deepEqual(response.body, { status: 'ok' });
});

test('valid artifact registration is accepted', async () => {
  const ref = `ghcr.io/acme/model@sha256:${'a'.repeat(64)}`;
  const response = await request(await app()).post('/v1/artifacts').send({ ref });
  assert.equal(response.status, 202);
  assert.equal(response.body.artifact, ref);
});

test('empty artifact registration is rejected', async () => {
  const response = await request(await app()).post('/v1/artifacts').send({ ref: '' });
  assert.equal(response.status, 400);
});

test('valid deploy is accepted', async () => {
  const response = await request(await app()).post('/v1/deploy').send({
    artifact: { ref: `ghcr.io/acme/a@sha256:${'a'.repeat(64)}` },
    agent_id: 'agent-1',
    command: ['true'],
  });
  assert.equal(response.status, 202);
});

test('invalid deploy is rejected', async () => {
  const response = await request(await app()).post('/v1/deploy').send({ artifact: {}, agent_id: '?' });
  assert.equal(response.status, 400);
});

test('attestation list response conforms to contract', async () => {
  const response = await request(await app()).get('/v1/attestations');
  assert.equal(response.status, 200);
  assert.deepEqual(response.body, { items: [] });
});
