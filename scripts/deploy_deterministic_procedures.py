import json
import os
import sys
import urllib.request
import urllib.error
import time

AGENT_ID = "agent_9701m0h3t3ctfq39xbfyzx9adzb0"
BRANCH_ID = "agtbrch_0401m0h3t3cvebbrkk6p110njdft"

# Get API key from MCP config
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
print("  Deploying Deterministic CSKH Agent")
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
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/auth/verify",
            "method": "POST",
            "request_body_schema": {
                "type": "object",
                "properties": {
                    "cccd_number": {"type": "string", "description": "Full 12-digit Citizen ID (CCCD)."}
                },
                "required": ["cccd_number"]
            }
        }
    },
    {
        "type": "webhook",
        "name": "get_customer_cards",
        "description": "Retrieve the list of all cards belonging to a customer based on their CCCD.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/cards?cccd_number={cccd_number}",
            "method": "GET",
            "path_params_schema": {
                "cccd_number": {"type": "string", "description": "The full CCCD number.", "is_system_provided": False, "is_omitted": False}
            }
        }
    },
    {
        "type": "webhook",
        "name": "execute_card_lock",
        "description": "Immediately lock the customer's card. Return a pre-recorded Vietnamese spoken message.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/cards/lock-emergency",
            "method": "POST",
            "request_body_schema": {
                "type": "object",
                "properties": {
                    "customerId": {"type": "string", "description": "Customer ID from session"},
                    "card_last_four": {"type": "string", "description": "Last 4 digits of card to lock"}
                },
                "required": ["customerId", "card_last_four"]
            }
        }
    },
    {
        "type": "webhook",
        "name": "get_card_balance",
        "description": "Check balance for customer card. Return the numeric balance and a pre-recorded Vietnamese spoken phrase.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/account/balance?customerId={customerId}",
            "method": "GET",
            "path_params_schema": {
                "customerId": {"type": "string", "description": "Customer ID from session", "is_system_provided": False, "is_omitted": False}
            }
        }
    },
    {
        "type": "webhook",
        "name": "get_recent_transactions",
        "description": "Query the customer's most recent account transactions.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/account/transactions?customerId={customerId}&limit={limit}",
            "method": "GET",
            "path_params_schema": {
                "customerId": {"type": "string", "description": "Customer ID from session", "is_system_provided": False, "is_omitted": False},
                "limit": {"type": "string", "description": "Number of transactions to return", "is_system_provided": False, "is_omitted": False}
            }
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

AUTH_STEPS = [
    {
        "type": "ask",
        "instruction": "If customerId is not yet recorded in this session, ask the customer for their full 12-digit CCCD (Can cuoc cong dan) number. Say: 'Dạ để bảo mật, anh/chị vui lòng cung cấp số Căn cước công dân gồm 12 số ạ.'"
    },
    {
        "type": "tool_call",
        "tool_name": "verify_customer_id",
        "instruction": "Call verify_customer_id with the provided CCCD. IMPORTANT: Save the returned 'customerId' to use for subsequent steps."
    },
    {
        "type": "branch",
        "branches": [
            {
                "condition": {
                    "type": "llm",
                    "condition": "verify_customer_id returned false or error"
                },
                "steps": [
                    {
                        "type": "ask",
                        "instruction": "Ask the customer to retry carefully. 'Dạ thông tin chưa khớp, anh/chị vui lòng đọc lại giúp em ạ.'"
                    },
                    {
                        "type": "tool_call",
                        "tool_name": "verify_customer_id",
                        "instruction": "Retry verify_customer_id."
                    },
                    {
                        "type": "branch",
                        "branches": [
                            {
                                "condition": {
                                    "type": "llm",
                                    "condition": "verify_customer_id failed a second time"
                                },
                                "steps": [
                                    {
                                        "type": "tell",
                                        "instruction": "Say: 'Dạ em xin lỗi, em chưa thể xác thực được. Em sẽ chuyển anh/chị đến chuyên viên ạ.'"
                                    },
                                    {
                                        "type": "system_tool",
                                        "system_tool_name": "transfer_to_number"
                                    }
                                ]
                            }
                        ],
                        "fallback": []
                    }
                ]
            }
        ],
        "fallback": []
    }
]

PROCEDURES = [
    {
        "name": "Bảo Mật / Khóa thẻ khẩn cấp",
        "type": "deterministic",
        "trigger": "Customer says they lost wallet, lost card, or asks to lock/block card.",
        "steps": [
            *AUTH_STEPS,
            {
                "type": "tool_call",
                "tool_name": "get_customer_cards",
                "instruction": "Call get_customer_cards using the CCCD number from authentication."
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "The customer has multiple active cards"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "List the cards and ask which one to lock. Provide last 4 digits."
                            }
                        ]
                    },
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "The customer has only 1 active card"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "Read the card details and ask for confirmation to lock."
                            }
                        ]
                    }
                ],
                "fallback": []
            },
            {
                "type": "tool_call",
                "tool_name": "execute_card_lock",
                "instruction": "Call execute_card_lock using customerId and the confirmed card_last_four."
            },
            {
                "type": "tell",
                "instruction": "Read the spokenMessage field from execute_card_lock verbatim to the customer. Then ask if they need anything else."
            }
        ]
    },
    {
        "name": "Tra cứu số dư",
        "type": "deterministic",
        "trigger": "Customer asks to check account balance, card balance, con bao nhieu tien.",
        "steps": [
            *AUTH_STEPS,
            {
                "type": "tool_call",
                "tool_name": "get_customer_cards",
                "instruction": "Call get_customer_cards using CCCD number."
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "The customer has multiple active cards"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "List the cards and ask which one to check."
                            }
                        ]
                    }
                ],
                "fallback": []
            },
            {
                "type": "tool_call",
                "tool_name": "get_card_balance",
                "instruction": "Call get_card_balance using customerId and card_last_four."
            },
            {
                "type": "tell",
                "instruction": "Read the spokenBalance verbatim to the customer."
            }
        ]
    },
    {
        "name": "Tra cứu giao dịch",
        "type": "deterministic",
        "trigger": "Customer asks for recent transactions, why balance changed.",
        "steps": [
            *AUTH_STEPS,
            {
                "type": "tool_call",
                "tool_name": "get_recent_transactions",
                "instruction": "Call get_recent_transactions using customerId."
            },
            {
                "type": "tell",
                "instruction": "Read the transactions aloud in natural Vietnamese. Then ask if they need anything else."
            }
        ]
    }
]

has_error = False
for p in PROCEDURES:
    content_str = json.dumps({"trigger": p["trigger"], "steps": p["steps"]})
    body = {
        "name": p["name"],
        "type": p["type"],
        "trigger": p["trigger"],
        "content": content_str
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

# 4. COMPILE
print("\n[4] Compiling Deterministic Procedures...")
comp_resp, err = api("POST", f"/branches/{BRANCH_ID}/procedures/compile")
if err:
    print("    ERROR compiling:", err[:1500])
    sys.exit(1)

workflow = comp_resp.get("workflow")
print("    OK - Compilation successful!")

# 5. PUBLISH
print("\n[5] Publishing to Branch...")
pub_body = {
    "workflow": workflow,
    "version_description": "Updated deterministic procedures and matched exact tool names"
}
_, err = api("PATCH", "", pub_body)
if err:
    print("    ERROR publishing:", err[:1000])
    sys.exit(1)

print("    OK - Agent Branch published with Deterministic workflow!")
print("="*60)
