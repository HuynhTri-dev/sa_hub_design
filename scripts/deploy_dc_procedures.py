import json
import os
import sys
import urllib.request
import urllib.error
import time

AGENT_ID = "agent_0001m0sdr3gzec7ry39y5fbg4dhn"
BRANCH_ID = "agtbrch_5401m0sdr437e3nbwa095dkx4pkh"

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
        "name": "get_debt_info",
        "description": "Lấy thông tin khoản nợ hiện tại và các biến trạng thái (state variables) của khách hàng.",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/debt/customer/{customerId}/status",
            "method": "GET",
            "path_params_schema": {
                "customerId": {"type": "string", "description": "The customer ID returned from verify_customer_id.", "is_system_provided": False, "is_omitted": False}
            }
        }
    },
    {
        "type": "webhook",
        "name": "update_debt_status",
        "description": "Cập nhật thông tin khách hàng cung cấp vào hệ thống CRM (ghi nhận PTP).",
        "api_schema": {
            "kind": "webhook",
            "url": "https://backend-banking-core.vercel.app/api/v1/debt/customer/{customerId}/status",
            "method": "PATCH",
            "path_params_schema": {
                "customerId": {"type": "string", "description": "The customer ID", "is_system_provided": False, "is_omitted": False}
            },
            "request_body_schema": {
                "type": "object",
                "properties": {
                    "confirm": {"type": "boolean", "description": "Customer confirmed the debt"},
                    "reason": {"type": "string", "description": "Reason for late payment"},
                    "solution": {"type": "string", "description": "Proposed solution for the debt"},
                    "promise_amount": {"type": "number", "description": "Promised payment amount"},
                    "promise_date": {"type": "string", "description": "Promised payment date"}
                }
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

PROCEDURES = [
    {
        "name": "Thu Thập Thông Tin PTP (Bảng Tích)",
        "type": "free_form",
        "trigger": "Khách hàng đã xác nhận đúng thông tin khoản nợ và đồng ý trao đổi tiếp.",
        "content": """
Bạn có nhiệm vụ thu thập thông tin Cam kết thanh toán (PTP) từ khách hàng. Hãy hoạt động như một "bảng kiểm" (checklist) để thu thập thông tin còn thiếu. 

LUÔN kiểm tra các thông tin đã biết trước khi hỏi để TRÁNH HỎI LẶP LẠI. 
Nếu khách hàng cung cấp nhiều thông tin cùng lúc, hãy ghi nhận tất cả và chỉ hỏi những gì CÒN THIẾU.

Các thông tin cần thu thập (Bảng tích):
1. **Lý do quá hạn (reason):**
   - Nếu chưa có: Hỏi "Dạ anh/chị cho em hỏi hiện tại mình đang gặp khó khăn gì mà chưa thể thanh toán khoản nợ này đúng hạn ạ?"
2. **Phương án xử lý (solution):**
   - Nếu chưa có: Đàm phán phương án. Nhấn mạnh: "Nếu không thanh toán, ngân hàng sẽ buộc phải phát mãi tài sản bảo đảm. Vậy anh/chị dự định phương án giải quyết sắp tới như thế nào ạ?"
3. **Số tiền cam kết nộp (promise_amount):**
   - Nếu chưa có: Hỏi "Dạ vậy anh/chị có thể nộp vào số tiền bao nhiêu để em ghi nhận lên hệ thống ạ?"
4. **Ngày giờ cam kết nộp (promise_date):**
   - Nếu chưa có: Hỏi "Dạ anh/chị dự kiến sẽ nộp số tiền này vào thời gian nào (ngày nào) để em tạo lịch hẹn ạ?"

HÀNH ĐỘNG KẾT THÚC:
- Sau khi đã thu thập ĐỦ 4 thông tin trên, BẮT BUỘC gọi tool `update_debt_status` để đẩy dữ liệu về hệ thống.
- Sau đó, cảm ơn và dặn dò khách hàng thanh toán đúng hạn.
"""
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
