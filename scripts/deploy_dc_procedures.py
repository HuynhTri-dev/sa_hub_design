import json
import os
import sys
import urllib.request
import urllib.error
import time

AGENT_ID = "agent_1301m118gtf3fnwb1bq7ed8t25st"
BRANCH_ID = "agtbrch_1601m118gtxve0maj03pw19kzp64"

# Get API key from environment variable or MCP config fallback
key = os.environ.get("ELEVENLABS_API_KEY")
if not key:
    try:
        p = os.path.expanduser('~/.gemini/config/mcp_config.json')
        key = json.load(open(p))['mcpServers']['ElevenLabs']['env']['ELEVENLABS_API_KEY']
    except Exception as e:
        print("Cannot read ElevenLabs API Key from config:", e)
        sys.exit(1)

HEADERS = {
    "xi-api-key": key,
    "Content-Type": "application/json"
}

def api(method, path, body=None):
    url = f"https://api.elevenlabs.io/v1/convai/agents/{AGENT_ID}"
    if path:
        url += path
    
    if "?" in url:
        url += f"&branch_id={BRANCH_ID}"
    else:
        url += f"?branch_id={BRANCH_ID}"

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        return None, e.read().decode()

print("="*60)
print("  Deploying Debt Collection Agent Procedures")
print("="*60)

# 1. DELETE EXISTING PROCEDURES
print("\n[1] Deleting existing procedures to avoid conflicts...")
procs, err = api("GET", "/branches/{}/procedures".format(BRANCH_ID))
if not err:
    proc_list = procs if isinstance(procs, list) else procs.get("procedures", [])
    for p in proc_list:
        pid = p.get('procedure_id')
        print(f"    Deleting {p.get('name')} ({pid})...")
        api("DELETE", f"/branches/{BRANCH_ID}/procedures/{pid}")
        time.sleep(0.5)

# 2. UPDATE TOOLS
print("\n[2] Updating Tool Names and Schemas...")
WEBHOOK_TOOLS = [
    {
        "type": "webhook",
        "name": "verify_customer_id",
        "description": "Verify customer identity using their CCCD (12 digits). This process is applied at the start of a call.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/verify",
            "method": "POST",
            "request_body_schema": {
                "description": "Full 12-digit Citizen ID (CCCD) for check debt info",
                "dynamic_variable": "",
                "is_omitted": False,
                "type": "object",
                "required": [
                    "cccd_number"
                ],
                "properties": {
                    "cccd_number": {
                        "type": "string",
                        "description": "Full 12-digit Citizen ID (CCCD).",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    }
                }
            },
            "content_type": "application/json"
        }
    },
    {
        "type": "webhook",
        "name": "get_debt_info",
        "description": "L\u1ea5y th\u00f4ng tin kho\u1ea3n n\u1ee3 hi\u1ec7n t\u1ea1i v\u00e0 c\u00e1c bi\u1ebfn tr\u1ea1ng th\u00e1i (state variables) c\u1ee7a kh\u00e1ch h\u00e0ng.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/debt/customer/{customerId}/status",
            "method": "GET",
            "path_params_schema": {
                "customerId": {
                    "type": "string",
                    "description": "The customer ID returned from verify_customer_id th\u00f4ng qua bi\u1ebfn {{customerId}}.",
                    "enum": None,
                    "is_system_provided": False,
                    "dynamic_variable": "",
                    "allowed_values_dynamic_variable": "",
                    "constant_value": "",
                    "is_omitted": False
                }
            },
            "content_type": "application/json"
        }
    },
    {
        "type": "webhook",
        "name": "update_debt_status",
        "description": "C\u1eadp nh\u1eadt th\u00f4ng tin kh\u00e1ch h\u00e0ng cung c\u1ea5p v\u00e0o h\u1ec7 th\u1ed1ng CRM (ghi nh\u1eadn PTP).",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/debt/customer/{customerId}/status",
            "method": "PATCH",
            "path_params_schema": {
                "customerId": {
                    "type": "string",
                    "description": "The customer ID",
                    "enum": None,
                    "is_system_provided": False,
                    "dynamic_variable": "",
                    "allowed_values_dynamic_variable": "",
                    "constant_value": "",
                    "is_omitted": False
                }
            },
            "request_body_schema": {
                "description": "",
                "dynamic_variable": "",
                "is_omitted": False,
                "type": "object",
                "required": [],
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Customer confirmed the debt",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for late payment",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    },
                    "solution": {
                        "type": "string",
                        "description": "Proposed solution for the debt",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    },
                    "promise_amount": {
                        "type": "number",
                        "description": "Promised payment amount",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    },
                    "promise_date": {
                        "type": "string",
                        "description": "Promised payment date",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    }
                }
            },
            "content_type": "application/json"
        }
    }
]


payload = {
    "conversation_config": {
        "agent": {
            "prompt": {
                "tools": WEBHOOK_TOOLS
            }
        }
    }
}

_, err = api("PATCH", "", payload)
if err:
    print("    ERROR patching tools:", err[:1000])
    sys.exit(1)
print("    OK - Webhook & Built-in tools updated.")


# 3. CREATE DETERMINISTIC PROCEDURES
print("\n[3] Creating Deterministic Procedures...")

PROCEDURES = [
    {
        "name": "Thu Th\u1eadp Th\u00f4ng Tin PTP (B\u1ea3ng T\u00edch)",
        "type": "free_form",
        "trigger": "Kh\u00e1ch h\u00e0ng \u0111\u00e3 x\u00e1c nh\u1eadn \u0111\u00fang th\u00f4ng tin kho\u1ea3n n\u1ee3 v\u00e0 \u0111\u1ed3ng \u00fd trao \u0111\u1ed5i ti\u1ebfp.",
        "content": "---\nname: Thu Th\u1eadp Th\u00f4ng Tin PTP (B\u1ea3ng T\u00edch)\ntrigger: Kh\u00e1ch h\u00e0ng \u0111\u00e3 x\u00e1c nh\u1eadn \u0111\u00fang th\u00f4ng tin kho\u1ea3n n\u1ee3 v\u00e0 \u0111\u1ed3ng \u00fd trao \u0111\u1ed5i ti\u1ebfp.\n---\n\nB\u1ea1n c\u00f3 nhi\u1ec7m v\u1ee5 thu th\u1eadp th\u00f4ng tin Cam k\u1ebft thanh to\u00e1n (PTP) t\u1eeb kh\u00e1ch h\u00e0ng. H\u00e3y ho\u1ea1t \u0111\u1ed9ng nh\u01b0 m\u1ed9t \"b\u1ea3ng ki\u1ec3m\" (checklist) \u0111\u1ec3 thu th\u1eadp th\u00f4ng tin c\u00f2n thi\u1ebfu.\n\nB\u01af\u1edaC 1: KH\u1edeI T\u1ea0O TH\u00d4NG TIN\n\nB\u1eaft bu\u1ed9c g\u1ecdi tool \u0111\u1ea7u [tool id=\"tool_4601m0see2pafbytam574hhyhb0m\" name=\"get_debt_info\"] v\u1edbi bi\u1ebfn customerId t\u1eeb {{customerId}}\n\n- \u0110\u1ecdc v\u00e0 set c\u00e1c bi\u1ebfn: \n  - `confirm`: {{confirm}}\n  - `reason_late_paid`: {{reason_late_paid}}\n  - `proposed_solution` : {{proposed_solution}}\n  - `promised_payment_amount` : {{promised_payment_amount}}\n  - `promised_payment_time` : {{promised_payment_time}} t\u1eeb k\u1ebft qu\u1ea3 tr\u1ea3 v\u1ec1 c\u1ee7a tool.\n\nB\u01af\u1edaC 2: THU TH\u1eacP TH\u00d4NG TIN (B\u1ea2NG T\u00cdCH)\nLU\u00d4N ki\u1ec3m tra c\u00e1c bi\u1ebfn v\u1eeba nh\u1eadn \u0111\u01b0\u1ee3c. N\u1ebeU D\u1eee LI\u1ec6U \u0110\u00c3 C\u00d3 (kh\u00e1c r\u1ed7ng ho\u1eb7c null), KH\u00d4NG \u0110\u01af\u1ee2C H\u1eceI L\u1ea0I. CH\u1ec8 H\u1eceI NH\u1eeeNG G\u00cc C\u00d2N THI\u1ebeU (d\u1eef li\u1ec7u r\u1ed7ng ho\u1eb7c null).\n\n1. **L\u00fd do qu\u00e1 h\u1ea1n (reason):**\n  - N\u1ebfu `reason_late_paid` r\u1ed7ng ho\u1eb7c null: H\u1ecfi \"D\u1ea1 anh/ch\u1ecb cho em h\u1ecfi hi\u1ec7n t\u1ea1i m\u00ecnh \u0111ang g\u1eb7p kh\u00f3 kh\u0103n g\u00ec m\u00e0 ch\u01b0a th\u1ec3 thanh to\u00e1n kho\u1ea3n n\u1ee3 n\u00e0y \u0111\u00fang h\u1ea1n \u1ea1?\"\n2. **Ph\u01b0\u01a1ng \u00e1n x\u1eed l\u00fd (solution):**\n  - N\u1ebfu `proposed_solution` r\u1ed7ng ho\u1eb7c null: \u0110\u00e0m ph\u00e1n ph\u01b0\u01a1ng \u00e1n. Nh\u1ea5n m\u1ea1nh: \"N\u1ebfu kh\u00f4ng thanh to\u00e1n, ng\u00e2n h\u00e0ng s\u1ebd bu\u1ed9c ph\u1ea3i ph\u00e1t m\u00e3i t\u00e0i s\u1ea3n b\u1ea3o \u0111\u1ea3m. V\u1eady anh/ch\u1ecb d\u1ef1 \u0111\u1ecbnh ph\u01b0\u01a1ng \u00e1n gi\u1ea3i quy\u1ebft s\u1eafp t\u1edbi nh\u01b0 th\u1ebf n\u00e0o \u1ea1?\"\n3. **S\u1ed1 ti\u1ec1n cam k\u1ebft n\u1ed9p (promise_amount):**\n  - N\u1ebfu `promised_payment_amount` r\u1ed7ng ho\u1eb7c null: H\u1ecfi \"D\u1ea1 v\u1eady anh/ch\u1ecb c\u00f3 th\u1ec3 n\u1ed9p v\u00e0o s\u1ed1 ti\u1ec1n bao nhi\u00eau \u0111\u1ec3 em ghi nh\u1eadn l\u00ean h\u1ec7 th\u1ed1ng \u1ea1?\"\n4. **Ng\u00e0y gi\u1edd cam k\u1ebft n\u1ed9p (promise_date):**\n  - N\u1ebfu `promised_payment_time` r\u1ed7ng ho\u1eb7c null: H\u1ecfi \"D\u1ea1 anh/ch\u1ecb d\u1ef1 ki\u1ebfn s\u1ebd n\u1ed9p s\u1ed1 ti\u1ec1n n\u00e0y v\u00e0o th\u1eddi gian n\u00e0o (ng\u00e0y n\u00e0o) \u0111\u1ec3 em t\u1ea1o l\u1ecbch h\u1eb9n \u1ea1?\"\n\nB\u01af\u1edaC 3: K\u1ebeT TH\u00daC\n\n- M\u1ed7i khi c\u00f3 b\u1ea5t k\u00ec th\u00f4ng tin m\u1edbi g\u00ec th\u00ec B\u1eaeT BU\u1ed8C g\u1ecdi tool [tool id=\"tool_6301m0see2pbfx5ay9kmgxr7cnay\" name=\"update_debt_status\"] \u0111\u1ec3 \u0111\u1ea9y c\u00e1c d\u1eef li\u1ec7u v\u1eeba l\u1ea5y \u0111\u01b0\u1ee3c v\u1ec1 h\u1ec7 th\u1ed1ng.\n- Cu\u1ed1i c\u00f9ng, c\u1ea3m \u01a1n v\u00e0 d\u1eb7n d\u00f2 kh\u00e1ch h\u00e0ng thanh to\u00e1n \u0111\u00fang h\u1ea1n."
    }
]


has_error = False
for p in PROCEDURES:
    body = {
        "name": p["name"],
        "type": p["type"],
        "trigger": p["trigger"],
        "content": p["content"]
    }
    resp, err = api("POST", f"/branches/{BRANCH_ID}/procedures", body)
    if err:
        print(f"    ERROR creating {p['name']}:", err[:300])
        has_error = True
    else:
        print(f"    OK - Created {p['name']} (ID: {resp.get('procedure_id')})")

if has_error:
    print("\nAborting compilation due to creation errors.")
    sys.exit(1)

# 4. PUBLISH
print("\n[4] Publishing to Branch...")
pub_body = {
    "version_description": "Deployed Debt Collection Webhooks and Free Form Checklist Procedure"
}
_, err = api("PATCH", "", pub_body)
if err:
    print("    ERROR publishing:", err[:1000])
    sys.exit(1)

print("    OK - Agent Branch published with Free Form procedure!")
print("="*60)
