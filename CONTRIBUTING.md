# Contributing to Finnish Social Services Schema API

Thank you for your interest in contributing to this project! This guide outlines how to contribute effectively.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sosmeta.git
   cd sosmeta
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Setup

### Running Locally
```bash
python server_example.py
```

### Running with Docker
```bash
docker-compose up --build
```

### Testing
```bash
# Test API endpoints
curl http://localhost:5000/api/v1/schemas
curl http://localhost:5000/health

# Run validation tests
python -m pytest tests/ -v
```

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Include detailed description and steps to reproduce
- Provide relevant logs and error messages

### Feature Requests
- Open an issue with detailed description
- Explain the use case and expected behavior
- Discuss implementation approach

### Code Contributions

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**:
   ```bash
   python -m pytest
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: description of your changes"
   ```

5. **Push and create pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Guidelines

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Maximum line length: 88 characters

### API Design
- RESTful endpoints
- Consistent error responses
- Proper HTTP status codes
- OpenAPI 3.1 compliance

### Documentation
- Update README.md for new features
- Add API documentation
- Include usage examples

## Schema Updates

### Adding New Schemas
1. Place JSON schema files in `Valmis/` directory
2. Follow OID naming convention: `1.2.246.537.6.{category}.{subcategory}.{date}.json`
3. Ensure schemas include proper `sosmeta` metadata
4. Test schema loading and validation

### Schema Validation
```bash
# Validate schema format
python validate_schemas.py Valmis/

# Test specific schema
python test_schema.py 1.2.246.537.6.1506.1000.2023.9.8
```

## Testing

### Unit Tests
```bash
python -m pytest tests/unit/ -v
```

### Integration Tests
```bash
python -m pytest tests/integration/ -v
```

### API Tests
```bash
python -m pytest tests/api/ -v
```

## Documentation

### API Documentation
- Update OpenAPI schema in `sosmeta-openai-action.json`
- Test with OpenAPI validators
- Generate documentation with tools like Swagger UI

### README Updates
- Keep feature list current
- Update examples for new functionality
- Maintain accurate setup instructions

## Security

### Reporting Security Issues
- **Do not** create public issues for security vulnerabilities
- Email security issues to: [security contact]
- Include detailed description and steps to reproduce

### Security Guidelines
- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all input parameters
- Implement proper authentication

## Release Process

### Version Numbering
- Follow Semantic Versioning (SemVer)
- Format: `MAJOR.MINOR.PATCH`
- Update version in relevant files

### Creating Releases
1. Update version numbers
2. Update CHANGELOG.md
3. Create GitHub release with tag
4. Include release notes

## Community

### Communication
- GitHub Discussions for questions
- Issues for bugs and features
- Pull requests for code changes

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers get started

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing:
- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing! 🙏
