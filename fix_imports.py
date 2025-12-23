#!/usr/bin/env python3
"""
Script to fix missing SQLAlchemy imports in model files
"""
import os
import re

# Define the backend models directory
MODELS_DIR = "C:/Users/it/Project-AgenCoding/erp/backend/app/models"

# Common SQLAlchemy types that might be missing
SQLALCHEMY_TYPES = ['Integer', 'Boolean', 'Text', 'Float', 'Numeric', 'Date']

def fix_imports_in_file(filepath):
    """Fix missing SQLAlchemy imports in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find existing sqlalchemy import line
    import_match = re.search(r'from sqlalchemy import (.+)', content)
    if not import_match:
        return False
    
    existing_imports = [imp.strip() for imp in import_match.group(1).split(',')]
    
    # Find which types are used in the file
    needed_types = set()
    for sql_type in SQLALCHEMY_TYPES:
        if re.search(rf'\bColumn\s*\(\s*{sql_type}\b', content):
            needed_types.add(sql_type)
    
    # Add missing imports
    missing = needed_types - set(existing_imports)
    if not missing:
        return False
    
    # Update the import line
    new_imports = existing_imports + list(missing)
    new_import_line = f"from sqlalchemy import {', '.join(sorted(new_imports))}"
    
    updated_content = content.replace(import_match.group(0), new_import_line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Fixed {filepath}: added {', '.join(missing)}")
    return True

# Process all Python files in models directory
fixed_count = 0
for filename in os.listdir(MODELS_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(MODELS_DIR, filename)
        if fix_imports_in_file(filepath):
            fixed_count += 1

print(f"\nTotal files fixed: {fixed_count}")
