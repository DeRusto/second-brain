import json

with open('second-brain.json', 'r') as f:
    data = json.load(f)

nodes = data['nodes']

# 1. Update Calendar Router to add fallback
router = next((n for n in nodes if n['name'] == 'Calendar Router'), None)
if router:
    # Add a fallback rule (empty condition list = default)
    # The current switch logic in n8n (v3.4+) usually treats the last output as default or you can route unmatched.
    # However, to be explicit as requested, we can add a catch-all condition.
    # Actually, n8n switch node (v3) usually routes first match. If no match, it goes nowhere unless routed.
    # The request asks to route any other value to personal calendar.
    # We can add a rule that always evaluates to true (or simply add a rule with no conditions if supported, but n8n often needs one).
    # A cleaner way in n8n is often to set the last output as the fallback.
    # But let's follow the specific suggestion: "add a fallback rule... that routes any other value to the personal calendar".

    # We will modify the 'personal' rule to be a catch-all OR add a new rule.
    # The suggestion implies creating an additional value entry.
    # Actually, simpler: make 'personal' the default by adding an OR condition for empty?
    # Or better yet, just add a 4th output for fallback and connect it to personal.

    # Let's add a 4th rule that catches everything else (effectively).
    # Since we can't easily do "else", we might rely on the fact that if it's not family or maggie, it should be personal.
    # But the user asked for a specific fallback rule.

    # Let's verify existing rules:
    # 0: family
    # 1: maggie
    # 2: personal

    # We will change rule 2 (personal) to be: calendar == personal OR calendar is empty OR calendar is not family/maggie?
    # The user suggested: "condition uses same leftValue... and (b) explicit comparator that matches empty/other".

    # Let's try adding a rule for "Calendar is Empty" and route it to Personal.
    # And maybe we just route the 'fallback' port of the switch to Personal?
    # n8n Switch node v3 has a "fallback" output if we configure it?
    # The JSON shows "rules": { "values": [...] }.

    # Let's try to add a condition to the 'Personal' rule to make it more inclusive.
    # "Calendar is NOT Family AND Calendar is NOT Maggie"

    # Current Personal Rule:
    # conditions: [{ left: ..., right: "personal", op: "equals" }]

    # We will change it to:
    # conditions: [
    #   { left: ..., right: "family", op: "notEqual" },
    #   { left: ..., right: "maggie", op: "notEqual" }
    # ]
    # combinator: AND

    # This effectively makes it "Anything that is not Family or Maggie".
    # This covers "personal", "", "other", etc.

    personal_rule_index = 2
    if len(router['parameters']['rules']['values']) > 2:
        personal_rule = router['parameters']['rules']['values'][2]
        personal_rule['conditions'] = {
            "options": {
                "caseSensitive": True,
                "leftValue": "",
                "typeValidation": "strict",
                "version": 3
            },
            "conditions": [
                {
                    "leftValue": "={{$('Confidence Gate').item.json.parsed.calendar}}",
                    "rightValue": "family",
                    "operator": {
                        "type": "string",
                        "operation": "notEquals"
                    }
                },
                {
                    "leftValue": "={{$('Confidence Gate').item.json.parsed.calendar}}",
                    "rightValue": "maggie",
                    "operator": {
                        "type": "string",
                        "operation": "notEquals"
                    }
                }
            ],
            "combinator": "and"
        }

# 2. Fix GCal Due Date Summary Expression
gcal_due = next((n for n in nodes if n['name'] == 'GCal Due Date'), None)
if gcal_due:
    summary_field = gcal_due['parameters'].get('additionalFields', {}).get('summary', '')
    # The comment says it uses $json.parsed.name.
    # Current JSON: "={{ \"Due: \" + $json.parsed.name }}"
    # We need to change it to: "={{ \"Due: \" + $('Confidence Gate').item.json.parsed.name }}"

    new_summary = '={{ "Due: " + $(\'Confidence Gate\').item.json.parsed.name }}'
    gcal_due['parameters']['additionalFields']['summary'] = new_summary

with open('second-brain.json', 'w') as f:
    json.dump(data, f, indent=2)
