"""
GenPark Autonomous Marketing Campaign Optimizer Model Context Protocol (MCP) Server
Exposes autonomous marketing capabilities as standard MCP tools for Claude Desktop, Cursor, and AI agents.
"""

import json
import sys
from marketing_optimizer_client import MarketingOptimizerClient, MarketingOptimizerConfig, AutonomyLevel

client = MarketingOptimizerClient()

MCP_TOOLS = [
    {
        "name": "marketing_audit_accounts",
        "description": "Perform 360-degree audit across Meta, Google, TikTok, and GA4 to detect ad fatigue and wasted spend.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ad channels to audit: meta, google, tiktok, ga4, shopify"
                }
            }
        }
    },
    {
        "name": "marketing_optimize_budgets",
        "description": "Calculate and execute ROAS-maximizing cross-channel budget shifts with graduated autonomy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_shift_pct": {
                    "type": "number",
                    "description": "Max percentage of daily budget to reallocate (default: 20.0)"
                }
            }
        }
    },
    {
        "name": "marketing_approve_action",
        "description": "Approve and execute a gated marketing action (such as budget shifts or campaign scaling).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action_id": {"type": "string", "description": "The unique ID of the pending marketing action"}
            },
            "required": ["action_id"]
        }
    },
    {
        "name": "marketing_generate_creatives",
        "description": "Generate high-converting multi-channel ad copy variants and creative hooks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string"},
                "value_props": {"type": "array", "items": {"type": "string"}},
                "target_audience": {"type": "string"},
                "channels": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["product_name", "value_props", "target_audience"]
        }
    },
    {
        "name": "marketing_get_activity_log",
        "description": "Retrieve the full audit log of perceive-decide-act marketing events.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_mcp_request(request: dict) -> dict:
    method = request.get("method")
    req_id = request.get("id")

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}

    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        try:
            if tool_name == "marketing_audit_accounts":
                res = client.audit_accounts(args.get("channels"))
            elif tool_name == "marketing_optimize_budgets":
                res = client.optimize_budgets(args.get("max_shift_pct"))
            elif tool_name == "marketing_approve_action":
                res = client.approve_action(args["action_id"])
            elif tool_name == "marketing_generate_creatives":
                res = client.generate_creative_variants(
                    args["product_name"],
                    args["value_props"],
                    args["target_audience"],
                    args.get("channels")
                )
            elif tool_name == "marketing_get_activity_log":
                res = client.get_activity_log()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                }
            }
        except Exception as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def run_mcp_server():
    print("GenPark Autonomous Marketing MCP Server running (stdio mode)...", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_mcp_request(req)
            print(json.dumps(resp))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    run_mcp_server()
