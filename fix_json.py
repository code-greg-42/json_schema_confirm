import json
import re

def fix_json(input_string):
    """
    Attempts to fix malformed JSON in an input string.
    
    Args:
        input_string (str): String containing potentially malformed JSON
        
    Returns:
        tuple: (corrected_json, success)
            - corrected_json: The parsed JSON data if successful, None otherwise
            - success: Boolean indicating whether JSON was fixed successfully
    """
    # Case 1: Check if it's already valid JSON
    try:
        json_data = json.loads(input_string)
        return json_data, True
    except json.JSONDecodeError:
        pass
    
    # Pre-check: Validate if the string has some JSON-like structure
    has_braces = '{' in input_string and '}' in input_string
    has_brackets = '[' in input_string and ']' in input_string
    has_quotes = '"' in input_string or "'" in input_string
    
    # If no JSON-like structure at all, return failure
    if not (has_braces or has_brackets) or not has_quotes:
        return None, False
        
    try:
        # Remove comments (both // and /* */ style)
        cleaned = re.sub(r'//.*?(\n|$)', '', input_string)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        
        # Fix missing quotes around keys
        cleaned = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', cleaned)
        
        # Convert single quotes to double quotes
        cleaned = re.sub(r'\'([^\']*)\'', r'"\1"', cleaned)
        
        # Remove trailing commas
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        
        # Try to balance braces and brackets
        stack = []
        balanced = []
        
        for char in cleaned:
            if char in ['{', '[']:
                stack.append(char)
                balanced.append(char)
            elif char == '}':
                if stack and stack[-1] == '{':
                    stack.pop()
                    balanced.append(char)
                elif not stack:  # Extra closing brace, ignore
                    pass
                else:  # Mismatched closing brace
                    closing = '}' if stack[-1] == '{' else ']'
                    stack.pop()
                    balanced.append(closing)
            elif char == ']':
                if stack and stack[-1] == '[':
                    stack.pop()
                    balanced.append(char)
                elif not stack:  # Extra closing bracket, ignore
                    pass
                else:  # Mismatched closing bracket
                    closing = '}' if stack[-1] == '{' else ']'
                    stack.pop()
                    balanced.append(closing)
            else:
                balanced.append(char)
        
        # Close any unclosed braces/brackets
        while stack:
            closer = '}' if stack.pop() == '{' else ']'
            balanced.append(closer)
        
        fixed = ''.join(balanced)
        
        # Try parsing the fixed JSON
        try:
            json_data = json.loads(fixed)
            return json_data, True
        except json.JSONDecodeError:
            # If still not valid, try to extract any valid JSON subset
            for i in range(len(input_string)):
                if input_string[i] in ['{', '[']:
                    for j in range(len(input_string), i, -1):
                        try:
                            subset = input_string[i:j]
                            # Remove comments
                            subset = re.sub(r'//.*?(\n|$)', '', subset)
                            subset = re.sub(r'/\*.*?\*/', '', subset, flags=re.DOTALL)
                            # Replace single quotes
                            subset = subset.replace("'", '"')
                            json_data = json.loads(subset)
                            return json_data, True
                        except json.JSONDecodeError:
                            continue
    except Exception:
        pass
    
    return None, False