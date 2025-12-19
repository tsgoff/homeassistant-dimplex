# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of this Home Assistant integration seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

1. **DO NOT** open a public issue
2. Send a private email to: mail@andreas-kurtz.de
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: We aim to release a patch within 30 days for confirmed vulnerabilities

### Disclosure Policy

- We follow responsible disclosure practices
- Security fixes will be released as patch versions
- Credit will be given to reporters (unless anonymity is requested)

## Security Best Practices for Users

### Credential Storage

- Credentials are stored in Home Assistant's encrypted configuration
- Never share your `refresh_token` publicly
- Use strong, unique passwords for your Dimplex account

### Network Security

- This integration communicates with Dimplex Cloud API over HTTPS
- No local network access to your heat pump required
- OAuth2 tokens are automatically refreshed

### Updates

- Keep this integration up to date
- Enable Dependabot alerts (if you fork this repo)
- Monitor the GitHub repository for security advisories

## Known Security Considerations

### OAuth2 Flow
- Uses Azure AD B2C authentication
- Client ID is public (as per OAuth2 PKCE specification for public clients)
- `client_secret` is intentionally empty (standard for mobile/public clients)

### API Communication
- All API calls use HTTPS/TLS
- Tokens have limited lifetime (typically 1 hour)
- Automatic token refresh with retry logic

### Data Privacy
- No telemetry or analytics collected by this integration
- All data stays between Home Assistant and Dimplex Cloud
- See [Dimplex Privacy Policy](https://www.dimplex.de/datenschutz) for cloud data handling

## Security Features

✅ Automatic token expiry and refresh
✅ Secure credential storage via Home Assistant
✅ HTTPS-only API communication
✅ No hardcoded credentials
✅ Proper error handling (no credential leaks in logs)
✅ Dependencies: minimal (only `aiohttp`)

## Contact

For security concerns, contact: mail@andreas-kurtz.de
