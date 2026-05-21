# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainers at **security@example.com** with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
3. Allow up to **72 hours** for an initial response
4. A fix will be developed and released before public disclosure

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x (current) | Yes |

## Security Architecture

### Authentication

- **JWT-based authentication** with signed tokens
- Passwords hashed with **bcrypt** (cost factor 12)
- Token expiration enforced (configurable, default 30 minutes)
- Refresh token rotation supported

### Authorization

- **Role-Based Access Control (RBAC)** with three roles:
  - `viewer` — read-only dashboard access
  - `analyst` — create/update incidents, run playbooks, manage alerts
  - `admin` — full access including user management, audit logs, rule reload
- Endpoint-level permission checks via dependency injection

### Input Validation

- All request bodies validated via **Pydantic** schemas
- SQL injection mitigated by **SQLAlchemy ORM** (parameterized queries)
- Path and query parameters type-checked by FastAPI

### Rate Limiting

- API rate limiting via Redis-backed middleware
- Per-user and per-endpoint rate limits configurable

### Audit Logging

- All state-changing operations recorded in the **AuditEntry** table
- Captures: actor, action, entity, before/after state, IP address, timestamp
- Audit entries are append-only (immutable)

### Container Security

- Backend runs as **non-root user** (`soc`) in production containers
- Multi-stage frontend build (build dependencies not shipped to production)
- No secrets baked into images — environment variables used at runtime
- Health checks enabled for all services

### Network

- Frontend proxies API calls through Nginx (no direct backend exposure in production)
- Internal service communication over Docker network (not exposed to host where possible)

## Known Limitations

This is a **demonstration/portfolio project** with synthetic data. The following limitations apply:

- Default credentials (`admin`/`admin123`) are included for demo purposes — **change in production**
- The `SECRET_KEY` in `docker-compose.yml` is a placeholder — **rotate before deployment**
- IOC enrichment uses mock/simulated data, not live threat intel feeds
- SOAR playbook actions are simulated (no actual cloud API integrations)
- No TLS/HTTPS configured by default — use a reverse proxy with TLS in production
- No CSRF protection (API-only backend with JWT auth)
- Session management relies on JWT expiration only (no server-side revocation list)

## Security Checklist for Production Deployment

- [ ] Change default admin credentials
- [ ] Set a strong, unique `SECRET_KEY`
- [ ] Enable TLS/HTTPS via reverse proxy
- [ ] Restrict database port exposure (remove host port binding)
- [ ] Configure proper CORS origins
- [ ] Set up log aggregation and monitoring
- [ ] Enable rate limiting
- [ ] Review and restrict RBAC permissions
- [ ] Rotate JWT signing keys periodically
