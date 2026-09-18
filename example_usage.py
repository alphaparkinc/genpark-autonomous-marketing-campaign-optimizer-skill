"""
Example Usage: GenPark Autonomous Marketing Campaign Optimizer Skill
Demonstrates 360-degree audit, graduated budget reallocation, creative generation,
and approval workflows.
"""

from marketing_optimizer_client import MarketingOptimizerClient, MarketingOptimizerConfig, AutonomyLevel
import json

def main():
    print("=" * 75)
    print("GENPARK AUTONOMOUS MARKETING CAMPAIGN OPTIMIZER AGENT SKILL")
    print("=" * 75)

    # 1. Initialize Client with Act-With-Approval Autonomy
    config = MarketingOptimizerConfig(
        api_key="demo_sandbox_key",
        autonomy_level=AutonomyLevel.ACT_WITH_APPROVAL,
        max_budget_shift_pct=25.0
    )
    client = MarketingOptimizerClient(config)

    # 2. Step 1: 360-Degree Account Audit
    print("\n[Step 1] Running 360-Degree Ad Account Audit...")
    audit = client.audit_accounts(["meta", "google", "tiktok", "ga4"])
    print(f"  -> Total Monthly Spend Analyzed: ${audit['total_monthly_spend_analyzed_usd']:,.2f}")
    print(f"  -> Wasted Spend Detected: ${audit['total_wasted_spend_detected_usd']:,.2f}")
    print(f"  -> Account Health Score: {audit['overall_health_score']}/100")
    print("  -> Key Critical Findings:")
    for issue in audit['key_issues']:
        print(f"     * {issue}")

    # 3. Step 2: Autonomous Budget Optimization (Act-With-Approval)
    print("\n[Step 2] Formulating Autonomous Budget Optimization...")
    decision = client.optimize_budgets()
    print(f"  -> Action ID: {decision['action_id']}")
    print(f"  -> Shift: ${decision['reallocated_amount_daily_usd']}/day from {decision['source_campaign']} -> {decision['destination_campaign']}")
    print(f"  -> Expected ROAS Lift: +{decision['expected_weekly_roas_lift_pct']}%")
    print(f"  -> Status: {decision['status']}")
    print(f"  -> Gated Approval URL: {decision.get('approval_url')}")

    # 4. Step 3: Human-In-The-Loop Approval Execution
    print("\n[Step 3] Simulating One-Tap Human Approval...")
    approved = client.approve_action(decision['action_id'])
    print(f"  -> Final Status: {approved['status']}")
    print(f"  -> Executed At Timestamp: {approved['executed_at']}")

    # 5. Step 4: Autonomous Creative Generation
    print("\n[Step 4] Generating Fresh High-Converting Ad Creatives...")
    creatives = client.generate_creative_variants(
        product_name="EcoClean Zero Waste Detergent",
        value_props=["100% plastic-free packaging", "3x concentrated formula", "cost 40% less per wash"],
        target_audience="Eco-conscious suburban homeowners aged 28-45"
    )
    print(f"  -> Batch ID: {creatives['batch_id']}")
    print(f"  -> Variants Generated: {creatives['variants_generated']}")
    for idx, v in enumerate(creatives['creatives'], 1):
        print(f"     [{idx}] Angle: {v['angle']}")
        print(f"         Headline: {v['headline']}")
        print(f"         Hook: {v['hook']}")

    # 6. Step 5: Reviewing Audit Trail / Activity Log
    print("\n[Step 5] Inspecting Workspace Activity Log...")
    log = client.get_activity_log()
    print(f"  -> Total Events Recorded: {len(log)}")
    for entry in log:
        print(f"     [{entry['type']}] {entry['summary']}")

    print("\n" + "=" * 75)
    print("✓ All Autonomous Marketing workflows executed successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
