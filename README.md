# Finnish Social Services Schema API - OpenAI Action

This OpenAI action provides comprehensive support for working with Finnish social services document schemas (SOSMETA). It enables schema validation, document generation assistance, and metadata extraction for standardized social services documentation.

## Features

### 1. Schema Management
- **List Schemas**: Browse all 202 available schemas with filtering by document type and subject
- **Get Schema Details**: Retrieve complete schema definitions with metadata
- **Search Schemas**: Find relevant schemas using Finnish or Swedish keywords

### 2. Document Validation
- **Validate Documents**: Check JSON documents against specific schemas
- **Error Reporting**: Detailed validation errors with field-level feedback
- **Completeness Analysis**: Track document completion percentage

### 3. Template Generation
- **Document Templates**: Generate structured templates for any schema
- **Field Instructions**: Get detailed field descriptions and examples
- **Multilingual Support**: Templates in Finnish and Swedish

### 4. AI Assistant
- **Document Guidance**: Get help with document creation and understanding
- **Schema Recommendations**: AI-powered schema suggestions based on use case
- **Best Practices**: Expert guidance on Finnish social services documentation

## Usage Examples

### Example 1: Finding the Right Schema
```
User: "I need to create an assessment document for elderly care services"

AI Response: Based on your needs, I recommend the "Iäkkäiden palvelutarpeen arvio" (Elderly Service Needs Assessment) schema:
- OID: 1.2.246.537.6.1506.1000.2023.9.8
- Document Type: Arvio (Assessment)
- Subject: Iäkkäiden palvelujen asiakasasiakirjat
```

### Example 2: Generating a Document Template
```
Request: Generate template for OID 1.2.246.537.6.1506.1000.2023.9.8

Response: Template includes:
- Customer information (required)
- Service needs assessment
- Professional evaluation
- Recommendations
- All fields with Finnish descriptions and validation rules
```

### Example 3: Document Validation
```
Document: { "iakkaiden_palvelutarpeen_arvio": { "asiakas": [...] }}
Schema: 1.2.246.537.6.1506.1000.2023.9.8

Validation Result:
- Valid: true
- Completeness: 85%
- Missing optional fields: 3
- No errors
```

## Schema Categories

### Document Types (202 schemas):
1. **Päätös** (Decision) - 53 schemas
2. **Suunnitelma** (Plan) - 24 schemas
3. **Arvio** (Assessment) - 17 schemas
4. **Ilmoitus** (Notification) - 15 schemas
5. **Asiakaskertomusmerkintä** (Client Record Entry) - 14 schemas
6. **Hakemus** (Application) - 12 schemas
7. **Others** - Various specialized document types

### Subject Areas:
- General social services
- Child protection (foster care, home care, aftercare)
- Disability services
- Elderly services
- Family services
- Adoption counseling
- Violence prevention
- Financial support services

## Implementation Notes

### Data Structure
Each schema contains:
- **JSON Schema v7** definitions
- **SOSMETA metadata** with Finnish/Swedish translations
- **Required/optional** field specifications
- **Validation rules** and constraints
- **Field descriptions** and examples

### Language Support
- **Finnish (fi)**: Primary language
- **Swedish (sv)**: Secondary language
- All field names, descriptions, and validation messages available in both languages

### OID System
Object Identifiers follow the pattern:
- `1.2.246.537.6.1505.*` - Customer/case documents
- `1.2.246.537.6.1506.*` - Service-specific documents
- Date suffix indicates version (YYYY.M.D)

## Authentication & Rate Limits

### API Key Required
All endpoints require valid API authentication.

### Rate Limits
- Schema queries: 100/minute
- Validation requests: 50/minute
- Template generation: 20/minute
- AI assistance: 10/minute

## Error Handling

### Common Error Codes
- `404`: Schema not found
- `400`: Invalid OID format
- `422`: Validation failed
- `429`: Rate limit exceeded
- `500`: Server error

### Validation Errors
Detailed error messages include:
- Field path (JSON pointer)
- Error description
- Suggested corrections
- Related documentation links

## Integration Examples

### ChatGPT Integration
```
"How do I create a child protection plan document?"

AI will:
1. Search relevant schemas
2. Recommend appropriate document type
3. Generate template with guidance
4. Provide completion assistance
```

### API Client Example
```javascript
// Get schema list
const schemas = await api.get('/schemas?documentType=Suunnitelma');

// Generate template
const template = await api.post('/generate-template', {
  schemaOid: 'selected-oid',
  includeOptional: true,
  language: 'fi'
});

// Validate document
const validation = await api.post('/validate', {
  schemaOid: 'selected-oid',
  document: userDocument
});
```

## Benefits

### For Social Workers
- **Standardized Documentation**: Ensure compliance with Finnish regulations
- **Reduced Errors**: Real-time validation and guidance
- **Faster Processing**: Pre-filled templates and smart suggestions
- **Multilingual Support**: Work in Finnish or Swedish

### For Organizations
- **Quality Assurance**: Consistent document standards
- **Compliance**: Meet regulatory requirements
- **Efficiency**: Automated validation and processing
- **Integration**: Easy API integration with existing systems

### For Developers
- **Complete API**: Full CRUD operations for schemas
- **Rich Metadata**: Comprehensive field information
- **Validation Engine**: Built-in JSON Schema validation
- **AI Enhancement**: Natural language assistance

## Support

For technical support, schema questions, or integration assistance:
- Documentation: [API Reference]
- Examples: [GitHub Repository]
- Support: [Contact Information]

---

*This action leverages the official Finnish SOSMETA schema library with 202 standardized document types for comprehensive social services documentation support.*
