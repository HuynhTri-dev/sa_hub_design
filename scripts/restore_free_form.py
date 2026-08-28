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
        "name": "B\u00e1o m\u1ea5t th\u1ebb / Kh\u00f3a th\u1ebb",
        "type": "free_form",
        "trigger": "Customer says they lost wallet, lost card, or asks to lock card.",
        "content": "## Kh\u00f3a Th\u1ebb Kh\u1ea9n C\u1ea5p\n\n1. N\u1ebfu `{{dynamic_variables`_`cccd_number}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u kh\u00e1ch \u0111\u1ecdc 12 s\u1ed1 CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`. \u0110\u1ecdc danh s\u00e1ch v\u00e0 h\u1ecfi kh\u00e1ch mu\u1ed1n kh\u00f3a th\u1ebb n\u00e0o.\n3. G\u1ecdi `execute_card_lock` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}` v\u00e0 4 s\u1ed1 cu\u1ed1i th\u1ebb kh\u00e1ch ch\u1ecdn.\n4. \u0110\u1ecdc nguy\u00ean v\u0103n k\u1ebft qu\u1ea3 tr\u1ea3 v\u1ec1."
    },
    {
        "name": "Tra c\u1ee9u s\u1ed1 d\u01b0",
        "type": "free_form",
        "trigger": "Customer asks to check balance.",
        "content": "## Tra c\u1ee9u s\u1ed1 d\u01b0\n\n1. N\u1ebfu `{{dynamic_variables`_`cccd_number}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u kh\u00e1ch \u0111\u1ecdc 12 s\u1ed1 CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}`. H\u1ecfi kh\u00e1ch mu\u1ed1n tra c\u1ee9u th\u1ebb n\u00e0o.\n3. G\u1ecdi `get_card_balance` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}` v\u00e0 4 s\u1ed1 cu\u1ed1i th\u1ebb c\u1ea7n tra.\n4. \u0110\u1ecdc nguy\u00ean v\u0103n k\u1ebft qu\u1ea3 tr\u1ea3 v\u1ec1."
    },
    {
        "name": "L\u1ecbch s\u1eed giao d\u1ecbch",
        "type": "free_form",
        "trigger": "Customer asks for recent transactions.",
        "content": "## Tra c\u1ee9u giao d\u1ecbch\n\n1. N\u1ebfu `{{dynamic_variables`_`customerId}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`. H\u1ecfi kh\u00e1ch mu\u1ed1n ki\u1ec3m tra th\u1ebb n\u00e0o.\n3. G\u1ecdi `get_recent_transactions` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`.\n4. \u0110\u1ecdc chi ti\u1ebft c\u00e1c giao d\u1ecbch b\u1eb1ng ti\u1ebfng Vi\u1ec7t."
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
    },
    {
        "name": "Nghiep Vu Ngoai Pham Vi Ho Tro",
        "type": "free_form",
        "trigger": "When the user requests any of the following: card unlock (mo khoa the), card activation (kich hoat the moi), OTP-related services, SMS Banking registration or cancellation, corporate loans (vay doanh nghiep), home loans (vay mua nha), opening a new bank account, letters of credit (mo L/C), complex dispute resolution, interest rate negotiation, or any banking service the agent cannot handle directly.",
        "content": "## Procedure: Nghiep Vu Ngoai Pham Vi Ho Tro\n\nThis procedure handles any banking request the CSKH agent cannot process directly.\n\n### Steps\n\n1. Acknowledge the customer's request with empathy and a calm tone.\n2. Clearly explain that this specific service requires a human specialist    and cannot be processed through the automated channel.\n3. Tell the customer exactly:\n *'Da doi voi yeu cau nay, em chua duoc cap quyen ho tro truc tiep.    De duoc ho tro chinh xac nhat, em xin phep chuyen tiep cuoc tro chuyen    cua anh/chi den chuyen vien tu van cua ngan hang a.'*\n4. Use [system_tool id=\"transfer_to_number\" name=\"Transfer to human agent\"]    to immediately route the call to a human operator.\n\n### Important Rules\n\n- Do NOT attempt to answer or provide information about OTP, card unlock,   card activation, SMS Banking toggle, corporate loans, or L/C.\n- Do NOT ask the customer for additional information before transferring.\n- Do NOT hallucinate or fabricate answers for unsupported banking topics.\n- The tool `toggle_sms_banking` does NOT exist and must NEVER be called.\n- The tools `send_otp`, `verify_otp`, `execute_card_unlock`, and   `execute_card_activation` do NOT exist and must NEVER be called."
    }
]


for p in PROCEDURES:
    body = {"name": p["name"], "type": p["type"], "trigger": p["trigger"], "content": p["content"]}
    api("POST", f"/branches/{BRANCH_ID}/procedures", body)

api("PATCH", "", {"version_description": "Restored stable free-form procedures with correct tool names"})
print("OK - Restored free-form procedures.")
