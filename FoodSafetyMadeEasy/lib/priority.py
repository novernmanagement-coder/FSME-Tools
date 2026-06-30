# ProctorHub Priority Scoring
# Scoring is internal — never exposed to end users
# Output is simply: High | Medium | Low | Review

# Violation keywords that indicate certification/knowledge gaps
CERT_KEYWORDS = [
    'certified food protection manager',
    'food protection manager',
    'person in charge',
    'pic',
    'no certified',
    'certification',
    'food manager',
    'cfpm',
]

KNOWLEDGE_KEYWORDS = [
    'cooking temperature',
    'cooling',
    'hot holding',
    'cold holding',
    'temperature',
    'cross contaminat',
    'handwash',
    'hand wash',
    'date mark',
    'food safety knowledge',
    'haccp',
]

def score_violations(violation_text):
    """
    Given raw violation text from an inspection record,
    return a priority tier: High | Medium | Low | Review
    """
    if not violation_text:
        return 'Review'

    text = violation_text.lower()

    has_cert = any(kw in text for kw in CERT_KEYWORDS)
    knowledge_count = sum(1 for kw in KNOWLEDGE_KEYWORDS if kw in text)

    if has_cert and knowledge_count >= 2:
        return 'High'
    elif has_cert or knowledge_count >= 3:
        return 'Medium'
    elif knowledge_count >= 1:
        return 'Low'
    else:
        return 'Review'
