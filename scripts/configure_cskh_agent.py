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
AGENT_ID = "agent_9701m0h3t3ctfq39xbfyzx9adzb0"
BRANCH_ID = "agtbrch_0401m0h3t3cvebbrkk6p110njdft"

# Backend base URL — replace with actual CBS endpoint before going live
CBS_BASE = "https://backend-banking-core.vercel.app/api/v1/cskh"

# ─────────────────────────────────────────────
# 1. Tool definitions (webhook + built-in)
# ─────────────────────────────────────────────
WEBHOOK_TOOLS = [
    {
        "type": "webhook",
        "name": "verify_customer_id",
        "description": (
            "Verifies a customer's Vietnamese Citizen ID (CCCD — 12 digits). "
            "Returns customerId and fullName on success. "
            "Call this ONCE per session when the user provides their CCCD. "
            "Store customerId in session context; do NOT re-send CCCD in subsequent calls."
        ),
        "api_schema": {
            "url": f"{CBS_BASE}/customer/verify",
            "method": "POST",
            "request_body_schema": {
                "type": "object",
                "properties": {
                    "cccd_number": {
                        "type": "string",
                        "description": "Full 12-digit Citizen ID number (CCCD) provided by the customer.",
                    }
                },
                "required": ["cccd_number"],
            },
            "response_body_schema": {
                "type": "object",
                "description": "Verification result.",
                "properties": {
                    "customerId": {
                        "type": "string",
                        "description": "Internal customer identifier. Store in session; use for all subsequent API calls.",
                    },
                    "fullName": {
                        "type": "string",
                        "description": "Customer's registered full name.",
                    },
                    "phoneNumber": {
                        "type": "string",
                        "description": "Customer's registered phone number. Assign this to a dynamic variable.",
                    },
                    "nationalIdLast4": {
                        "type": "string",
                        "description": "Customer's last 4 digits of CCCD. Assign this to a dynamic variable.",
                    },
                    "verified": {
                        "type": "boolean",
                        "description": "True when the CCCD matched a customer record.",
                    },
                },
            },
        },
    },
    {
        "type": "webhook",
        "name": "get_customer_cards",
        "description": (
            "Retrieves all cards (type, last 4 digits, status) for an authenticated customer. "
            "Pass customerId from session — never pass the raw CCCD again. "
            "Only return ACTIVE cards to the customer."
        ),
        "api_schema": {
            "url": f"{CBS_BASE}/customer/cards",
            "method": "GET",
            "query_params_schema": {
                "properties": {
                    "customerId": {
                        "type": "string",
                        "description": "Customer identifier from session.",
                    }
                }
            },
            "response_body_schema": {
                "type": "object",
                "description": "Card list for the customer.",
                "properties": {
                    "cards": {
                        "type": "array",
                        "description": "List of customer cards.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "cardType": {
                                    "type": "string",
                                    "description": "Card network brand (Visa, Mastercard, JCB, Napas).",
                                },
                                "cardLastFour": {
                                    "type": "string",
                                    "description": "Last 4 digits of the card number.",
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Card status: ACTIVE, LOCKED, or EXPIRED.",
                                },
                            },
                        },
                    }
                },
            },
        },
    },
    {
        "type": "webhook",
        "name": "execute_card_lock",
        "description": (
            "Locks a specific card immediately. "
            "Use customerId from session and the card_last_four digits confirmed by the customer. "
            "Read the spokenMessage field from the response back to the customer verbatim."
        ),
        "api_schema": {
            "url": f"{CBS_BASE}/customer/lock-card",
            "method": "POST",
            "request_body_schema": {
                "type": "object",
                "properties": {
                    "customerId": {
                        "type": "string",
                        "description": "Customer identifier from session.",
                    },
                    "card_last_four": {
                        "type": "string",
                        "description": "Last 4 digits of the card to be locked.",
                    },
                },
                "required": ["customerId", "card_last_four"],
            },
            "response_body_schema": {
                "type": "object",
                "description": "Card lock result.",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "True when the card was locked successfully.",
                    },
                    "spokenMessage": {
                        "type": "string",
                        "description": "Pre-formatted Vietnamese confirmation message to read aloud to the customer.",
                    },
                },
            },
        },
    },
    {
        "type": "webhook",
        "name": "get_card_balance",
        "description": (
            "Retrieves the available balance for a specific card. "
            "Returns spokenBalance — a pre-formatted Vietnamese string (e.g. 'muoi lam trieu dong'). "
            "Read spokenBalance verbatim; do NOT reformat the number."
        ),
        "api_schema": {
            "url": f"{CBS_BASE}/customer/balance",
            "method": "GET",
            "query_params_schema": {
                "properties": {
                    "customerId": {
                        "type": "string",
                        "description": "Customer identifier from session.",
                    },
                    "card_last_four": {
                        "type": "string",
                        "description": "Last 4 digits of the card to check.",
                    }
                }
            },
            "response_body_schema": {
                "type": "object",
                "description": "Card balance result.",
                "properties": {
                    "balance": {
                        "type": "number",
                        "description": "Raw numeric balance in VND.",
                    },
                    "spokenBalance": {
                        "type": "string",
                        "description": "Pre-formatted Vietnamese text for TTS. Read this verbatim.",
                    },
                },
            },
        },
    },
    {
        "type": "webhook",
        "name": "get_recent_transactions",
        "description": (
            "Retrieves the last N recent transactions for a card. "
            "Default limit=3. Read each transaction aloud in natural Vietnamese: "
            "date, amount (say 'tru' for negative, 'cong' for positive), and description."
        ),
        "api_schema": {
            "url": f"{CBS_BASE}/account/transactions",
            "method": "GET",
            "query_params_schema": {
                "properties": {
                    "customerId": {
                        "type": "string",
                        "description": "Customer identifier from session.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of transactions to return.",
                    }
                }
            },
            "response_body_schema": {
                "type": "object",
                "description": "Transaction history.",
                "properties": {
                    "transactions": {
                        "type": "array",
                        "description": "List of recent transactions, newest first.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "Transaction date (ISO 8601).",
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Amount in VND. Negative = debit, positive = credit.",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Human-readable transaction description.",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Transaction type (DEBIT, CREDIT, TRANSFER, ATM_WITHDRAWAL).",
                                },
                            },
                        },
                    }
                },
            },
        },
    },
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
                    "condition": "verify_customer_id returned verified=false or an error",
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
                    "condition": "verify_customer_id returned verified=false or an error",
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
    # ── 1. Emergency Card Lock (deterministic) ───────────────────────────────
    {
        "name": "Bao Mat The / Khoa The Khan Cap",
        "slug": "proc_emergency_lock",
        "type": "deterministic",
        "trigger": (
            "When the user says they lost their wallet, lost their card, "
            "suspects their card is compromised, or asks to lock, block, or freeze their card immediately."
        ),
        "content": build_deterministic_content(
            trigger=(
                "When the user says they lost their wallet, lost their card, "
                "suspects their card is compromised, or asks to lock, block, or freeze their card immediately."
            ),
            steps=[
                *AUTH_STEPS_WITH_RETRY_TRANSFER,
                *CARD_SELECT_STEPS,
                {
                    "type": "branch",
                    "branches": [
                        {
                            "condition": {
                                "type": "llm",
                                "condition": "there is exactly one active card",
                            },
                            "steps": [
                                {
                                    "type": "ask",
                                    "instruction": (
                                        "Read the single card details and ask for confirmation before locking. "
                                        "Say: 'Da em thay anh/chi dang co the [cardType] duoi [cardLastFour]. "
                                        "Anh/chi co muon khoa the nay khong a?'"
                                    ),
                                }
                            ],
                        }
                    ],
                    "fallback": [
                        {
                            "type": "ask",
                            "instruction": (
                                "Ask which card to lock by last 4 digits. "
                                "Say: 'Anh/chi muon khoa the nao a? Vui long cho em biet 4 so cuoi cua the can khoa.'"
                            ),
                        }
                    ],
                },
                {
                    "type": "tool_call",
                    "tool_name": "execute_card_lock",
                    "instruction": (
                        "Call execute_card_lock with customerId from session "
                        "and card_last_four confirmed by the customer."
                    ),
                },
                {
                    "type": "branch",
                    "branches": [
                        {
                            "condition": {
                                "type": "llm",
                                "condition": "execute_card_lock returned success=false or an error",
                            },
                            "steps": [
                                {
                                    "type": "tell",
                                    "instruction": (
                                        "Inform the customer the lock failed and transfer to a human agent. "
                                        "Say: 'Da em xin loi, he thong hien khong the khoa the. "
                                        "Em se chuyen anh/chi den tong dai vien xu ly ngay a.'"
                                    ),
                                },
                                {
                                    "type": "system_tool",
                                    "system_tool_name": "transfer_to_number",
                                },
                            ],
                        }
                    ],
                    "fallback": [
                        {
                            "type": "tell",
                            "instruction": (
                                "Read the spokenMessage field from execute_card_lock response verbatim. "
                                "Then ask if the customer needs anything else."
                            ),
                        }
                    ],
                },
            ],
        ),
    },

    # ── 2. Check Card Balance (deterministic) ────────────────────────────────
    {
        "name": "Tra Cuu So Du Tai Khoan / The",
        "slug": "proc_check_balance",
        "type": "deterministic",
        "trigger": (
            "When the user asks to check their account balance, how much money is in their account, "
            "their current card balance, or says 'xem so du', 'con bao nhieu tien', 'tai khoan co bao nhieu'."
        ),
        "content": build_deterministic_content(
            trigger=(
                "When the user asks to check their account balance, how much money is in their account, "
                "their current card balance, or says 'xem so du', 'con bao nhieu tien', 'tai khoan co bao nhieu'."
            ),
            steps=[
                *AUTH_STEPS_WITH_RETRY_DENY,
                *CARD_SELECT_STEPS,
                {
                    "type": "tool_call",
                    "tool_name": "get_card_balance",
                    "instruction": (
                        "Call get_card_balance with customerId from session "
                        "and card_last_four selected by the customer."
                    ),
                },
                {
                    "type": "tell",
                    "instruction": (
                        "Read spokenBalance from the response verbatim. Do NOT reformat the number. "
                        "Say: 'Da, so du kha dung cua the duoi [cardLastFour] la [spokenBalance] a.' "
                        "Then ask if the customer needs anything else."
                    ),
                },
            ],
        ),
    },

    # ── 3. Recent Transactions (deterministic) ───────────────────────────────
    {
        "name": "Tra Cuu Lich Su Giao Dich",
        "slug": "proc_recent_tx",
        "type": "deterministic",
        "trigger": (
            "When the user asks about recent transactions, why their balance changed, "
            "whether a transfer went through, or says 'xem lich su giao dich', "
            "'tai sao so du bi tru', 'moi chuyen khoan xong chua', 'tra cuu giao dich'."
        ),
        "content": build_deterministic_content(
            trigger=(
                "When the user asks about recent transactions, why their balance changed, "
                "whether a transfer went through, or says 'xem lich su giao dich', "
                "'tai sao so du bi tru', 'moi chuyen khoan xong chua', 'tra cuu giao dich'."
            ),
            steps=[
                *AUTH_STEPS_WITH_RETRY_TRANSFER,
                *CARD_SELECT_STEPS,
                {
                    "type": "tool_call",
                    "tool_name": "get_recent_transactions",
                    "instruction": (
                        "Call get_recent_transactions with customerId from session and limit=3."
                    ),
                },
                {
                    "type": "tell",
                    "instruction": (
                        "Read each transaction aloud in natural Vietnamese, newest first. "
                        "For each: state the date naturally (e.g. 'ngay 22 thang 8'), "
                        "say 'tru [amount]' for negative amounts and 'cong [amount]' for positive, "
                        "then the description. "
                        "Example: 'Giao dich gan nhat la vao ngay 22 thang 8, tru nam muoi nghin dong tai ATM a.' "
                        "After all transactions, ask if the customer needs anything else."
                    ),
                },
            ],
        ),
    },

    # ── 4. Unsupported Banking (free_form) ───────────────────────────────────
    {
        "name": "Nghiep Vu Ngoai Pham Vi Ho Tro",
        "slug": "proc_unsupported",
        "type": "free_form",
        "trigger": (
            "When the user requests any of the following: card unlock (mo khoa the), "
            "card activation (kich hoat the moi), OTP-related services, "
            "SMS Banking registration or cancellation, corporate loans (vay doanh nghiep), "
            "home loans (vay mua nha), opening a new bank account, "
            "letters of credit (mo L/C), complex dispute resolution, "
            "interest rate negotiation, or any banking service the agent cannot handle directly."
        ),
        "content": (
            "## Procedure: Nghiep Vu Ngoai Pham Vi Ho Tro\n\n"
            "This procedure handles any banking request the CSKH agent cannot process directly.\n\n"
            "### Steps\n\n"
            "1. Acknowledge the customer's request with empathy and a calm tone.\n"
            "2. Clearly explain that this specific service requires a human specialist "
            "   and cannot be processed through the automated channel.\n"
            "3. Tell the customer exactly:\n"
            "   *'Da doi voi yeu cau nay, em chua duoc cap quyen ho tro truc tiep. "
            "   De duoc ho tro chinh xac nhat, em xin phep chuyen tiep cuoc tro chuyen "
            "   cua anh/chi den chuyen vien tu van cua ngan hang a.'*\n"
            "4. Use [system_tool id=\"transfer_to_number\" name=\"Transfer to human agent\"] "
            "   to immediately route the call to a human operator.\n\n"
            "### Important Rules\n\n"
            "- Do NOT attempt to answer or provide information about OTP, card unlock, "
            "  card activation, SMS Banking toggle, corporate loans, or L/C.\n"
            "- Do NOT ask the customer for additional information before transferring.\n"
            "- Do NOT hallucinate or fabricate answers for unsupported banking topics.\n"
            "- The tool `toggle_sms_banking` does NOT exist and must NEVER be called.\n"
            "- The tools `send_otp`, `verify_otp`, `execute_card_unlock`, and "
            "  `execute_card_activation` do NOT exist and must NEVER be called.\n"
        ),
    },
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
