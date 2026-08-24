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
        "content": (
            "## Khóa Thẻ Khẩn Cấp\n\n"
            "1. Nếu `{{dynamic_variables.customerId}}` đã có sẵn, KHÔNG HỎI LẠI CCCD. Nếu chưa có, yêu cầu khách đọc 12 số CCCD và gọi `verify_customer_id`.\n"
            "2. Gọi `get_customer_cards` với `customerId` = `{{dynamic_variables.customerId}}`. Đọc danh sách và hỏi khách muốn khóa thẻ nào.\n"
            "3. Gọi `execute_card_lock` với `customerId` = `{{dynamic_variables.customerId}}` và 4 số cuối thẻ khách chọn.\n"
            "4. Đọc nguyên văn kết quả trả về."
        )
    },
    {
        "name": "Tra cứu số dư",
        "type": "free_form",
        "trigger": "Customer asks to check balance.",
        "content": (
            "## Tra cứu số dư\n\n"
            "1. Nếu `{{dynamic_variables.customerId}}` đã có sẵn, KHÔNG HỎI LẠI CCCD. Nếu chưa có, yêu cầu khách đọc 12 số CCCD và gọi `verify_customer_id`.\n"
            "2. Gọi `get_customer_cards` với `customerId` = `{{dynamic_variables.customerId}}`. Hỏi khách muốn tra cứu thẻ nào.\n"
            "3. Gọi `get_card_balance` với `customerId` = `{{dynamic_variables.customerId}}` và 4 số cuối thẻ.\n"
            "4. Đọc nguyên văn kết quả trả về."
        )
    },
    {
        "name": "Lịch sử giao dịch",
        "type": "free_form",
        "trigger": "Customer asks for recent transactions.",
        "content": (
            "## Tra cứu giao dịch\n\n"
            "1. Nếu `{{dynamic_variables.customerId}}` đã có sẵn, KHÔNG HỎI LẠI CCCD. Nếu chưa có, yêu cầu CCCD và gọi `verify_customer_id`.\n"
            "2. Gọi `get_customer_cards` với `customerId` = `{{dynamic_variables.customerId}}`. Hỏi khách muốn kiểm tra thẻ nào.\n"
            "3. Gọi `get_recent_transactions` với `customerId` = `{{dynamic_variables.customerId}}`.\n"
            "4. Đọc chi tiết các giao dịch bằng tiếng Việt."
        )
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
