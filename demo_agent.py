"""
MiniBase Content Moderation Agent Demo

Demonstrates the agent design from the Agent Purpose Document (06_Agent_Purpose_Document.md).
Validates delegation archetypes, escalation rules, and confidence scoring logic.
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class AgentDecision:
    """Represents the agent's moderation decision."""
    delegation_archetype: str
    action: str
    confidence: float
    rationale: str
    policy_reference: str
    data_sources_checked: list[str]
    escalation_trigger: str | None
    estimated_time_saved: str


class ModerationAgent:
    """
    Implements the moderation logic from Agent Purpose Document.

    This is a rule-based simulation (no LLM calls) to validate whether
    the specification is buildable and complete.
    """

    # Confidence thresholds from Agent Purpose Document Section 6.1
    CONFIDENCE_THRESHOLD_AUTO_ACTION = 0.9
    CONFIDENCE_THRESHOLD_ESCALATE = 0.7

    # Spam patterns from Section 7.1
    SPAM_PATTERNS = {
        'link_farm': {'keywords': ['check out', 'buy now', 'amazing deals'], 'min_urls': 3},
        'gibberish': {'min_consecutive_consonants': 7},
        'off_topic': {'wrong_subforum_keywords': ['buy', 'sell', 'price']}
    }

    def __init__(self):
        self.decisions_log = []

    def classify_post(self, post_data: Dict[str, Any]) -> AgentDecision:
        """
        Main decision function implementing the delegation logic.

        Decision flow from Agent Purpose Document Section 6.1:
        1. Check if Human-Only case (IP claims, bans)
        2. Check escalation triggers (sponsor accounts, watchlist, high engagement)
        3. Classify intent (spam, grey-zone, appeal)
        4. Calculate confidence
        5. Determine delegation archetype
        """

        # Step 1: Human-Only cases
        if self._is_human_only_case(post_data):
            return self._handle_human_only(post_data)

        # Step 2: Check escalation triggers
        escalation_trigger = self._check_escalation_triggers(post_data)
        if escalation_trigger:
            return self._handle_escalation(post_data, escalation_trigger)

        # Step 3: Classify intent
        intent, confidence = self._classify_intent(post_data)

        # Step 4: Route based on intent and confidence
        if intent == "clear_spam" and confidence >= self.CONFIDENCE_THRESHOLD_AUTO_ACTION:
            return self._handle_fully_agentic(post_data, intent, confidence)
        elif intent == "grey_zone" or confidence < self.CONFIDENCE_THRESHOLD_ESCALATE:
            return self._handle_human_led(post_data, intent, confidence)
        else:
            return self._handle_agent_led(post_data, intent, confidence)

    def _is_human_only_case(self, post_data: Dict[str, Any]) -> bool:
        """Check if this requires human-only handling."""
        # IP claims
        if 'claim_id' in post_data:
            return True
        # Ban decisions
        if post_data.get('requires_ban_decision'):
            return True
        return False

    def _check_escalation_triggers(self, post_data: Dict[str, Any]) -> str | None:
        """
        Check escalation triggers from Agent Purpose Document Section 6.3.

        Returns trigger reason if escalation required, None otherwise.
        """
        # Sponsor account (2024 incident precedent)
        if post_data.get('is_sponsor_account'):
            return "Sponsor account - Tom reviews personally (2024 incident)"

        # Watchlist (Tom's pattern tracker)
        if post_data.get('is_on_watchlist'):
            return "User on Tom's watchlist - requires review"

        # High community engagement (>12 reactions)
        if post_data.get('reactions_count', 0) > 12:
            return "High community engagement (>12 reactions) - risky to auto-remove"

        # Subforum-specific norms
        subforum = post_data.get('subforum')
        if subforum == 'painters':
            norms = post_data.get('subforum_norms', {})
            critique_invited = norms.get('critique_invited', False)
            if not critique_invited and 'critique' in post_data.get('content', '').lower():
                return "Painters subforum: critique without invitation - violates norm"

        return None

    def _classify_intent(self, post_data: Dict[str, Any]) -> Tuple[str, float]:
        """
        Classify post intent and return confidence score.

        Returns: (intent, confidence) where intent is one of:
        - 'clear_spam': Link farms, gibberish, obvious violations
        - 'grey_zone': Harsh critique, commercial-adjacent, cultural ambiguity
        - 'appeal': User dispute
        """
        content = post_data.get('content', '').lower()

        # Appeal handling
        if 'appeal' in post_data:
            return ('appeal', 0.95)

        # Clear spam patterns
        url_count = content.count('http')
        spam_keywords = sum(1 for kw in ['buy now', 'check out', 'amazing deals', 'click here'] if kw in content)

        if url_count >= 3 and spam_keywords >= 2:
            # Link farm spam
            confidence = 0.95
            if post_data.get('author_post_count', 0) < 3:
                confidence = 0.98  # New user + spam pattern = very high confidence
            return ('clear_spam', confidence)

        # Grey-zone: harsh critique
        flag_reasons = post_data.get('flagged_reasons', [])
        harassment_flags = flag_reasons.count('harassment')

        if harassment_flags >= 3:
            # High flag count for harassment, but check context
            author_reputation = post_data.get('author_reputation', 0)
            if author_reputation > 50:
                # Established user - likely harsh but legitimate critique
                return ('grey_zone', 0.65)
            else:
                # Low reputation + harassment flags
                return ('grey_zone', 0.72)

        # Default: needs review
        return ('grey_zone', 0.60)

    def _handle_fully_agentic(self, post_data: Dict[str, Any], intent: str, confidence: float) -> AgentDecision:
        """Fully Agentic: Agent removes without human approval."""
        return AgentDecision(
            delegation_archetype="🤖 Fully Agentic",
            action="AUTO-REMOVE",
            confidence=confidence,
            rationale=f"Clear spam detected: {post_data.get('content', '')[:100]}... Pattern matches link farm with {post_data.get('content', '').count('http')} URLs and spam keywords.",
            policy_reference="Rule 3: No spam or self-promotion",
            data_sources_checked=[
                "Post content (pattern matching)",
                f"Author history ({post_data.get('author_post_count', 0)} posts)",
                f"Flag count ({post_data.get('flag_count', 0)} flags)",
                f"Subforum ({post_data.get('subforum', 'unknown')})"
            ],
            escalation_trigger=None,
            estimated_time_saved="30 seconds (moderator would have removed immediately)"
        )

    def _handle_agent_led(self, post_data: Dict[str, Any], intent: str, confidence: float) -> AgentDecision:
        """Agent-Led: Agent proposes action, human approves."""
        return AgentDecision(
            delegation_archetype="🤝 Agent-Led with Oversight",
            action="PROPOSE REMOVAL (requires human approval)",
            confidence=confidence,
            rationale=f"Edge case spam - confidence {confidence:.2f} above escalation threshold (0.70) but below auto-action (0.90). Recommending removal but flagging for review.",
            policy_reference="Rule 3: No spam or self-promotion",
            data_sources_checked=[
                "Post content (pattern matching)",
                f"Author history ({post_data.get('author_post_count', 0)} posts, {post_data.get('author_account_age_days', 0)} days old)",
                f"Flag reasons: {', '.join(post_data.get('flagged_reasons', []))}",
                f"Subforum norms ({post_data.get('subforum', 'unknown')})"
            ],
            escalation_trigger="Confidence in grey zone (0.70-0.90) - requires human approval",
            estimated_time_saved="3 minutes (agent gathers context, human reviews in 30 sec vs 3 min full investigation)"
        )

    def _handle_human_led(self, post_data: Dict[str, Any], intent: str, confidence: float) -> AgentDecision:
        """Human-Led: Agent gathers context, human decides."""

        if intent == 'appeal':
            context = self._gather_appeal_context(post_data)
            return AgentDecision(
                delegation_archetype="👤 Human-Led with Agent Support",
                action="CONTEXT GATHERED - Human decides",
                confidence=confidence,
                rationale=f"User appeal case. Agent gathered context but does not recommend action. Human must review original removal decision and appeal justification.",
                policy_reference="Appeals process (Section 4.3)",
                data_sources_checked=[
                    "Original moderation action",
                    f"Original rationale: {post_data.get('moderation_history', [{}])[0].get('rationale', 'N/A')}",
                    f"Appeal reason: {post_data.get('appeal', {}).get('reason', 'N/A')}",
                    f"Community support: {post_data.get('reactions_count', 0)} reactions",
                    f"Author reputation: {post_data.get('author_reputation', 0)}"
                ],
                escalation_trigger="User appeal - requires human judgment on original decision",
                estimated_time_saved="5 minutes (agent gathers all context, human reviews in 3 min vs 8 min manual gathering)"
            )
        else:
            # Grey-zone case
            return AgentDecision(
                delegation_archetype="👤 Human-Led with Agent Support",
                action="ESCALATE TO MODERATOR - Grey-zone case",
                confidence=confidence,
                rationale=f"Grey-zone case with confidence {confidence:.2f} (below 0.70 threshold). Harsh critique detected with {post_data.get('flagged_reasons', []).count('harassment')} harassment flags, but author has {post_data.get('author_reputation', 0)} reputation. Requires human judgment on tone vs. harassment distinction.",
                policy_reference="Rule 4: No harassment or personal attacks",
                data_sources_checked=[
                    "Post content (harassment pattern detection)",
                    f"Author reputation: {post_data.get('author_reputation', 0)}",
                    f"Subforum norms: {post_data.get('subforum', 'unknown')}",
                    f"Parent post context: {post_data.get('parent_post_content', 'N/A')[:100]}",
                    f"Critique invited: {post_data.get('subforum_norms', {}).get('critique_invited', False)}"
                ],
                escalation_trigger="Low confidence - harsh critique vs. harassment requires cultural judgment",
                estimated_time_saved="2 minutes (agent gathers context from 4 systems, human reviews in 3 min vs 5 min)"
            )

    def _handle_escalation(self, post_data: Dict[str, Any], escalation_trigger: str) -> AgentDecision:
        """Handle cases with explicit escalation triggers."""
        return AgentDecision(
            delegation_archetype="🤝 Agent-Led with Oversight",
            action="ESCALATE TO TOM - Special handling required",
            confidence=0.0,  # N/A for escalations
            rationale=f"Escalation trigger activated: {escalation_trigger}. Agent gathered context but does not recommend action due to special account status.",
            policy_reference="Escalation policy (Section 6.3)",
            data_sources_checked=[
                f"Sponsor account status: {post_data.get('is_sponsor_account', False)}",
                f"Watchlist status: {post_data.get('is_on_watchlist', False)}",
                f"Community engagement: {post_data.get('reactions_count', 0)} reactions",
                "Post content and flag reasons"
            ],
            escalation_trigger=escalation_trigger,
            estimated_time_saved="0 minutes (Tom must review personally - agent provides context packaging)"
        )

    def _handle_human_only(self, post_data: Dict[str, Any]) -> AgentDecision:
        """Handle Human-Only cases where agent has no role."""

        if 'claim_id' in post_data:
            return AgentDecision(
                delegation_archetype="⛔ Human-Only (No Agent Role)",
                action="NO AGENT ACTION - Tom handles",
                confidence=0.0,  # N/A
                rationale=f"IP claim from {post_data.get('claimant_name', 'unknown')}. This is a legal matter requiring human judgment. Agent has no role in IP claim resolution.",
                policy_reference="IP Claims Policy (DMCA compliance)",
                data_sources_checked=[
                    f"Claimant: {post_data.get('claimant_name', 'N/A')}",
                    f"Claim type: {post_data.get('claim_type', 'N/A')}",
                    f"Evidence provided: {len(post_data.get('evidence_urls', []))} URLs",
                    f"Claimant history: {post_data.get('claimant_history', {}).get('previous_claims_valid', 0)}/{post_data.get('claimant_history', {}).get('previous_claims_count', 0)} valid claims"
                ],
                escalation_trigger="IP claim - legal sensitivity, requires Tom's review",
                estimated_time_saved="0 minutes (agent cannot assist with legal decisions)"
            )

        return AgentDecision(
            delegation_archetype="⛔ Human-Only (No Agent Role)",
            action="NO AGENT ACTION",
            confidence=0.0,
            rationale="This case type is outside agent scope.",
            policy_reference="N/A",
            data_sources_checked=[],
            escalation_trigger="Human-only case type",
            estimated_time_saved="0 minutes"
        )

    def _gather_appeal_context(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gather context for appeal cases."""
        return {
            'original_action': post_data.get('moderation_history', [{}])[0],
            'appeal_reason': post_data.get('appeal', {}).get('reason'),
            'community_support': post_data.get('reactions_count', 0),
            'author_standing': post_data.get('author_reputation', 0)
        }


def load_fixture(fixture_name: str) -> Dict[str, Any]:
    """Load test fixture from tests/fixtures directory."""
    fixture_path = Path(__file__).parent / "tests" / "fixtures" / fixture_name
    with open(fixture_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def display_decision(decision: AgentDecision, post_data: Dict[str, Any]):
    """Display agent decision in pretty-printed format."""

    st.markdown("---")
    st.markdown("### 🎯 Agent Decision")

    # Delegation Archetype (prominent)
    st.markdown(f"## {decision.delegation_archetype}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Action:**")
        if "AUTO-REMOVE" in decision.action:
            st.error(decision.action)
        elif "ESCALATE" in decision.action or "PROPOSE" in decision.action:
            st.warning(decision.action)
        elif "NO AGENT ACTION" in decision.action:
            st.info(decision.action)
        else:
            st.success(decision.action)

    with col2:
        st.markdown("**Confidence Score:**")
        if decision.confidence > 0:
            st.metric("Confidence", f"{decision.confidence:.2%}")
        else:
            st.info("N/A (escalation case)")

    st.markdown("**Rationale:**")
    st.write(decision.rationale)

    st.markdown("**Policy Reference:**")
    st.code(decision.policy_reference)

    st.markdown("**Data Sources Checked:**")
    for source in decision.data_sources_checked:
        st.markdown(f"- {source}")

    if decision.escalation_trigger:
        st.markdown("**Escalation Trigger:**")
        st.warning(f"⚠️ {decision.escalation_trigger}")

    st.markdown("**Estimated Time Saved:**")
    st.success(f"⏱️ {decision.estimated_time_saved}")

    # Show raw post data in expander
    with st.expander("📄 View Raw Post Data"):
        st.json(post_data)


def main():
    st.set_page_config(page_title="MiniBase Moderation Agent Demo", layout="wide")

    st.title("🛡️ MiniBase Content Moderation Agent")
    st.markdown("### Demonstration of Agent Purpose Document (Week 2 Deliverable)")

    st.markdown("""
    This demo validates that the Agent Purpose Document is **buildable** by implementing
    its delegation logic, escalation rules, and confidence scoring without LLM calls.

    **Purpose:** Prove the specification has enough detail to implement the agent.

    **Methodology:** Rule-based simulation using test fixtures.
    """)

    st.markdown("---")

    # Use cases
    st.markdown("## 📋 Select a Use Case")

    use_cases = [
        {
            "name": "🔴 Link Farm Spam (Fully Agentic)",
            "description": "Obvious spam with multiple URLs - should auto-remove",
            "fixture": "spam_linkfarm.json",
            "delegation": "Fully Agentic"
        },
        {
            "name": "🟡 Harsh Critique in Painters Sub (Agent-Led)",
            "description": "Grey-zone case - harsh critique with harassment flags but invited",
            "fixture": "greyzone_harsh_critique.json",
            "delegation": "Agent-Led with Oversight"
        },
        {
            "name": "🟢 User Appeal (Human-Led)",
            "description": "User disputes removal - agent gathers context, human decides",
            "fixture": "appeal_example.json",
            "delegation": "Human-Led with Agent Support"
        },
        {
            "name": "⚫ IP Claim (Human-Only)",
            "description": "Legal matter - agent has no role",
            "fixture": "ip_claim.json",
            "delegation": "Human-Only"
        }
    ]

    col1, col2, col3, col4 = st.columns(4)

    selected_case = None

    with col1:
        if st.button(use_cases[0]["name"], use_container_width=True):
            selected_case = use_cases[0]

    with col2:
        if st.button(use_cases[1]["name"], use_container_width=True):
            selected_case = use_cases[1]

    with col3:
        if st.button(use_cases[2]["name"], use_container_width=True):
            selected_case = use_cases[2]

    with col4:
        if st.button(use_cases[3]["name"], use_container_width=True):
            selected_case = use_cases[3]

    # Display results
    if selected_case:
        st.markdown(f"### Selected Case: {selected_case['name']}")
        st.info(f"**Expected Delegation:** {selected_case['delegation']}")
        st.write(selected_case['description'])

        # Load fixture and run agent
        try:
            post_data = load_fixture(selected_case['fixture'])
            agent = ModerationAgent()
            decision = agent.classify_post(post_data)

            # Display decision
            display_decision(decision, post_data)

            # Validation check
            st.markdown("---")
            st.markdown("### ✅ Validation Check")
            if selected_case['delegation'] in decision.delegation_archetype:
                st.success(f"✅ PASS: Agent correctly applied '{selected_case['delegation']}' archetype")
            else:
                st.error(f"❌ FAIL: Expected '{selected_case['delegation']}' but got '{decision.delegation_archetype}'")
                st.warning("⚠️ This indicates a gap in the Agent Purpose Document specification!")

        except FileNotFoundError:
            st.error(f"❌ Fixture file not found: {selected_case['fixture']}")
            st.info("Run from project root: `streamlit run demo_agent.py`")
        except Exception as e:
            st.error(f"❌ Error processing case: {str(e)}")
            st.exception(e)

    # Footer
    st.markdown("---")
    st.markdown("""
    **About this demo:**
    - Implements logic from `Specification/06_Agent_Purpose_Document.md`
    - Uses test fixtures from `tests/fixtures/`
    - No LLM calls (pure rule-based logic)
    - Validates delegation boundaries, escalation triggers, confidence thresholds

    **Closed Build Loop Goal:** Expose gaps in the specification where the document
    doesn't provide enough detail to implement the agent confidently.
    """)


if __name__ == "__main__":
    main()
