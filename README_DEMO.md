# MiniBase Moderation Agent Demo

This demo validates the Agent Purpose Document (`Specification/06_Agent_Purpose_Document.md`) by implementing its delegation logic.

## Purpose

**Validate the Agent Purpose Document is buildable** - does it contain enough detail to implement the agent's decision logic without ambiguity?

This is part of the Week 2 "closed build loop" requirement: build what you can, identify gaps, diagnose them, revise the specification.

## What This Demo Does

- Implements the 4 delegation archetypes (Fully Agentic, Agent-Led, Human-Led, Human-Only)
- Applies escalation rules (sponsor accounts, watchlist, high engagement, subforum norms)
- Calculates confidence scores and routes decisions accordingly
- Shows delegation info, rationale, data sources checked, and time saved

## What This Demo Does NOT Do

- No LLM calls (pure rule-based logic)
- No real API integration (uses mock fixtures)
- No production accuracy validation (limited test cases)
- No human-in-the-loop workflow (no approval UI)

## Running the Demo

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Demo

```bash
streamlit run demo_agent.py
```

This will open a browser window with the demo interface.

### Using the Demo

1. Click one of the 4 use case buttons:
   - **Link Farm Spam** - Tests Fully Agentic archetype (auto-remove)
   - **Harsh Critique** - Tests Agent-Led archetype (propose removal, require approval)
   - **User Appeal** - Tests Human-Led archetype (context gathering only)
   - **IP Claim** - Tests Human-Only archetype (no agent role)

2. Review the agent's decision:
   - Delegation archetype applied
   - Action taken/proposed
   - Confidence score
   - Rationale and policy reference
   - Data sources checked
   - Escalation trigger (if any)
   - Estimated time saved

3. Check validation:
   - Does the agent apply the correct delegation archetype?
   - If not, this indicates a gap in the Agent Purpose Document

## Test Fixtures

Located in `tests/fixtures/`:
- `spam_linkfarm.json` - Clear spam (new user, 3+ URLs, spam keywords)
- `greyzone_harsh_critique.json` - Harsh critique in painters subforum (critique invited)
- `appeal_example.json` - User appeals removal of GW pricing criticism (47 reactions)
- `ip_claim.json` - Copyright claim from SculptureDragon (established sculptor)

## Expected Outcomes

### Link Farm Spam
- **Delegation:** Fully Agentic
- **Action:** AUTO-REMOVE
- **Confidence:** >0.90
- **Time saved:** 30 seconds

### Harsh Critique
- **Delegation:** Human-Led with Agent Support
- **Action:** ESCALATE TO MODERATOR
- **Confidence:** 0.65 (below 0.70 threshold)
- **Time saved:** 2 minutes (context gathering)

### User Appeal
- **Delegation:** Human-Led with Agent Support
- **Action:** CONTEXT GATHERED
- **Confidence:** 0.95
- **Time saved:** 5 minutes (context gathering)

### IP Claim
- **Delegation:** Human-Only
- **Action:** NO AGENT ACTION
- **Confidence:** N/A
- **Time saved:** 0 minutes (agent cannot assist)

## Validation Questions

As you run the demo, ask:

1. **Is the logic clear?** Can you understand why the agent made each decision?
2. **Are escalation rules complete?** Did you encounter cases where you weren't sure when to escalate?
3. **Are confidence thresholds justified?** Do 0.7 and 0.9 seem right, or should they be adjusted?
4. **Is the delegation mapping unambiguous?** Is it clear which archetype applies to each case?
5. **What's missing?** What information does the agent need that isn't in the fixtures?

## Gaps Found (To Be Updated)

Use this section to document gaps found during the closed build loop:

- [ ] **Gap 1:** [Description of specification ambiguity]
- [ ] **Gap 2:** [Missing escalation rule or confidence threshold]
- [ ] **Gap 3:** [Data requirement not specified]

These gaps will inform revisions to the Agent Purpose Document.

## Next Steps

1. Run demo with all 4 use cases
2. Document gaps in specification
3. Revise `Specification/06_Agent_Purpose_Document.md` to address gaps
4. Re-run demo to verify fixes
5. Expand test fixtures if needed (commercial posts, cultural ambiguity, etc.)
