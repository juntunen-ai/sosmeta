# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-05-26

### Added
- Initial release of Finnish Social Services Schema API
- OpenAI Action integration for SOSMETA schemas
- Support for 202 Finnish social services document schemas
- Complete OpenAPI 3.1 specification
- RESTful API with the following endpoints:
  - `GET /schemas` - List all available schemas with filtering
  - `GET /schemas/{oid}` - Get specific schema details
  - `POST /validate` - Validate documents against schemas
  - `POST /generate-template` - Generate document templates
  - `GET /search` - Search schemas by keywords
  - `POST /assistant/help` - Get AI assistance for document creation
- Flask server implementation with comprehensive error handling
- Docker and Docker Compose support for easy deployment
- Multilingual support (Finnish and Swedish)
- Authentication and rate limiting
- Health check endpoints
- Comprehensive documentation and deployment guides

### Schema Support
- **Document Types**: 21 different types including Päätös, Suunnitelma, Arvio, etc.
- **Subject Areas**: Coverage of all major Finnish social services domains
- **OID System**: Support for official Finnish registry identifiers
- **Validation**: Full JSON Schema Draft 7 validation
- **Templates**: Auto-generation of document templates with field guidance

### Documentation
- Complete API documentation with examples
- Deployment guide for multiple cloud platforms
- Contributing guidelines
- Setup and configuration instructions
- Security best practices

### Infrastructure
- Production-ready Flask server
- Docker containerization
- Environment-based configuration
- Logging and monitoring setup
- CORS and security headers
- Rate limiting and API key authentication

## [Unreleased]

### Planned
- Enhanced AI assistance features
- Advanced search capabilities
- Schema comparison tools
- Bulk validation endpoints
- Webhook support for schema updates
- Performance optimizations
- Extended language support

---

For detailed information about each change, see the individual commit messages and pull requests.
