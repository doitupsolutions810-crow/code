import express from 'express';
import OpenApiValidator from 'express-openapi-validator';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export async function createApp() {
  const app = express();
  app.use(express.json({ limit: '1mb' }));
  app.use(OpenApiValidator.middleware({
    apiSpec: path.join(__dirname, '../api/openapi.yaml'),
    validateRequests: true,
    validateResponses: true,
  }));
  app.get('/health', (_req, res) => res.json({ status: 'ok' }));
  app.post('/v1/artifacts', (req, res) => res.status(202).json({ status: 'pending-verification', artifact: req.body.ref }));
  app.post('/v1/deploy', (req, res) => res.status(202).json({ status: 'verification-required', agent_id: req.body.agent_id }));
  app.get('/v1/attestations', (_req, res) => res.json({ items: [] }));
  app.use((error, _req, res, _next) => res.status(error.status || 500).json({ error: error.message }));
  return app;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const port = Number(process.env.PORT || 8080);
  (await createApp()).listen(port, '0.0.0.0', () => console.log(`SACP control plane listening on ${port}`));
}
