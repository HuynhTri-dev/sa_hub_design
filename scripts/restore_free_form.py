import json
import os
import sys
import urllib.request
import urllib.error

AGENT_ID = "agent_9701m0h3t3ctfq39xbfyzx9adzb0"
BRANCH_ID = "agtbrch_0401m0h3t3cvebbrkk6p110njdft"

p = os.path.expanduser('~/.gemini/config/mcp_config.json')
key = json.load(open(p))['mcpServers']['ElevenLabs']['env']['ELEVENLABS_API_KEY']
HEADERS = {'xi-api-key': key, 'Content-Type': 'application/json'}

def api(method, path, body=None):
    url = f"https://api.elevenlabs.io/v1/convai/agents/{AGENT_ID}{path}"
    if "?" in url: url += f"&branch_id={BRANCH_ID}"
    else: url += f"?branch_id={BRANCH_ID}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    try: return json.loads(urllib.request.urlopen(req).read()), None
    except urllib.error.HTTPError as e: return None, e.read().decode()

# Delete all procedures
procs, _ = api("GET", "/branches/{}/procedures".format(BRANCH_ID))
for p in (procs if isinstance(procs, list) else procs.get("procedures", [])):
    api("DELETE", f"/branches/{BRANCH_ID}/procedures/{p.get('procedure_id')}")

# Create correct FREE FORM procedures
PROCEDURES = [
    {
        "name": "Báo mất thẻ / Khóa thẻ",
        "type": "free_form",
        "trigger": "Customer says they lost wallet, lost card, or asks to lock card.",
        "content": "## Khóa Thẻ Khẩn Cấp\n\n1. Ask for 12-digit CCCD.\n2. Call `verify_customer_id` with CCCD.\n3. Call `get_customer_cards` using customerId. Ask customer to select which card.\n4. Call `execute_card_lock` using customerId and card_last_four.\n5. Read spokenMessage verbatim."
    },
    {
        "name": "Tra cứu số dư",
        "type": "free_form",
        "trigger": "Customer asks to check balance.",
        "content": "## Tra cứu số dư\n\n1. Ask for CCCD and call `verify_customer_id`.\n2. Call `get_customer_cards`. Select card.\n3. Call `get_card_balance` with customerId.\n4. Read spokenBalance verbatim."
    },
    {
        "name": "Lịch sử giao dịch",
        "type": "free_form",
        "trigger": "Customer asks for recent transactions.",
        "content": "## Tra cứu giao dịch\n\n1. Ask for CCCD and call `verify_customer_id`.\n2. Call `get_customer_cards`. Select card.\n3. Call `get_recent_transactions`.\n4. Read transactions aloud."
    },
    {
        "name": "Fraud Report",
        "type": "free_form",
        "trigger": "Customer reports fraud, unrecognized transactions.",
        "content": "Transfer immediately via `transfer_to_number`."
    },
    {
        "name": "Unsupported",
        "type": "free_form",
        "trigger": "Customer asks for OTP, unlock card, loans.",
        "content": "Explain not supported. Transfer via `transfer_to_number`."
    }
]

for p in PROCEDURES:
    body = {"name": p["name"], "type": p["type"], "trigger": p["trigger"], "content": p["content"]}
    api("POST", f"/branches/{BRANCH_ID}/procedures", body)

api("PATCH", "", {"version_description": "Restored stable free-form procedures with correct tool names"})
print("OK - Restored free-form procedures.")
