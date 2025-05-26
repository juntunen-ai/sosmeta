"""
Finnish Social Services Schema API Server
Implementation example for the OpenAI action
"""

from flask import Flask, request, jsonify
import json
import os
import glob
from jsonschema import Draft7Validator
from datetime import datetime
from functools import wraps
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=os.getenv("CORS_ORIGINS", "*"))
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s: %(message)s"
)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per hour"])

# Load all schemas on startup
SCHEMAS_DIR = "./Valmis"
schemas_cache = {}
metadata_cache = {}

def require_api_key(f):
    """Require Authorization header with Bearer token matching API_KEY"""
    @wraps(f)
    def decorated(*args, **kwargs):
        expected = os.getenv("API_KEY")
        token = request.headers.get("Authorization", "")
        if not expected or token != f"Bearer {expected}":
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated

@app.before_request
def log_request():
    app.logger.info(f"{request.method} {request.path} from {request.remote_addr}")
def load_schemas():
    """Load all schemas from the Valmis directory"""
    schema_files = glob.glob(f"{SCHEMAS_DIR}/*.json")
    
    for file_path in schema_files:
        filename = os.path.basename(file_path)
        oid = filename.replace('.json', '')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)
            schemas_cache[oid] = schema_data
            
            # Extract metadata
            sosmeta = schema_data.get('sosmeta', {})
            metadata_cache[oid] = {
                'oid': oid,
                'title': sosmeta.get('title', ''),
                'documentType': sosmeta.get('documentType', ''),
                'documentSubject': sosmeta.get('documentSubject', ''),
                'documentAuthor': sosmeta.get('documentAuthor', ''),
                'status': sosmeta.get('status', ''),
                'documentDefinitionVersion': sosmeta.get('documentDefinitionVersion', ''),
                'dataComponentLibraryVersion': sosmeta.get('dataComponentLibraryVersion', '')
            }

# Load schemas on startup
load_schemas()

@app.route('/api/v1/schemas', methods=['GET'])
@require_api_key
@limiter.limit("100 per minute")
def list_schemas():
    """List all available schemas with filtering"""
    document_type = request.args.get('documentType')
    document_subject = request.args.get('documentSubject')
    
    filtered_schemas = []
    
    for oid, metadata in metadata_cache.items():
        # Apply filters
        if document_type and metadata['documentType'] != document_type:
            continue
        if document_subject and metadata['documentSubject'] != document_subject:
            continue
            
        filtered_schemas.append(metadata)
    
    return jsonify({
        'schemas': filtered_schemas,
        'total': len(filtered_schemas)
    })

@app.route('/api/v1/schemas/<oid>', methods=['GET'])
@require_api_key
@limiter.limit("100 per minute")
def get_schema(oid):
    """Get specific schema by OID"""
    if oid not in schemas_cache:
        return jsonify({'error': 'Schema not found'}), 404
    
    schema = schemas_cache[oid]
    metadata = metadata_cache[oid]
    
    # Generate summary
    summary = analyze_schema_structure(schema)
    
    return jsonify({
        'metadata': metadata,
        'schema': schema,
        'summary': summary
    })

@app.route('/api/v1/validate', methods=['POST'])
@require_api_key
@limiter.limit("50 per minute")
def validate_document():
    """Validate a document against a schema"""
    data = request.get_json()
    schema_oid = data.get('schemaOid')
    document = data.get('document')
    
    if schema_oid not in schemas_cache:
        return jsonify({'error': 'Schema not found'}), 404
    
    schema = schemas_cache[schema_oid]
    
    # Perform validation
    validator = Draft7Validator(schema)
    errors = []
    warnings = []
    
    for error in validator.iter_errors(document):
        errors.append({
            'path': '.'.join(str(x) for x in error.absolute_path),
            'message': error.message,
            'field': error.absolute_path[-1] if error.absolute_path else 'root'
        })
    
    # Calculate completeness
    completeness = calculate_completeness(document, schema)
    
    return jsonify({
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'summary': {
            'totalErrors': len(errors),
            'totalWarnings': len(warnings),
            'completeness': completeness
        }
    })

@app.route('/api/v1/generate-template', methods=['POST'])
@require_api_key
@limiter.limit("20 per minute")
def generate_template():
    """Generate a document template from a schema"""
    data = request.get_json()
    schema_oid = data.get('schemaOid')
    include_optional = data.get('includeOptional', False)
    language = data.get('language', 'fi')
    
    if schema_oid not in schemas_cache:
        return jsonify({'error': 'Schema not found'}), 404
    
    schema = schemas_cache[schema_oid]
    
    # Generate template
    template = generate_document_template(schema, include_optional)
    instructions = extract_field_instructions(schema, language)
    
    return jsonify({
        'template': template,
        'instructions': instructions
    })

@app.route('/api/v1/search', methods=['GET'])
@require_api_key
@limiter.limit("100 per minute")
def search_schemas():
    """Search schemas by title, description, or field names"""
    query = request.args.get('q', '').lower()
    language = request.args.get('language', 'fi')
    
    if len(query) < 2:
        return jsonify({'error': 'Query too short'}), 400
    
    results = []
    
    for oid, metadata in metadata_cache.items():
        score = 0
        matched_fields = []
        
        # Search in title
        if query in metadata['title'].lower():
            score += 3
            matched_fields.append('title')
        
        # Search in document type
        if query in metadata['documentType'].lower():
            score += 2
            matched_fields.append('documentType')
        
        # Search in subject
        if query in metadata['documentSubject'].lower():
            score += 2
            matched_fields.append('documentSubject')
        
        # Search in schema fields (simplified)
        schema = schemas_cache[oid]
        if search_in_schema_fields(schema, query, language):
            score += 1
            matched_fields.append('fields')
        
        if score > 0:
            results.append({
                'oid': oid,
                'title': metadata['title'],
                'documentType': metadata['documentType'],
                'documentSubject': metadata['documentSubject'],
                'relevanceScore': score / 8,  # Normalize to 0-1
                'matchedFields': matched_fields
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x['relevanceScore'], reverse=True)
    
    return jsonify({
        'results': results,
        'total': len(results)
    })

@app.route('/api/v1/assistant/help', methods=['POST'])
@require_api_key
@limiter.limit("10 per minute")
def get_document_assistance():
    """Get AI assistance for document creation"""
    data = request.get_json()
    question = data.get('question', '')
    context = data.get('context', {})
    
    # This would integrate with an AI service
    # For now, return a structured response based on keywords
    
    response_text = generate_assistance_response(question, context)
    suggested_schemas = find_relevant_schemas(question, context)
    next_steps = generate_next_steps(question, context)
    examples = generate_examples(question, context)
    
    return jsonify({
        'response': response_text,
        'suggestedSchemas': suggested_schemas,
        'nextSteps': next_steps,
        'examples': examples
    })

# Helper functions

def analyze_schema_structure(schema):
    """Analyze schema structure to generate summary"""
    required_fields = []
    optional_fields = []
    field_count = 0
    
    def extract_fields(obj, path=""):
        nonlocal field_count
        if isinstance(obj, dict):
            if 'properties' in obj:
                field_count += len(obj['properties'])
                required = obj.get('required', [])
                for field_name, field_def in obj['properties'].items():
                    full_path = f"{path}.{field_name}" if path else field_name
                    if field_name in required:
                        required_fields.append(full_path)
                    else:
                        optional_fields.append(full_path)
                    extract_fields(field_def, full_path)
            elif 'items' in obj:
                extract_fields(obj['items'], path)
    
    extract_fields(schema)
    
    return {
        'requiredFields': required_fields[:10],  # Limit for API response
        'optionalFields': optional_fields[:10],
        'fieldCount': field_count
    }

def calculate_completeness(document, schema):
    """Calculate document completeness percentage"""
    # Simplified calculation - would need more sophisticated logic
    return 85.0  # Placeholder

def generate_document_template(schema, include_optional=False):
    """Generate a template document structure"""
    def create_template(schema_part):
        if schema_part.get('type') == 'object':
            template = {}
            properties = schema_part.get('properties', {})
            required = schema_part.get('required', [])
            
            for prop_name, prop_def in properties.items():
                if prop_name in required or include_optional:
                    if prop_def.get('type') == 'string':
                        template[prop_name] = f"[{prop_name}]"
                    elif prop_def.get('type') == 'array':
                        template[prop_name] = [create_template(prop_def.get('items', {}))]
                    elif prop_def.get('type') == 'object':
                        template[prop_name] = create_template(prop_def)
                    else:
                        template[prop_name] = None
            return template
        return None
    
    return create_template(schema)

def extract_field_instructions(schema, language='fi'):
    """Extract field instructions and descriptions"""
    required_fields = []
    optional_fields = []
    
    def extract_instructions(obj, path=""):
        if isinstance(obj, dict):
            if 'properties' in obj:
                required = obj.get('required', [])
                for field_name, field_def in obj['properties'].items():
                    sosmeta = field_def.get('sosmeta', {})
                    names = sosmeta.get('name', [])
                    descriptions = sosmeta.get('description', [])
                    
                    # Get localized name and description
                    name = field_name
                    description = ""
                    
                    for name_entry in names:
                        if name_entry.get('lang') == language:
                            name = name_entry.get('value', field_name)
                            break
                    
                    for desc_entry in descriptions:
                        if desc_entry.get('lang') == language:
                            description = desc_entry.get('value', "")
                            break
                    
                    field_info = {
                        'field': field_name,
                        'description': description,
                        'type': field_def.get('type', 'unknown'),
                        'example': f"Example {name}"
                    }
                    
                    if field_name in required:
                        required_fields.append(field_info)
                    else:
                        optional_fields.append(field_info)
                    
                    # Recurse into nested objects
                    extract_instructions(field_def, f"{path}.{field_name}" if path else field_name)
    
    extract_instructions(schema)
    
    return {
        'requiredFields': required_fields,
        'optionalFields': optional_fields
    }

def search_in_schema_fields(schema, query, language):
    """Search for query in schema field names and descriptions"""
    # Simplified search - would need more sophisticated implementation
    schema_str = json.dumps(schema).lower()
    return query in schema_str

def generate_assistance_response(question, context):
    """Generate AI assistance response (placeholder)"""
    # This would integrate with OpenAI API or similar
    return f"Based on your question about '{question}', I can help you create the appropriate Finnish social services document."

def find_relevant_schemas(question, context):
    """Find schemas relevant to the user's question"""
    # Simple keyword matching - would be more sophisticated in practice
    relevant = []
    question_lower = question.lower()
    
    keywords = {
        'elderly': ['1.2.246.537.6.1506.1000.2023.9.8'],
        'child': ['1.2.246.537.6.1506.11000.2023.9.8'],
        'assessment': ['1.2.246.537.6.1506.1000.2023.9.8'],
        'plan': ['1.2.246.537.6.1506.11001.2023.9.8']
    }
    
    for keyword, oids in keywords.items():
        if keyword in question_lower:
            for oid in oids:
                if oid in metadata_cache:
                    relevant.append(metadata_cache[oid])
    
    return relevant[:5]  # Limit results

def generate_next_steps(question, context):
    """Generate suggested next steps"""
    return [
        "1. Select the appropriate schema for your document type",
        "2. Generate a template to get started",
        "3. Fill in required fields first",
        "4. Validate your document before submission"
    ]

def generate_examples(question, context):
    """Generate relevant examples"""
    return [
        {
            "description": "Example elderly service assessment",
            "example": {
                "iakkaiden_palvelutarpeen_arvio": {
                    "asiakas": [{
                        "sukunimi": "Virtanen",
                        "etunimet": "Aino Maria",
                        "henkilotunnus": "010250-123A"
                    }]
                }
            }
        }
    ]


@app.route('/health', methods=['GET'])
@require_api_key
@limiter.limit("60 per minute")
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'schemas_loaded': len(schemas_cache),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
