"""
name: configure_cskh_agent.py
description: Configure the SacomBank CSKH ElevenLabs conversational AI agent.
             Sets up webhook tools, built-in tools, and procedures, then compiles
             and publishes all changes to the target agent branch.

Usage:
    export ELEVENLABS_API_KEY=<your_key>
    pip install "elevenlabs>=2.60.0"
    python scripts/configure_cskh_agent.py
"""

import json
import os
import sys
from elevenlabs import ElevenLabs
from elevenlabs.types import CreateProcedureRequestModel
from elevenlabs.errors import BadRequestError

# ─────────────────────────────────────────────
# Target agent & branch IDs (from URL)
# ─────────────────────────────────────────────
AGENT_ID = "agent_4201m118d1d2fmz9xjz9zt6kxsr8"
BRANCH_ID = "agtbrch_7601m118d2jsf45aadzb591c1w8m"

# Backend base URL — replace with actual CBS endpoint before going live
CBS_BASE = "https://backend-banking-core.vercel.app/api/v1/cskh"

# ─────────────────────────────────────────────
# 1. Tool definitions (webhook + built-in)
# ─────────────────────────────────────────────
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


BUILT_IN_TOOLS = {
    "end_call": {
        "type": "system",
        "name": "end_call",
        "description": "End the conversation session after the customer's needs are resolved.",
        "params": {"system_tool_type": "end_call"},
    },
    "transfer_to_number": {
        "type": "system",
        "name": "transfer_to_number",
        "description": (
            "Transfer the call to a human agent when requested, authentication fails twice, "
            "user reports fraud, or request is outside scope."
        ),
        "params": {"system_tool_type": "transfer_to_number"},
    },
    "start_procedure": {
        "type": "system",
        "name": "start_procedure",
        "description": "Activate a named procedure when a matching intent is detected.",
        "params": {"system_tool_type": "start_procedure"},
    },
}

# ─────────────────────────────────────────────
# 2. Procedure definitions
# ─────────────────────────────────────────────

def build_deterministic_content(trigger: str, steps: list) -> str:
    """
    Serialize a deterministic procedure content object to a JSON string.

    Args:
        trigger: Routing trigger string.
        steps: List of step objects.

    Returns:
        JSON-encoded string of the deterministic procedure body.
    """
    return json.dumps({"trigger": trigger, "steps": steps})


# Auth sub-steps reused across deterministic procedures
AUTH_STEPS_WITH_RETRY_TRANSFER = [
    {
        "type": "ask",
        "instruction": (
            "If the customer has NOT been authenticated in this session, "
            "ask for their full 12-digit CCCD (Can cuoc cong dan) number. "
            "Say: 'Da de bao mat tai khoan, em can anh/chi cung cap so can cuoc cong dan gom 12 chu so a.'"
        ),
    },
    {
        "type": "tool_call",
        "tool_name": "verify_customer_id",
        "instruction": "Call verify_customer_id with the CCCD number. Store customerId and fullName in session.",
    },
    {
        "type": "branch",
        "branches": [
            {
                "condition": {
                    "type": "llm",
                    "condition": "verify_customer_id returned verified=False or an error",
                },
                "steps": [
                    {
                        "type": "ask",
                        "instruction": (
                            "Tell the customer the CCCD did not match. Ask to try again carefully. "
                            "Say: 'Da so can cuoc cong dan khong khop. Anh/chi vui long kiem tra va nhap lai a.'"
                        ),
                    },
                    {
                        "type": "tool_call",
                        "tool_name": "verify_customer_id",
                        "instruction": "Call verify_customer_id again with the re-entered CCCD.",
                    },
                    {
                        "type": "branch",
                        "branches": [
                            {
                                "condition": {
                                    "type": "llm",
                                    "condition": "verify_customer_id failed a second time",
                                },
                                "steps": [
                                    {
                                        "type": "tell",
                                        "instruction": (
                                            "Apologize and transfer to human agent. "
                                            "Say: 'Da em xin loi, em khong the xac thuc thong tin. "
                                            "Em se chuyen anh/chi den tong dai vien a.'"
                                        ),
                                    },
                                    {
                                        "type": "system_tool",
                                        "system_tool_name": "transfer_to_number",
                                    },
                                ],
                            }
                        ],
                        "fallback": [],
                    },
                ],
            }
        ],
        "fallback": [],
    },
]

AUTH_STEPS_WITH_RETRY_DENY = [
    {
        "type": "ask",
        "instruction": (
            "If the customer has NOT been authenticated this session, "
            "ask for their full 12-digit CCCD number."
        ),
    },
    {
        "type": "tool_call",
        "tool_name": "verify_customer_id",
        "instruction": "Call verify_customer_id. Store customerId in session.",
    },
    {
        "type": "branch",
        "branches": [
            {
                "condition": {
                    "type": "llm",
                    "condition": "verify_customer_id returned verified=False or an error",
                },
                "steps": [
                    {
                        "type": "ask",
                        "instruction": "Ask to re-enter CCCD carefully.",
                    },
                    {
                        "type": "tool_call",
                        "tool_name": "verify_customer_id",
                        "instruction": "Retry verify_customer_id.",
                    },
                    {
                        "type": "branch",
                        "branches": [
                            {
                                "condition": {
                                    "type": "llm",
                                    "condition": "verify_customer_id failed again",
                                },
                                "steps": [
                                    {
                                        "type": "tell",
                                        "instruction": (
                                            "Deny access and ask to visit a branch. "
                                            "Say: 'Da em xin loi, khong the xac thuc. "
                                            "Anh/chi vui long den chi nhanh gan nhat a.'"
                                        ),
                                    },
                                    {
                                        "type": "system_tool",
                                        "system_tool_name": "end_call",
                                    },
                                ],
                            }
                        ],
                        "fallback": [],
                    },
                ],
            }
        ],
        "fallback": [],
    },
]

CARD_SELECT_STEPS = [
    {
        "type": "tool_call",
        "tool_name": "get_customer_cards",
        "instruction": "Call get_customer_cards with customerId from session. List ACTIVE cards only.",
    },
    {
        "type": "branch",
        "branches": [
            {
                "condition": {
                    "type": "llm",
                    "condition": "there are multiple active cards",
                },
                "steps": [
                    {
                        "type": "ask",
                        "instruction": (
                            "List all active cards and ask which one to use. "
                            "Say: 'Da anh/chi co [N] the: [list cards]. "
                            "Anh/chi muon thuc hien voi the nao a?'"
                        ),
                    }
                ],
            }
        ],
        "fallback": [],
    },
]

PROCEDURES = [
    {
        "name": "B\u00e1o m\u1ea5t th\u1ebb / Kh\u00f3a th\u1ebb",
        "slug": "proc_b\u00e1o_m\u1ea5t_th\u1ebb__kh\u00f3a_th\u1ebb",
        "type": "free_form",
        "trigger": "Customer says they lost wallet, lost card, or asks to lock card.",
        "content": "---\nname: B\u00e1o m\u1ea5t th\u1ebb / Kh\u00f3a th\u1ebb\ntrigger: Customer says they lost wallet, lost card, or asks to lock card.\n---\n\n## Kh\u00f3a Th\u1ebb Kh\u1ea9n C\u1ea5p\n\n1. N\u1ebfu `{{dynamic_variables`_`cccd_number}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u kh\u00e1ch \u0111\u1ecdc 12 s\u1ed1 CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`. \u0110\u1ecdc danh s\u00e1ch v\u00e0 h\u1ecfi kh\u00e1ch mu\u1ed1n kh\u00f3a th\u1ebb n\u00e0o.\n3. G\u1ecdi `execute_card_lock` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}` v\u00e0 4 s\u1ed1 cu\u1ed1i th\u1ebb kh\u00e1ch ch\u1ecdn.\n4. \u0110\u1ecdc nguy\u00ean v\u0103n k\u1ebft qu\u1ea3 tr\u1ea3 v\u1ec1."
    },
    {
        "name": "Tra c\u1ee9u s\u1ed1 d\u01b0",
        "slug": "proc_tra_c\u1ee9u_s\u1ed1_d\u01b0",
        "type": "free_form",
        "trigger": "Customer asks to check balance.",
        "content": "---\nname: Tra c\u1ee9u s\u1ed1 d\u01b0\ntrigger: Customer asks to check balance.\n---\n\n## Tra c\u1ee9u s\u1ed1 d\u01b0\n\n1. N\u1ebfu `{{dynamic_variables`_`cccd_number}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u kh\u00e1ch \u0111\u1ecdc 12 s\u1ed1 CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}`. H\u1ecfi kh\u00e1ch mu\u1ed1n tra c\u1ee9u th\u1ebb n\u00e0o.\n3. G\u1ecdi `get_card_balance` v\u1edbi `cccd_number` = `{{dynamic_variables`_`cccd_number}}` v\u00e0 4 s\u1ed1 cu\u1ed1i th\u1ebb c\u1ea7n tra.\n4. \u0110\u1ecdc nguy\u00ean v\u0103n k\u1ebft qu\u1ea3 tr\u1ea3 v\u1ec1."
    },
    {
        "name": "L\u1ecbch s\u1eed giao d\u1ecbch",
        "slug": "proc_l\u1ecbch_s\u1eed_giao_d\u1ecbch",
        "type": "free_form",
        "trigger": "Customer asks for recent transactions.",
        "content": "---\nname: L\u1ecbch s\u1eed giao d\u1ecbch\ntrigger: Customer asks for recent transactions.\n---\n\n## Tra c\u1ee9u giao d\u1ecbch\n\n1. N\u1ebfu `{{dynamic_variables`_`customerId}}` \u0111\u00e3 c\u00f3 s\u1eb5n, KH\u00d4NG H\u1eceI L\u1ea0I CCCD. N\u1ebfu ch\u01b0a c\u00f3, y\u00eau c\u1ea7u CCCD v\u00e0 g\u1ecdi `verify_customer_id`.\n2. G\u1ecdi `get_customer_cards` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`. H\u1ecfi kh\u00e1ch mu\u1ed1n ki\u1ec3m tra th\u1ebb n\u00e0o.\n3. G\u1ecdi `get_recent_transactions` v\u1edbi `customerId` = `{{dynamic_variables`_`customerId}}`.\n4. \u0110\u1ecdc chi ti\u1ebft c\u00e1c giao d\u1ecbch b\u1eb1ng ti\u1ebfng Vi\u1ec7t."
    },
    {
        "name": "Fraud Report",
        "slug": "proc_fraud_report",
        "type": "free_form",
        "trigger": "Customer reports fraud, unrecognized transactions.",
        "content": "Transfer immediately via `transfer_to_number`."
    },
    {
        "name": "Unsupported",
        "slug": "proc_unsupported",
        "type": "free_form",
        "trigger": "Customer asks for OTP, unlock card, loans.",
        "content": "Explain not supported. Transfer via `transfer_to_number`."
    }
]


def configure_tools(client: ElevenLabs) -> None:
    """
    PATCH the agent to set webhook tools and built-in tools.
    Uses two separate PATCH calls to avoid SDK serialization quirks
    with built_in_tools requiring a 'name' field on some SDK versions.

    Args:
        client: Authenticated ElevenLabs client.
    """
    print("\n[1/4] Configuring tools on agent...")
    client.conversational_ai.agents.update(
        agent_id=AGENT_ID,
        branch_id=BRANCH_ID,
        conversation_config={
            "agent": {
                "prompt": {
                    "tools": WEBHOOK_TOOLS,
                }
            }
        },
    )
    print("      OK - Tools configured.")


def create_procedures(client: ElevenLabs) -> list:
    """
    Create all procedure drafts on the branch.

    Args:
        client: Authenticated ElevenLabs client.

    Returns:
        List of (type, procedure_id, slug) tuples.
    """
    print("\n[2/4] Creating procedure drafts...")
    procs_api = client.conversational_ai.agents.procedures
    procedure_ids = []

    for proc in PROCEDURES:
        print(f"      Creating: {proc['slug']} ({proc['type']})...")
        created = procs_api.create(
            agent_id=AGENT_ID,
            branch_id=BRANCH_ID,
            request=CreateProcedureRequestModel(
                name=proc["name"],
                type=proc["type"],
                trigger=proc["trigger"],
                content=proc["content"],
            ),
        )
        proc_id = created.procedure_id
        procedure_ids.append((proc["type"], proc_id, proc["slug"]))
        print(f"      OK - {proc['slug']} -> procedure_id={proc_id}")

    return procedure_ids


def compile_and_publish(client: ElevenLabs, has_deterministic: bool) -> None:
    """
    Compile structured procedures (if any), then publish all drafts.

    Args:
        client: Authenticated ElevenLabs client.
        has_deterministic: Whether any deterministic procedures were staged.
    """
    procs_api = client.conversational_ai.agents.procedures
    workflow = None

    if has_deterministic:
        print("\n[3/4] Compiling structured (deterministic) procedures...")
        try:
            compiled = procs_api.compile(agent_id=AGENT_ID, branch_id=BRANCH_ID)
            workflow = compiled.workflow
            print("      OK - Compilation successful.")
        except BadRequestError as err:
            print(f"      ERROR - Compile failed:\n{err.body}")
            print("      Fix reported errors in PROCEDURES and re-run the script.")
            sys.exit(1)
    else:
        print("\n[3/4] No deterministic procedures - skipping compilation.")

    print("\n[4/4] Publishing all staged drafts to the branch...")
    update_kwargs = {
        "agent_id": AGENT_ID,
        "branch_id": BRANCH_ID,
        "version_description": (
            "CSKH Agent: webhook tools + "
            "proc_emergency_lock, proc_check_balance, proc_recent_tx, proc_unsupported"
        ),
    }
    if workflow:
        update_kwargs["workflow"] = workflow

    client.conversational_ai.agents.update(**update_kwargs)
    print("      OK - Published successfully.")


def main() -> None:
    """
    Entry point.
    Authenticate, configure tools, create procedures, compile, and publish.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY environment variable is not set.")
        print("   Run: export ELEVENLABS_API_KEY=<your_key>")
        sys.exit(1)

    print("=" * 60)
    print("  SacomBank - CSKH Agent Configuration Script")
    print("=" * 60)
    print(f"  Agent  : {AGENT_ID}")
    print(f"  Branch : {BRANCH_ID}")

    client = ElevenLabs(api_key=api_key)

    # Step 1 - Configure tools
    configure_tools(client)

    # Step 2 - Create procedures
    procedure_ids = create_procedures(client)

    # Step 3 + 4 - Compile + Publish
    has_deterministic = any(t == "deterministic" for t, _, _ in procedure_ids)
    compile_and_publish(client, has_deterministic)

    print("\n" + "=" * 60)
    print("  DONE - Configuration complete!")
    print("  Procedures created:")
    for ptype, pid, slug in procedure_ids:
        print(f"    - {slug} ({ptype}) -> {pid}")
    print("=" * 60)


if __name__ == "__main__":
    main()
