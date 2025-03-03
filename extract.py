import json
import re

def extract(input_string):
    """
    Extract valid JSON from an input string.
    
    Args:
        input_string (str): The input string containing potential JSON.
    
    Returns:
        tuple: (json_data, success)
            - json_data: The parsed JSON data if successful, None otherwise.
            - success: Boolean indicating whether valid JSON was found.
    """
    # Try to parse the entire string as JSON first
    try:
        json_data = json.loads(input_string)
        return json_data, True
    except json.JSONDecodeError:
        pass
    
    # Look for JSON blocks between ```json and ``` markers
    json_block_pattern = r'```json\s*([\s\S]*?)\s*```'
    json_blocks = re.findall(json_block_pattern, input_string)
    
    for block in json_blocks:
        try:
            json_data = json.loads(block)
            return json_data, True
        except json.JSONDecodeError:
            continue
    
    # Find the largest valid JSON object or array in the string
    # Try different starting positions to find any valid JSON
    for i in range(len(input_string)):
        # Check for opening braces or brackets
        if input_string[i] in ['{', '[']:
            # Try to find the matching closing brace/bracket
            stack = [input_string[i]]
            for j in range(i + 1, len(input_string)):
                if input_string[j] in ['{', '[']:
                    stack.append(input_string[j])
                elif input_string[j] == '}' and stack[-1] == '{':
                    stack.pop()
                elif input_string[j] == ']' and stack[-1] == '[':
                    stack.pop()
                
                if not stack:
                    potential_json = input_string[i:j+1]
                    try:
                        json_data = json.loads(potential_json)
                        return json_data, True
                    except json.JSONDecodeError:
                        break  # Invalid JSON, continue with next starting position
    
    # No valid JSON found
    return None, False