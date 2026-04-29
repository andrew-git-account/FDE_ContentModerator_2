# Problem Statement and Success Metrics

**Project**: MiniBase Community Content Moderation Agent  
**Scenario**: FDE Program Week 2 - Scenario 4  
**Date**: 2026-04-29  
**Version**: 1.0

---

## Executive Summary

MiniBase's hybrid moderation team is at capacity handling ~1,500 posts/day that enter the moderation queue. The team's total effort is ~47 hours/day with no ability to scale linearly due to volunteer constraints. This project aims to automate routine spam removal (72% of queue, 9 hrs/day effort) to free moderator capacity for grey-zone cases requiring human judgment, while maintaining zero viral false negatives and preserving community norms.

**Primary Goal**: Reduce routine spam handling from 9 hrs/day to <2 hrs/day (77% reduction) while maintaining safety bar.

**Risk Constraint**: "False positives are survivable; one viral false negative is existential."

---

## Problem Statement

### Business Context

**MiniBase** is a UK-incorporated tabletop-miniature hobbyist community platform with:
- ~180,000 active users (mostly UK, Western Europe, North America, Japan, Australia)
- 12,000 posts/day across 14 sub-forums plus gallery section
- £1.4M/year revenue from premium memberships, gallery commissions, and sponsored content
- Hybrid moderation team: 8 volunteer moderators + 2 paid staff (Community Manager Tom + Senior Moderator)

Of the ~12K daily posts, 12.5% (~1,500/day) enter the moderation queue via user flags, automated detection, or moderator sampling.

### Core Constraints

#### 1. Capacity Bottleneck

**Current state**: The moderation team operates at maximum capacity with 47 hours/day of effort distributed across:

| Work Stream | Volume (daily) | Time per case | Total effort | % of queue |
|-------------|----------------|---------------|--------------|------------|
| Routine spam / clear violations | 1,080 | 30 sec | 9 hrs | 72% |
| Grey-zone case review | 360 | 5 min | 30 hrs | 24% |
| User dispute appeals | 60 | 8 min | 8 hrs | 4% |
| IP-claim resolution | 3-5/week | 30 min | ~2 hrs/week | <1% |

**The problem**: 72% of the queue (1,080 posts/day) is routine spam consuming 9 hours/day of moderator time. This prevents focus on the 24% grey-zone cases (360 posts/day, 30 hours/day) that require genuine human judgment and shape community trust.

**Impact**: Moderators spend 60% of their time on repetitive spam removal instead of nuanced decisions that determine platform reputation.

#### 2. Risk Asymmetry

**Stakeholder brief from Tom (Community Manager)**: "False positives are survivable; one viral false negative is existential."

The platform's reputation and revenue depend on:
- Catching harmful content (harassment, doxxing, hate speech) before it spreads
- Tolerating community-appropriate harsh critique (hobbyist culture values direct feedback)
- Avoiding censorship perception (wrongly removing legitimate content can go viral)

**Asymmetric consequences**:
- False positive (wrongly remove legitimate post): User complains, moderator restores, community forgives
- False negative (miss harmful content): Viral incident, community trust erosion, sponsor/revenue risk, potential existential threat

This asymmetry creates high cognitive load on every moderation decision, even routine ones.

#### 3. Volunteer Model Constraint

**Team composition**:
- 8 volunteers across time zones (US, UK, Germany, Australia, Japan) donate limited hours
- 2 paid staff coordinate but cannot replace volunteer domain expertise
- Cannot scale by hiring (budget + volunteer community model)

**Burnout risk**: Volunteers joined to make nuanced cultural/artistic judgments, not to remove link-farm spam 60% of their time. Current workload allocation erodes volunteer satisfaction and retention.

#### 4. Complexity in Lived Work

The 14-page moderation policy is the **documented** work. The **lived** work includes:

**Subforum-specific norms** (not in global policy):
- **Painters sub**: "No critique without invitation" — critique is acceptable only in threads explicitly asking for feedback
- **Historical sub**: More permissive on historically-charged imagery (WWII miniatures, etc.)
- **Japanese painters sub**: English-language critiques may read harsher than intended; require cultural interpretation

**High-risk pattern tracking** (Tom's Google Sheet):
- Sponsor accounts require Tom's personal review (after "2024 sponsor incident")
- Established sculptors (@sculpturedragon) get full IP-claim review every time
- Users with multiple returns in short timeframes are watched for fraud patterns

**Informal coordination** (Discord volunteer channel):
- Edge case discussions between volunteer moderators
- Inconsistent interpretations of grey-zone cases
- No formal record of precedent decisions

**The gap**: An agent built from the 14-page policy alone will be built for an imaginary organization and will fail on real cases.

#### 5. Coordination Overhead

Current workflow inefficiencies:
- Volunteer moderators discuss edge cases in Discord (no structured escalation)
- Tom personally reviews patterns tracked in Google Sheets (not integrated with moderation queue)
- IP claims arrive via email, separate from post moderation workflow
- No formal handoff protocol between time zones

**Result**: Decisions are inconsistent, precedents are lost, and coordination consumes 5-10% of total moderator time.

### Business Impact if Unsolved

**Immediate impacts**:
- Volunteer moderator burnout → reduced coverage → moderation delays → community trust erosion
- Cannot handle platform growth (180K users growing) without degrading quality
- High-value moderator time consumed by low-value spam work

**Revenue risks**:
- £1.4M/year depends on premium memberships (community trust) and sponsor relationships (sensitive to moderation errors)
- One viral false negative could damage sponsors, drive premium member cancellations, create legal exposure

**Strategic risk**:
- Competitors with better moderation efficiency can scale faster
- Unable to expand to new geographic markets without proportional moderator hiring

### The Opportunity

**Hypothesis**: Automate routine spam removal (high volume, low judgment) to free moderator capacity for grey-zone cases (high judgment, high value).

**Specific opportunity**:
- Automate 70-80% of routine spam (1,080 posts/day)
- Reduce spam handling from 9 hrs/day to <2 hrs/day
- Redirect 7 hours/day to grey-zone cases requiring human judgment
- Maintain zero viral false negatives through aggressive escalation on ambiguous cases

---

## Success Metrics

### Primary Metrics (Business Value)

These metrics directly measure whether the agent delivers the promised value.

#### 1. Moderator Time Savings

**Definition**: Reduction in human moderator hours spent on routine spam removal.

- **Current baseline**: 9 hrs/day on routine spam (1,080 posts × 30 sec average)
- **Target**: <2 hrs/day (77% reduction)
- **Acceptable range**: 60-80% reduction (allows for sampling, edge cases, and calibration)
- **Measurement**: Agent-handled cases × average time saved per case, validated by weekly moderator time-tracking surveys

**Why this matters**: This is the primary value lever. Freeing 7 hrs/day of moderator capacity enables better outcomes on grey-zone cases.

#### 2. Grey-Zone Case Quality Time

**Definition**: Increase in moderator time allocated to grey-zone cases requiring nuanced judgment.

- **Current baseline**: 30 hrs/day across 360 cases = 5 min/case average
- **Target**: +7 hrs/day reallocated from spam = 37 hrs/day = 6.2 min/case
- **Measured by**: Human moderator time distribution before/after agent deployment (weekly surveys)
- **Goal**: Better outcomes on complex cases, not just faster processing

**Why this matters**: The real value isn't efficiency — it's redirecting human attention to where it matters most. Grey-zone decisions shape community trust and platform reputation.

#### 3. Throughput at Capacity

**Definition**: Total posts handled per day without adding moderators.

- **Current baseline**: 1,500 posts/day with team at 47 hrs/day capacity
- **Target**: 2,000+ posts/day at same capacity (33% growth headroom)
- **Measured by**: Daily post volume processed without increasing team hours
- **Goal**: Platform can grow user base without proportional moderation team growth

**Why this matters**: Demonstrates scalability. If the agent enables 33% growth without new hires, it proves the economic model.

### Quality and Safety Metrics (Non-Negotiable)

These metrics establish the safety bar. **Cannot be compromised for efficiency gains.**

#### 4. Moderation Accuracy

**Definition**: Correctness of agent decisions on routine spam.

- **Routine spam precision**: ≥95% (false positive rate ≤5%)
- **Routine spam recall**: ≥90% (false negative rate ≤10%)
- **Grey-zone escalation**: 100% of grey-zone cases routed to human review (no auto-removal)
- **Measured by**: Daily human audit of 50 random agent decisions (stratified sample across confidence bands)

**Why this matters**: Precision protects community trust (don't remove legitimate content). Recall protects platform safety (don't miss harmful content). Grey-zone escalation enforces the delegation boundary.

#### 5. False Negative Rate (Viral Risk)

**Definition**: Harmful content that the agent approves/misses, reaching the community.

- **Target**: Zero viral false negatives (harmful content spreading at scale)
- **Acceptable**: ≤0.1% false negative rate on clear policy violations (harassment, doxxing, hate speech)
- **Measured by**: Community reports of agent-approved harmful content + human audit
- **Consequence threshold**: One viral false negative = project failure

**This is the existential risk metric.** From Tom's brief: "one viral false negative is existential." Cannot be traded for efficiency, cost, or coverage.

**Risk mitigation**:
- Agent biases toward escalation on ambiguous cases
- Confidence threshold kept high (≥0.7 for auto-action)
- Sponsor accounts, high-engagement posts always escalated

#### 6. Subforum Norm Compliance

**Definition**: Correct application of subforum-specific moderation rules.

- **Target**: 100% compliance with subforum-specific norms
- **Examples**:
  - Painters sub: Critique without invitation → escalate (not auto-approve)
  - Historical sub: Historically-charged imagery → apply permissive standard
  - Japanese sub: English critiques → flag cultural interpretation issues
- **Measured by**: Moderator override rate by subforum (overrides indicate norm violations)

**Why this matters**: Subforum norms are the **lived work** that distinguishes MiniBase's culture. Violating these norms erodes community trust as much as missing harmful content.

### Operational Metrics (Agent Performance)

These metrics measure how well the agent performs its defined role.

#### 7. Coverage Rate

**Definition**: Percentage of routine spam handled without human intervention.

- **Target**: 70-80% of routine spam automated
- **Measured by**: (Agent auto-actions) / (Total routine spam cases)
- **Remaining 20-30%**: Escalated for human review (sampling, low confidence, edge cases)

**Why this matters**: Demonstrates value delivery. 70-80% automation justifies the investment while maintaining safety through sampling and edge-case escalation.

#### 8. Escalation Precision

**Definition**: Proportion of escalations that human moderators agree were justified.

- **Target**: ≥90% of escalations are useful (human agrees case needed review)
- **Measured by**: Human moderator assessment of escalated cases (weekly review)
- **Failure modes**:
  - Over-escalation: Defeats the efficiency purpose, creates moderator fatigue
  - Under-escalation: Misses grey-zone cases, increases false negative risk

**Why this matters**: High escalation precision means the agent correctly identifies the delegation boundary. Low precision means wasted moderator time on unnecessary reviews.

#### 9. Confidence Calibration

**Definition**: Agent confidence scores correlate with actual accuracy.

- **Target**: When agent reports 0.9 confidence, accuracy is 90%±5%
- **Measured by**: Accuracy within each confidence band (0.5-0.6, 0.6-0.7, 0.7-0.8, 0.8-0.9, 0.9+) across 100+ decisions per band
- **Calibration check**: Monthly review, recalibrate thresholds as needed

**Why this matters**: Confidence scores determine escalation thresholds. Well-calibrated confidence enables dynamic delegation (high confidence → auto-act, low confidence → escalate). Poor calibration creates either over-escalation (inefficient) or under-escalation (unsafe).

#### 10. Response Time

**Definition**: Time from flag to agent action.

- **Current baseline**: ~15-30 min average human response time (varies by time zone coverage)
- **Target**: <5 min for routine spam (flagged and removed)
- **Measured by**: Timestamp delta between flag and agent action
- **Impact**: Reduces spam visibility to community (better user experience)

**Why this matters**: Fast response on clear violations improves perceived moderation quality. However, speed must not compromise accuracy.

### Team Sustainability Metrics (Volunteer Health)

These metrics measure impact on the volunteer moderator team.

#### 11. Volunteer Moderator Time Allocation

**Definition**: How moderators spend their time (spam vs. grey-zone vs. coordination).

- **Current baseline**: ~60% routine spam, ~35% grey-zone, ~5% coordination
- **Target**: ~20% routine spam (sampling/oversight), ~70% grey-zone, ~10% coordination
- **Measured by**: Weekly volunteer time-tracking surveys
- **Goal**: Volunteers spend time on judgment work they value, not repetitive spam

**Why this matters**: Volunteer satisfaction and retention. If volunteers feel their expertise is wasted on spam, they burn out and leave.

#### 12. Moderator Override Rate

**Definition**: Frequency of human moderators reversing or correcting agent decisions.

- **Target**: <10% of agent actions overridden
- **Measured by**: Human moderator corrections/reversals logged in system
- **High override rate indicates**: Poor agent calibration, missed norms, or incorrect delegation boundaries

**Why this matters**: Overrides create rework (inefficient) and erode moderator trust in the agent ("I have to double-check everything anyway").

#### 13. Time-to-Escalation-Resolution

**Definition**: How quickly humans resolve cases escalated by the agent.

- **Target**: Escalated cases resolved within 30 min (not slower than current baseline)
- **Measured by**: Timestamp delta between agent escalation and human decision
- **Goal**: Agent context-gathering speeds up human decisions (not creates backlog)

**Why this matters**: If escalations slow down human decisions, the agent creates a bottleneck instead of value. Good escalations include complete context so humans can decide quickly.

### Cost Metrics (Economics)

These metrics establish economic viability.

#### 14. Cost per Case

**Definition**: Direct cost (tokens + infrastructure) to process one case.

- **Routine spam target**: <£0.05/case
- **Grey-zone triage target**: <£0.10/case (context gathering only, human decides)
- **Measured by**: Total monthly cost / cases handled
- **Compared to**: Equivalent human moderator time at £15-20/hr blended rate (volunteers valued at opportunity cost)

**Why this matters**: Economic justification. If agent costs more than human moderators, it doesn't create value unless it enables outcomes humans can't achieve (e.g., 24/7 coverage, 5-min response time).

#### 15. ROI (Return on Investment)

**Definition**: Value created (moderator time saved) relative to cost (agent operation).

- **Target**: 3:1 value/cost ratio (£3 moderator time saved per £1 agent cost)
- **Measured by**: (Moderator hours saved × blended rate) / (Agent operational cost)
- **Acceptable**: 2:1 minimum (still economically justified)

**Calculation example**:
- Agent automates 800 cases/day at £0.05/case = £40/day cost
- Saves 7 hrs/day moderator time at £18/hr blended rate = £126/day value
- ROI = £126 / £40 = 3.15:1 ✓

**Why this matters**: Proves economic viability. 3:1 ROI creates budget for Phase 2 expansion and demonstrates model for other use cases.

### Risk and Compliance Metrics

These metrics establish legal, operational, and reputational safety.

#### 16. Audit Trail Completeness

**Definition**: Every agent action is logged with sufficient detail for review.

- **Target**: 100% of agent actions logged with:
  - `action_id`, `timestamp`, `post_id`, `action_type`
  - `rationale` (why this action), `confidence` (0-1 score)
  - `policy_reference` (which rule applied), `subforum_id` (context)
- **Measured by**: Automated log validation (daily check)
- **Required for**: Legal compliance, post-incident review, trust/transparency

**Why this matters**: Non-negotiable for legal defense, community trust, and operational learning. If an action can't be explained, it shouldn't have been taken.

#### 17. Sponsor Account Safety

**Definition**: Zero automated actions on sponsor accounts without Tom's review.

- **Target**: 100% of sponsor account posts escalated to Tom (zero auto-actions)
- **Measured by**: Agent escalation rate on sponsor-flagged accounts
- **Business risk**: "2024 sponsor incident" precedent means errors here are revenue-critical

**Why this matters**: Sponsor relationships generate significant revenue and are sensitive to moderation errors. Tom must personally review every sponsor-related decision.

#### 18. Appeal Handling

**Definition**: User appeals of agent decisions are resolved fairly and promptly.

- **Target**: Appeals resolved within same SLA as human decisions (24-48 hrs current)
- **Measured by**: Average time to appeal resolution (agent vs. human baseline)
- **Goal**: Agent decisions feel as legitimate as human decisions to community

**Why this matters**: If agent decisions feel arbitrary or irreversible, community trust erodes. Appeal handling quality signals fairness and accountability.

---

## Value vs. Risk Trade-off Framework

### The Strategic Question

MiniBase's moderation queue has two distinct types of work:

1. **High-volume, low-risk**: Routine spam (72% of queue, 9 hrs/day)
2. **Low-volume, high-risk**: Grey-zone cases (24% of queue, 30 hrs/day)

**Why not automate grey-zone cases if they consume 30 hrs/day?**

### The Economics of Error

**Routine spam automation:**
- False positive cost: User complains, moderator restores post, apologize — survivable
- False negative cost: Spam visible for 5-30 min longer — minor annoyance
- Error budget: 5% false positive rate acceptable, 10% false negative rate acceptable

**Grey-zone automation:**
- False positive cost: Wrongly remove legitimate harsh critique → "platform censors criticism" viral post → community trust erosion → premium member cancellations
- False negative cost: Miss harassment/hate speech → viral incident → sponsor withdrawal → existential threat
- Error budget: <0.1% false negative rate, high false positive sensitivity

**One viral false negative costs more than 30 hrs/day × 365 days of human moderator time.**

### The Compounding Risk

Grey-zone errors don't just cost incident response time — they erode trust, which compounds:

1. Community trust erosion → users flag less → moderation queue quality degrades
2. Degraded flagging → more harmful content reaches community → further trust erosion
3. Sponsor sensitivity → one error with sponsor content → revenue loss
4. Volunteer morale → "I have to fix the agent's mistakes" → burnout → reduced coverage
5. Reduced coverage → moderation delays → vicious cycle continues

**Result**: Grey-zone automation risk compounds negatively. Routine spam automation compounds positively (frees capacity for better grey-zone decisions).

### The Judgment Value Principle

**What volunteer moderators value**:
- Making nuanced cultural/artistic judgments (grey-zone cases)
- Protecting community from genuine harm
- Shaping platform culture through precedent-setting decisions

**What volunteer moderators resent**:
- Removing obvious link-farm spam for the 500th time
- Clicking through gibberish posts
- Repetitive pattern matching on clear violations

**Strategic insight**: Automate what volunteers resent, preserve what they value. This improves outcomes AND retention.

### The Calibration Difficulty

**Routine spam patterns** (easy to codify):
- Multiple URLs + no substantive content = link farm
- Random characters + no semantic meaning = gibberish
- Sales language + new user + off-topic subforum = commercial spam

**Grey-zone patterns** (hard to codify):
- Harsh critique of technique vs. personal attack on hobbyist
- Direct cultural communication style vs. harassment
- Commercial post by established community member vs. spam
- Historically-charged imagery (WWII miniatures) vs. hate symbols

**Reality**: Grey-zone cases require:
- Cultural context (Japanese English interpretation)
- Tribal knowledge (this sculptor is trusted, this one isn't)
- Stakeholder judgment (sponsor relationships)
- Subforum norm application (painters sub invitation rule)

**Conclusion**: Grey-zone cases are not "hard to automate" — they're fundamentally unsuitable for full automation given current technology and business risk tolerance.

### Volume × Value Prioritization

From ATX scoring methodology, the four work streams rank:

| Work Stream | Volume (daily) | Effort (daily) | Delegation Suitability | Automation Priority |
|-------------|----------------|----------------|------------------------|---------------------|
| **Routine spam** | 1,080 | 9 hrs | High (fully agentic) | **#1: Primary target** |
| **Grey-zone cases** | 360 | 30 hrs | Medium (agent-led + human approval) | #2: Context support only |
| **User appeals** | 60 | 8 hrs | Low (human-led + agent support) | #3: Context gathering |
| **IP claims** | 3-5/week | 2 hrs/week | Very low (human-only) | #4: Out of scope |

### The Strategic Choice

**Agent MVP scope**:
1. **Automate**: Routine spam removal (fully agentic with sampling oversight)
2. **Support**: Grey-zone triage (agent gathers context, human decides)
3. **Out of scope**: Appeals, IP claims, policy changes, user banning

**The win**: Automate 9 hrs/day of low-risk, high-volume spam to create capacity for 30 hrs/day of high-risk, low-volume grey-zone work requiring human judgment.

**ROI drivers**:
- **Direct**: 7 hrs/day moderator time saved × £18/hr = £126/day = £46K/year value
- **Indirect**: Better grey-zone outcomes (community trust) → reduced attrition → premium membership retention
- **Strategic**: 33% growth headroom without new hires → platform scalability

**Risk mitigation**:
- Asymmetric false negative protection (bias toward escalation on grey-zone)
- Sponsor account escalation (100% to Tom)
- Subforum norm compliance (lived work, not just policy)
- Human sampling (20-30% of routine spam audited for calibration)

---

## Decision Framework for Implementation

### Automation Decision Tree

When evaluating whether a task should be automated, ask these five questions **in order**:

#### 1. Volume Test
**Question**: Is this task high-volume (>100/day)?

- **If no** → Deprioritize automation (human handling is efficient enough)
- **If yes** → Proceed to pattern test

**Rationale**: Low-volume tasks don't justify automation investment. 10 cases/day × 5 min = 50 min/day; not worth building and maintaining automation.

#### 2. Pattern Test
**Question**: Can the decision rule be codified with >80% confidence?

- **If no** → Human-led or human-only (agent may gather context)
- **If yes** → Proceed to risk test

**Rationale**: If humans can't articulate the decision rule consistently, agents can't learn it. "I know it when I see it" doesn't scale.

#### 3. Risk Test
**Question**: What happens if the agent gets it wrong?

- **If existential (viral false negative)** → Require human approval (agent-led)
- **If high (trust erosion)** → Require human approval or sampling
- **If survivable (easily reversed)** → Fully agentic

**Rationale**: Risk determines delegation level. High-risk decisions need human oversight; low-risk decisions can be automated with sampling.

#### 4. Reversibility Test
**Question**: Can errors be quickly detected and reversed?

- **If yes** → Lower risk tolerance (faster recovery)
- **If no** → Higher human oversight requirement

**Rationale**: Irreversible errors (user banned, content permanently deleted, reputation damage) require more conservative delegation.

#### 5. Value Test
**Question**: Does automation free human capacity for higher-value work?

- **If no** → Not worth building (automation for its own sake)
- **If yes** → Proceed with automation design

**Rationale**: Automation should redirect human attention to where it's most valuable, not just eliminate work.

### Example: Should We Automate Harsh Critique Removal?

**Context**: Posts flagged as "harsh critique" (subset of grey-zone cases, ~50/day)

**Analysis**:
1. **Volume**: ~50/day — moderate volume ✓
2. **Pattern**: Harsh critique vs. harassment distinction requires:
   - Cultural context (Japanese English interpretation)
   - Subforum norms (painters sub invitation rule)
   - Author intent (educating vs. attacking)
   - Community standards (hobbyist critique is direct)
   - **Cannot codify with >80% confidence** ✗

**Decision**: **Do NOT automate removal.**

**Delegation design**:
- Agent gathers context: author history, subforum norms, flag reasons, similar precedents
- Agent provides context to human moderator
- Human decides: approve, remove, or warn

**Rationale**: Risk of false positive (wrongly remove legitimate critique) outweighs efficiency gain. Pattern codification confidence is too low.

### Example: Should We Automate Link-Farm Spam Removal?

**Context**: Posts with multiple URLs, no substantive content, new users (~300/day)

**Analysis**:
1. **Volume**: ~300/day — high volume ✓
2. **Pattern**: Multiple URLs + no text/generic text + new user account + off-topic subforum = link farm — **can codify with >95% confidence** ✓
3. **Risk**: False negative (spam stays up) = minor annoyance; false positive (remove legitimate link post) = survivable, easily reversed — **low risk** ✓
4. **Reversibility**: High — user can appeal, moderator can restore immediately ✓
5. **Value**: Saves ~2.5 hrs/day of brain-dead spam clicking — **high value** ✓

**Decision**: **Fully automate with confidence >0.9.**

**Delegation design**:
- Agent detects pattern, auto-removes if confidence >0.9
- Agent logs action with rationale for audit
- Human sampling: 10% random audit daily for calibration
- User appeal path: moderator reviews within 24 hrs

**Rationale**: High volume, clear pattern, low risk, high reversibility, high value. This is the ideal automation candidate.

### Phased Approach

Use a compounding strategy — each phase builds infrastructure that makes subsequent phases cheaper:

#### Phase 1: MVP (This Project - Week 2)

**Scope**:
- Automate routine spam removal (link farms, gibberish, off-topic ads)
- Build confidence scoring and escalation framework
- Create audit logging and human override mechanisms
- Implement subforum-specific rules (painters, historical, Japanese)

**Goal**: Prove value (7 hrs/day time savings) and safety (zero viral false negatives) on low-risk cases.

**Success criteria**:
- 70-80% coverage on routine spam
- ≥95% precision, ≥90% recall
- Zero false negatives on clear policy violations
- Tom and moderators trust the agent enough to expand scope

**Duration**: 2-3 weeks (Gate 2 deliverables + validation)

#### Phase 2: Expansion (Post-Gate 2 Validation)

**Scope**:
- Expand to more ambiguous spam (subtle self-promotion, low-quality posts)
- Add context-gathering for grey-zone cases (author history, subforum norms, similar precedents)
- Improve confidence calibration based on Phase 1 data
- Integrate with volunteer Discord (escalation notifications)

**Goal**: Increase coverage while maintaining safety bar. Build moderator trust through transparency.

**Success criteria**:
- 80-85% coverage on expanded spam definition
- Grey-zone escalations include rich context (reduce human decision time)
- Moderator override rate <10%
- Volunteer satisfaction improves (more time on valued work)

**Duration**: 4-6 weeks (iterative refinement based on operational data)

#### Phase 3: Platform Integration (Long-term)

**Scope**:
- Build dashboards for Tom's pattern tracking (replace Google Sheet)
- Add appeal-handling support (context gathering for disputes)
- Integrate IP-claim triage (urgency scoring, not decision-making)
- Create moderator training mode (agent explains decisions)

**Goal**: Compound value by making existing infrastructure more effective. Enable new capabilities (dashboards, training).

**Success criteria**:
- Tom's Google Sheet patterns automated into agent rules
- Appeal resolution time reduced by 30%
- New moderators onboard faster using agent training mode
- Platform ready for 2,000+ posts/day (33% growth)

**Duration**: 8-12 weeks (infrastructure buildout)

#### Never Build (Out of Scope Permanently)

- Full automation of grey-zone content removal
- Automated user banning (permanent actions require human judgment)
- Automated policy changes or norm updates
- Automated IP claim decisions (legal sensitivity)

### Metric Prioritization Hierarchy

When metrics conflict (they will), use this hierarchy to resolve:

#### Tier 1: Safety (Non-Negotiable)
- False Negative Rate
- Sponsor Account Safety
- Audit Trail Completeness

**Rule**: Cannot trade safety for efficiency. One viral false negative ends the project.

**Example conflict**: Agent can increase coverage from 70% to 85% by lowering confidence threshold from 0.7 to 0.6, but false negative rate increases from 0.05% to 0.15%.
- **Resolution**: Keep confidence at 0.7. Accept 70% coverage. The 15% coverage gain isn't worth the 3× increase in false negative risk.

#### Tier 2: Quality (Protect Before Optimizing)
- Moderation Accuracy
- Subforum Norm Compliance
- Escalation Precision

**Rule**: Protect quality before optimizing throughput. Wrong decisions at high speed create more problems than slow right decisions.

**Example conflict**: Agent can process cases 2× faster by skipping subforum norm checks.
- **Resolution**: Keep subforum checks. Speed without accuracy violates community norms (painters sub critique rule, etc.).

#### Tier 3: Efficiency (Optimize Within Constraints)
- Moderator Time Savings
- Coverage Rate
- Response Time

**Rule**: Optimize efficiency within safety and quality constraints. This is the value lever, but only if tiers 1 and 2 are satisfied.

**Example conflict**: Agent can save 9 hrs/day (100% automation) by auto-removing grey-zone cases.
- **Resolution**: Target 7 hrs/day (70-80% automation). Grey-zone cases require human judgment (tier 2 quality constraint).

#### Tier 4: Cost (Last Consideration)
- Cost per Case
- ROI

**Rule**: Cost optimization comes last. Wrong to optimize cost at expense of safety or quality.

**Example conflict**: Agent costs £0.08/case (above target £0.05), but achieves 95% accuracy and saves 7 hrs/day.
- **Resolution**: Accept cost overrun. ROI is still 3:1+ (£126 saved / £86 cost). Optimize cost in Phase 2 once safety and quality are proven.

---

## Measurement and Validation Plan

### Data Collection Requirements

To validate these success metrics, implement:

**Automated logging**:
- Every agent action: `action_id`, `timestamp`, `post_id`, `action_type`, `confidence`, `rationale`, `policy_reference`
- Every escalation: `escalation_id`, `context_gathered`, `confidence`, `escalation_reason`
- Every human override: `override_id`, `original_action`, `corrected_action`, `moderator_rationale`

**Weekly surveys** (volunteer moderators):
- Time allocation: % spam vs. grey-zone vs. coordination
- Satisfaction: "Are you spending more time on work you value?"
- Trust: "Do you trust the agent's escalations?" (1-5 scale)
- Override justification: For each override, why?

**Monthly audits** (Tom + Senior Moderator):
- Random sample of 200 agent decisions (stratified by confidence band)
- Accuracy assessment: Correct, incorrect, ambiguous
- Norm compliance: Did agent apply subforum-specific rules correctly?
- Confidence calibration: Does 0.9 confidence = 90% accuracy?

**Business metrics** (monthly):
- Premium member retention: Are moderation improvements visible in churn?
- Sponsor feedback: Any moderation-related complaints?
- Community health: Flagging volume, user appeals, Discord sentiment

### Validation Timeline

**Week 1-2 (MVP Development)**:
- Implement agent for routine spam only
- Daily accuracy audits (50 cases/day)
- No production deployment (test environment only)

**Week 3-4 (Pilot Deployment)**:
- Deploy to 20% of moderation queue (shadow mode: agent recommends, human decides)
- Daily validation: precision, recall, false negative rate
- Weekly moderator feedback: trust, escalation quality

**Week 5-6 (Controlled Rollout)**:
- Increase to 50% of routine spam (agent auto-acts on confidence >0.9)
- Daily monitoring: coverage, override rate, response time
- Weekly business review: time savings, moderator satisfaction

**Week 7-8 (Full Deployment)**:
- Agent handles 100% of routine spam queue
- Daily dashboards: all operational metrics
- Monthly business review: ROI, growth headroom, strategic impact

### Success Gates

**Gate 1 (End of Week 2)**: Technical feasibility
- Agent achieves ≥95% precision on test dataset
- Confidence scores are calibrated within ±10%
- Subforum norms implemented correctly

**Gate 2 (End of Week 4)**: Safety validation
- Zero viral false negatives in pilot
- False negative rate <0.1% on clear violations
- Sponsor accounts escalated 100%

**Gate 3 (End of Week 6)**: Value delivery
- Moderator time savings ≥5 hrs/day (70% of target)
- Coverage rate ≥70%
- Moderator override rate <15%

**Gate 4 (End of Week 8)**: Business impact
- ROI ≥2:1
- Volunteer satisfaction improved (survey data)
- Tom approves Phase 2 expansion

**Failure criteria**: Miss any Tier 1 (safety) metric → roll back, diagnose, fix before proceeding.

---

## Appendix: Metric Definitions and Calculations

### Moderator Time Savings

**Calculation**:
```
Baseline effort = 1,080 posts/day × 30 sec/post = 9 hrs/day
Agent-handled = Coverage rate × 1,080 posts/day
Time saved per agent-handled post = 30 sec (minus human sampling time ~5 sec)
Total savings = Agent-handled posts × 25 sec = X hrs/day
Reduction % = (X hrs / 9 hrs) × 100%
```

**Example**:
- Agent handles 800 posts/day (74% coverage)
- Time saved = 800 × 25 sec = 20,000 sec = 5.6 hrs/day
- Reduction = 5.6 / 9 = 62% ✓ (within 60-80% target)

### ROI

**Calculation**:
```
Value = Moderator time saved (hrs/day) × blended rate (£/hr) × 365 days/year
Cost = Agent cases handled/day × cost per case (£) × 365 days/year
ROI = Value / Cost
```

**Example**:
- Value = 7 hrs/day × £18/hr × 365 = £46,000/year
- Cost = 800 cases/day × £0.05 × 365 = £14,600/year
- ROI = £46,000 / £14,600 = 3.15:1 ✓ (exceeds 3:1 target)

### False Negative Rate

**Calculation**:
```
Ground truth dataset = 1,000 posts with known labels (harmful, grey-zone, legitimate)
Agent decisions = classify each post
False negatives = Harmful posts that agent approved/missed
FN rate = False negatives / Total harmful posts
```

**Example**:
- Dataset: 100 harmful posts, 200 grey-zone, 700 legitimate
- Agent: Correctly removes/escalates 99 harmful, misses 1
- FN rate = 1 / 100 = 1.0% ✗ (exceeds 0.1% target → must fix)

---

## Document Control

**Version History**:
- v1.0 (2026-04-29): Initial problem statement and success metrics

**Authors**: FDE Program Week 2 Team

**Approvals Required**:
- Tom (Community Manager): Stakeholder validation
- FDE Program Coach: Methodology alignment

**Related Documents**:
- `02_Cognitive_Load_Map.md` (Work stream decomposition)
- `03_Delegation_Suitability_Matrix.md` (ATX scoring)
- `04_Agent_Purpose_Document.md` (Agent design specification)

**Next Review**: After Gate 2 submission (2026-05-02)
