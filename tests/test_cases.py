TEST_CASES = [
    # ----------------------------------------------------------------------------
    # 1. Only valid JSON in the input string (should return True)
    # ----------------------------------------------------------------------------
    (
        "Single valid JSON object",
        '{"name": "Alice", "age": 30}',
        True
    ),
    (
        "Single valid JSON array",
        '[1, 2, 3, 4]',
        True
    ),
    (
        "Nested valid JSON object",
        '{"outer": {"inner": {"key": "value"}}}',
        True
    ),

    # ----------------------------------------------------------------------------
    # 2. Valid JSON in the response, between JSON blocks ```json ... ```
    #    (should return True)
    # ----------------------------------------------------------------------------
    (
        "JSON code block at the end",
        'Some explanation text.\n```json\n{"valid": true}\n```\n',
        True
    ),
    (
        "JSON code block at the start",
        '```json\n{"list": [1, 2, 3]}\n```\nAdditional notes afterward.',
        True
    ),
    (
        "Multiple code blocks, only one is JSON",
        'Here is some text.\n```python\nprint("Hello")\n```\nBut here is JSON:\n```json\n{"msg": "hello"}\n```\n',
        True
    ),

    # ----------------------------------------------------------------------------
    # 3. Additional text at beginning or end, no json blocks, but there is valid
    #    JSON somewhere in the input string (should return True)
    # ----------------------------------------------------------------------------
    (
        "JSON embedded in sentence",
        'Before text { "key": "value" } after text',
        True
    ),
    (
        "Array embedded in sentence",
        'Some prefix text [10, 20, 30] some suffix text.',
        True
    ),
    (
        "Nested JSON embedded",
        'Check out this structure: {"outer": {"inner": 42}}. Pretty cool!',
        True
    ),

    # ----------------------------------------------------------------------------
    # 4. No valid JSON in input string (should return False)
    # ----------------------------------------------------------------------------
    (
        "No JSON at all",
        'This string has no JSON.',
        False
    ),
    (
        "Malformed braces",
        'Not quite JSON { some text without quotes }',
        False
    ),
    (
        "Code block but not JSON",
        '```json\nfunction test() { return 42; }\n```\nNo valid JSON here.',
        False
    ),
    # 1. Valid JSON with escaped quotes
    (
        "Valid JSON object with escaped quotes inside string",
        '{"text": "He said \\"Hello\\" today"}',
        True
    ),
    # 2. Valid JSON with multiline formatting inside a code block
    (
        "Multiline JSON code block",
        'Here is some text:\n```json\n{\n  "user": "Bob",\n  "score": 42,\n  "achievements": ["medal1", "medal2"]\n}\n```',
        True
    ),
    # 3. Text + valid JSON + text
    (
        "Text around valid JSON object",
        'Leading text, then {"id": 101, "valid": true}, then trailing text.',
        True
    ),
    # 4. Multiple JSON code blocks - both valid
    (
        "Multiple JSON code blocks, all valid",
        '```json\n{"block": 1}\n```\nSome filler.\n```json\n{"block": 2}\n```',
        True
    ),
    # 5. Looks like JSON but single quotes for object keys/values
    (
        "Invalid JSON using single quotes instead of double quotes",
        "{'name': 'SingleQuotes', 'valid': false}",
        False
    ),
    # 6. Partial valid JSON in the first code block, second code block fully valid
    (
        "First code block invalid, second code block valid",
        '```json\n{"incomplete": "data"\n```\nOops!\n```json\n{"complete": true}\n```',
        True
    ),
    # 7. Trailing comma in JSON
    (
        "Trailing comma in JSON object",
        '{"item1": "value1", "item2": "value2",}',
        False
    ),
    # 8. Triple backtick block without "json" label but still valid JSON
    (
        "Unlabeled code block with valid JSON",
        '``` \n{\n  "unlabeled": true,\n  "data": [1, 2, 3]\n}\n```',
        True
    ),
    # 9. No code block, just whitespace and valid JSON
    (
        "Lots of whitespace, then valid JSON",
        '       \n   {"key": "value"}    \n',
        True
    ),
    # 10. Empty string
    (
        "Empty string should have no valid JSON",
        "",
        False
    ),
]

FIX_TEST_CASES = [
    # --------------------------------------------------------------------------
    # Category 1: Input string is valid JSON (expected_result = True)
    # --------------------------------------------------------------------------
    (
        "Valid JSON object",
        '{"name": "Alice", "age": 30}',
        True
    ),
    (
        "Valid JSON array",
        '[1, 2, 3]',
        True
    ),
    (
        "Nested JSON",
        '{"outer": {"inner": [10, 20, "thirty"]}}',
        True
    ),
    (
        "Valid JSON with escaped quotes",
        '{"quote": "He said \\"Hello!\\""}',
        True
    ),

    # --------------------------------------------------------------------------
    # Category 2: Input string is slightly off from valid JSON (expected_result = True)
    # --------------------------------------------------------------------------
    (
        "Single quotes instead of double quotes",
        "{'key': 'value', 'number': 123}",
        True
    ),
    (
        "Trailing comma in object",
        '{"key1": "val1", "key2": "val2",}',
        True
    ),
    (
        "Missing quotes around key",
        '{name: "Bob", "score": 42}',
        True
    ),
    (
        "Extra bracket at the end",
        '{"a": 1, "b": 2}]}',
        True
    ),

    # --------------------------------------------------------------------------
    # Category 3: Input string is very off from valid JSON (expected_result = False)
    # --------------------------------------------------------------------------
    (
        "Random text with some braces",
        "Hello {something} not valid JSON!",
        False
    ),
    (
        "Random brackets and text",
        "{this is not JSON though, [just some text]",
        False
    ),
    (
        "Mismatched braces and brackets",
        '{"validPart": {"x": 1], "y": 2',
        False
    ),
    (
        "Keys but no structure",
        'key1: "val1" key2: "val2"',
        False
    ),

    # --------------------------------------------------------------------------
    # Category 4: Input string has no JSON whatsoever (expected_result = False)
    # --------------------------------------------------------------------------
    (
        "Completely empty string",
        "",
        False
    ),
    (
        "Just plain text",
        "No curly braces, no brackets, no quotes - just text.",
        False
    ),
    
    # ----------------------
    # Category 5: Edge Cases
    # ----------------------
    (
        "Weird but valid JSON with unusual tokens in strings",
        '{\n  "special": "value with triple backticks ``` here",\n  "nested": {\n    "inner_key": "some text with <|END|> token"\n  }\n}',
        True
    ),
    (
        "LLM-style comment in JSON object",
        '{\n  "someKey": "someValue",  // A comment from the LLM\n  "anotherKey": "whatever"\n}',
        True
    ),
    (
        "Broken JSON with missing syntax and stray text",
        'Sure! Here\'s your JSON:\n{\n   "foo": "bar"\n   "stuff"   // Missing colon, value, and a comma\n}',
        False
    ),
    (
        "No JSON, only a pseudo-code snippet",
        "Sure, here's some pseudo-code:\n```python\nprint('Hello World')\n```\nEnd of snippet.",
        False
    ),
]
