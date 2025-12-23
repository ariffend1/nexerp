#!/usr/bin/env python3
"""
Comprehensive fix script for all backend import and duplicate table issues
"""
import os
import re
from pathlib import Path

BACKEND_DIR = Path("C:/Users/it/Project-AgenCoding/erp/backend")
MODELS_DIR = BACKEND_DIR / "app" / "models"

# SQLAlchemy types to check for
SQLALCHEMY_TYPES = {
    'Integer': r'\bColumn\s*\(\s*Integer\b',
    'Boolean': r'\bColumn\s*\(\s*Boolean\b',
    'Text': r'\bColumn\s*\(\s*Text\b',
    'Float': r'\bColumn\s*\(\s*Float\b',
    'Numeric': r'\bColumn\s*\(\s*Numeric\b',
    'Date': r'\bColumn\s*\(\s*Date\b',
}

def fix_sqlalchemy_imports(filepath):
    """Add missing SQLAlchemy type imports"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find existing sqlalchemy import
    import_match = re.search(r'from sqlalchemy import ([^\n]+)', content)
    if not import_match:
        return False
    
    existing_imports = [imp.strip() for imp in import_match.group(1).split(',')]
    
    # Find needed types
    needed = set()
    for type_name, pattern in SQLALCHEMY_TYPES.items():
        if re.search(pattern, content):
            needed.add(type_name)
    
    # Add missing
    missing = needed - set(existing_imports)
    if not missing:
        return False
    
    # Update import line
    all_imports = sorted(set(existing_imports) | missing)
    new_line = f"from sqlalchemy import {', '.join(all_imports)}"
    
    updated = content.replace(import_match.group(0), new_line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)
    
    print(f"✓ {filepath.name}: added {', '.join(sorted(missing))}")
    return True

# Fix all model files
print("=" * 60)
print("FIXING SQLALCHEMY IMPORTS")
print("=" * 60)

fixed_count = 0
for py_file in MODELS_DIR.glob("*.py"):
    if py_file.name != "__init__.py":
        if fix_sqlalchemy_imports(py_file):
            fixed_count += 1

print(f"\nTotal files fixed: {fixed_count}")
print("\nDone!")
