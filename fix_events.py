import re

with open('ml_pipeline/event_generator.py', 'r') as f:
    code = f.read()

# Update base_event signature
code = code.replace(
    'global_visitor_id=None\n):',
    'global_visitor_id=None,\n    confidence=0.95\n):'
)

code = code.replace(
    '"confidence": 0.95,',
    '"confidence": float(confidence),'
)

def repl_def(match):
    return match.group(1) + ',\n    confidence=0.95\n):'
code = re.sub(r'([ \t]*global_visitor_id=None[ \t]*\n)\):', repl_def, code)

def repl_def2(match):
    if 'global_visitor_id' not in match.group(0):
        return match.group(1) + ',\n    confidence=0.95\n):'
    return match.group(0)
code = re.sub(r'([ \t]*camera_id[ \t]*\n)\):', repl_def2, code)

def repl_call(match):
    args = match.group(1)
    if 'confidence' in args: return match.group(0)
    return 'base_event(' + args + ',\n        confidence=confidence\n    )'

code = re.sub(r'base_event\((.*?)\n    \)', repl_call, code, flags=re.DOTALL)

with open('ml_pipeline/event_generator.py', 'w') as f:
    f.write(code)
