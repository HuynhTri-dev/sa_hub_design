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
        "description": "Verifies a customer's Vietnamese Citizen ID (CCCD \u2014 12 digits). Returns customerId and fullName on success. Call this ONCE per session when the user provides their CCCD. Store customerId in session context; do NOT re-send CCCD in subsequent calls.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/verify",
            "method": "POST",
            "request_body_schema": {
                "description": "Full 12-digit Citizen ID (CCCD).",
                "dynamic_variable": "",
                "is_omitted": False,
                "type": "object",
                "required": [
                    "cccd_number"
                ],
                "properties": {
                    "cccd_number": {
                        "type": "string",
                        "description": "Full 12-digit Citizen ID number (CCCD) provided by the customer.",
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
        "name": "get_customer_cards",
        "description": "Retrieves all cards (type, last 4 digits, status) for an authenticated customer. Pass cccd_number is Full 12-digit Citizen ID (CCCD) from session \u2014 never pass the raw CCCD again.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/cards",
            "method": "GET",
            "query_params_schema": {
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
                },
                "required": []
            },
            "content_type": "application/json"
        }
    },
    {
        "type": "webhook",
        "name": "execute_card_lock",
        "description": "Locks a specific card immediately. Use cccd_number from session and the card_last_four digits confirmed by the customer. Read the spokenMessage field from the response back to the customer verbatim.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/lock-card",
            "method": "POST",
            "request_body_schema": {
                "description": "Information about the Full 12-digit Citizen ID (CCCD) and Last 4 digits of the card to be locked.",
                "dynamic_variable": "",
                "is_omitted": False,
                "type": "object",
                "required": [
                    "cccd_number",
                    "card_last_four"
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
                    },
                    "card_last_four": {
                        "type": "string",
                        "description": "Last 4 digits of the card to be locked.",
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
        "name": "get_card_balance",
        "description": "Retrieves the available balance for a specific card. Returns spokenBalance \u2014 a pre-formatted Vietnamese string (e.g. 'muoi lam trieu dong'). Read spokenBalance verbatim; do NOT reformat the number.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/customer/balance",
            "method": "GET",
            "query_params_schema": {
                "properties": {
                    "cccd_number": {
                        "type": "string",
                        "description": "Full 12-digit Citizen ID (CCCD) in the session.",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    },
                    "card_last_four": {
                        "type": "string",
                        "description": "Last 4 digits of the card to check.",
                        "enum": None,
                        "is_system_provided": False,
                        "dynamic_variable": "",
                        "allowed_values_dynamic_variable": "",
                        "constant_value": "",
                        "is_omitted": False
                    }
                },
                "required": []
            },
            "content_type": "application/json"
        }
    },
    {
        "type": "webhook",
        "name": "get_recent_transactions",
        "description": "Retrieves the last N recent transactions for a card. Read each transaction aloud in natural Vietnamese: date, amount (say 'tru' for negative, 'cong' for positive), and description.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/cskh/account/transactions?customerId={customerId}&limit={limit}",
            "method": "GET",
            "path_params_schema": {
                "customerId": {
                    "type": "string",
                    "description": "Customer identifier from session.",
                    "enum": None,
                    "is_system_provided": False,
                    "dynamic_variable": "",
                    "allowed_values_dynamic_variable": "",
                    "constant_value": "",
                    "is_omitted": False
                },
                "limit": {
                    "type": "string",
                    "description": "Number of transactions to return.",
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
                    "condition": "verify_customer_id returned False or error"
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
        "name": "Bao Mat The / Khoa The Khan Cap",
        "type": "deterministic",
        "trigger": "When the user says they lost their wallet, lost their card, suspects their card is compromised, or asks to lock, block, or freeze their card immediately.",
        "steps": [
            {
                "type": "ask",
                "instruction": "If the customer has NOT been authenticated in this session, ask for their full 12-digit CCCD (Can cuoc cong dan) number. Say: 'Da de bao mat tai khoan, em can anh/chi cung cap so can cuoc cong dan gom 12 chu so a.'",
                "id": "d7b75f88-2cda-4fb5-93c3-e7de517bb51b"
            },
            {
                "type": "tool_call",
                "tool_name": "verify_customer_id",
                "instruction": "Call verify_customer_id with the CCCD number. Store customerId and fullName in session.",
                "id": "ab6d2335-4f4f-419e-8955-203c44533253"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "verify_customer_id returned verified=False or an error"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "Tell the customer the CCCD did not match. Ask to try again carefully. Say: 'Da so can cuoc cong dan khong khop. Anh/chi vui long kiem tra va nhap lai a.'",
                                "id": "c2fc0fea-9f7f-47bd-8ac0-4c0bf1c22fd8"
                            },
                            {
                                "type": "tool_call",
                                "tool_name": "verify_customer_id",
                                "instruction": "Call verify_customer_id again with the re-entered CCCD.",
                                "id": "1f148f28-4a20-4ed0-bade-28afd1a0c3b4"
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
                                                "instruction": "Apologize and transfer to human agent. Say: 'Da em xin loi, em khong the xac thuc thong tin. Em se chuyen anh/chi den tong dai vien a.'"
                                            },
                                            {
                                                "type": "system_tool",
                                                "system_tool_name": "transfer_to_number"
                                            }
                                        ]
                                    }
                                ],
                                "fallback": [],
                                "id": "18307517-4938-4be2-8fa0-c321dda5629b"
                            }
                        ],
                        "id": "76774dfb-2531-4dc3-bab8-704a115e1d31"
                    }
                ],
                "fallback": [],
                "id": "bf996fe9-7b1b-4c6a-86b0-ffadc007340a"
            },
            {
                "type": "tool_call",
                "tool_name": "get_customer_cards",
                "instruction": "Call get_customer_cards with customerId from session. List ACTIVE cards only.",
                "id": "883fcc3f-c4a6-42ad-8c8d-a6f631f5324f"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "there are multiple active cards"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "List all active cards and ask which one to use. Say: 'Da anh/chi co [N] the: [list cards]. Anh/chi muon thuc hien voi the nao a?'",
                                "id": "6592efd7-7585-4851-80b1-c786b0879111"
                            }
                        ],
                        "id": "e77c9a61-bd7f-4e20-83a5-83c175f25e1f"
                    }
                ],
                "fallback": [],
                "id": "1416b54c-607a-4e50-99e2-0e1ad626d8ee"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "there is exactly one active card"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "Read the single card details and ask for confirmation before locking. Say: 'Da em thay anh/chi dang co the [cardType] duoi [cardLastFour]. Anh/chi co muon khoa the nay khong a?'",
                                "id": "b12d2ffc-f3de-4eca-8f0e-fbd986b85914"
                            }
                        ],
                        "id": "5d468175-7251-41ae-af38-5a3eee09e47c"
                    }
                ],
                "fallback": [
                    {
                        "type": "ask",
                        "instruction": "Ask which card to lock by last 4 digits. Say: 'Anh/chi muon khoa the nao a? Vui long cho em biet 4 so cuoi cua the can khoa.'",
                        "id": "4323415d-644f-4bb7-ba81-41be06d38c1a"
                    }
                ],
                "id": "fb2dd762-92af-4896-8583-e745c5e56dfe"
            },
            {
                "type": "tool_call",
                "tool_name": "execute_card_lock",
                "instruction": "Call execute_card_lock with customerId from session and card_last_four confirmed by the customer.",
                "id": "2644ef4a-7534-4524-9f54-0caeb2a70e77"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "execute_card_lock returned success=False or an error"
                        },
                        "steps": [
                            {
                                "type": "tell",
                                "instruction": "Inform the customer the lock failed and transfer to a human agent. Say: 'Da em xin loi, he thong hien khong the khoa the. Em se chuyen anh/chi den tong dai vien xu ly ngay a.'",
                                "id": "9bc62a47-b0b9-4645-8a6e-832b750d63cb"
                            },
                            {
                                "type": "system_tool",
                                "system_tool_name": "transfer_to_number",
                                "id": "14dd165c-bd69-4859-877f-b0f9edf90bbb"
                            }
                        ],
                        "id": "b492c450-482b-4ff9-a872-c908dcb1a622"
                    }
                ],
                "fallback": [
                    {
                        "type": "tell",
                        "instruction": "Read the spokenMessage field from execute_card_lock response verbatim. Then ask if the customer needs anything else.",
                        "id": "7fd571c9-c699-481d-b4fd-cc9f180c1b00"
                    }
                ],
                "id": "5e981647-8ee1-4691-ac74-42adb29f5e74"
            }
        ]
    },
    {
        "name": "Tra Cuu So Du Tai Khoan / The",
        "type": "deterministic",
        "trigger": "When the user asks to check their account balance, how much money is in their account, their current card balance, or says 'xem so du', 'con bao nhieu tien', 'tai khoan co bao nhieu'.",
        "steps": [
            {
                "type": "ask",
                "instruction": "If the customer has NOT been authenticated this session, ask for their full 12-digit CCCD number."
            },
            {
                "type": "tool_call",
                "tool_name": "verify_customer_id",
                "instruction": "Call verify_customer_id. Store customerId in session."
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "verify_customer_id returned verified=False or an error"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "Ask to re-enter CCCD carefully."
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
                                            "condition": "verify_customer_id failed again"
                                        },
                                        "steps": [
                                            {
                                                "type": "tell",
                                                "instruction": "Deny access and ask to visit a branch. Say: 'Da em xin loi, khong the xac thuc. Anh/chi vui long den chi nhanh gan nhat a.'"
                                            },
                                            {
                                                "type": "system_tool",
                                                "system_tool_name": "end_call"
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
            },
            {
                "type": "tool_call",
                "tool_name": "get_customer_cards",
                "instruction": "Call get_customer_cards with customerId from session. List ACTIVE cards only."
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "there are multiple active cards"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "List all active cards and ask which one to use. Say: 'Da anh/chi co [N] the: [list cards]. Anh/chi muon thuc hien voi the nao a?'"
                            }
                        ]
                    }
                ],
                "fallback": []
            },
            {
                "type": "tool_call",
                "tool_name": "get_card_balance",
                "instruction": "Call get_card_balance with customerId from session and card_last_four selected by the customer."
            },
            {
                "type": "tell",
                "instruction": "Read spokenBalance from the response verbatim. Do NOT reformat the number. Say: 'Da, so du kha dung cua the duoi [cardLastFour] la [spokenBalance] a.' Then ask if the customer needs anything else."
            }
        ]
    },
    {
        "name": "Tra Cuu Lich Su Giao Dich",
        "type": "deterministic",
        "trigger": "When the user asks about recent transactions, why their balance changed, whether a transfer went through, or says 'xem lich su giao dich', 'tai sao so du bi tru', 'moi chuyen khoan xong chua', 'tra cuu giao dich'.",
        "steps": [
            {
                "type": "ask",
                "instruction": "If the customer has NOT been authenticated in this session, ask for their full 12-digit CCCD (Can cuoc cong dan) number. Say: 'Da de bao mat tai khoan, em can anh/chi cung cap so can cuoc cong dan gom 12 chu so a.'",
                "id": "e0a604b3-fe6f-4d68-9432-58a79b31e1f3"
            },
            {
                "type": "tool_call",
                "tool_name": "verify_customer_id",
                "instruction": "Call verify_customer_id with the CCCD number. Store customerId and fullName in session.",
                "id": "0cadb044-44c2-43ed-a136-b4ea51c9f878"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "verify_customer_id returned verified=False or an error"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "Tell the customer the CCCD did not match. Ask to try again carefully. Say: 'Da so can cuoc cong dan khong khop. Anh/chi vui long kiem tra va nhap lai a.'",
                                "id": "af5387fc-be11-419a-a050-2c7bc7d62248"
                            },
                            {
                                "type": "tool_call",
                                "tool_name": "verify_customer_id",
                                "instruction": "Call verify_customer_id again with the re-entered CCCD.",
                                "id": "522b7315-8731-4052-a31c-f6983020513f"
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
                                                "instruction": "Apologize and transfer to human agent. Say: 'Da em xin loi, em khong the xac thuc thong tin. Em se chuyen anh/chi den tong dai vien a.'"
                                            },
                                            {
                                                "type": "system_tool",
                                                "system_tool_name": "transfer_to_number"
                                            }
                                        ]
                                    }
                                ],
                                "fallback": [],
                                "id": "b9ba9e26-165f-4bbb-a395-ab8f21658cdf"
                            }
                        ],
                        "id": "9e2b187f-eb35-4de7-947c-4dd58725ce61"
                    }
                ],
                "fallback": [],
                "id": "0996bf14-f253-4460-bf88-85e365c600a9"
            },
            {
                "type": "tool_call",
                "tool_name": "get_customer_cards",
                "instruction": "Call get_customer_cards with customerId from session. List ACTIVE cards only.",
                "id": "f21e456d-786c-4f19-8e8e-78b933045a3d"
            },
            {
                "type": "branch",
                "branches": [
                    {
                        "condition": {
                            "type": "llm",
                            "condition": "there are multiple active cards"
                        },
                        "steps": [
                            {
                                "type": "ask",
                                "instruction": "List all active cards and ask which one to use. Say: 'Da anh/chi co [N] the: [list cards]. Anh/chi muon thuc hien voi the nao a?'",
                                "id": "17056bba-9021-4983-9e99-1d2bc8fd3872"
                            }
                        ],
                        "id": "44d4d351-eed7-4f0c-b5ee-ff575d1b74be"
                    }
                ],
                "fallback": [],
                "id": "cf38e717-c490-4929-9880-65baea1f5486"
            },
            {
                "type": "tool_call",
                "tool_name": "get_recent_transactions",
                "instruction": "Call get_recent_transactions with customerId from session and limit=3.",
                "id": "94ffe050-52b1-4b67-9645-bdf3af56d55d"
            },
            {
                "type": "tell",
                "instruction": "Read each transaction aloud in natural Vietnamese, newest first. For each: state the date naturally (e.g. 'ngay 22 thang 8'), say 'tru [amount]' for negative amounts and 'cong [amount]' for positive, then the description. Example: 'Giao dich gan nhat la vao ngay 22 thang 8, tru nam muoi nghin dong tai ATM a.' After all transactions, ask if the customer needs anything else.",
                "id": "4b1534a0-5a7f-46c4-a2db-59f5b10b8d23"
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
