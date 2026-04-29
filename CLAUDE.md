# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is an **FDE Program Week 2 project** focused on ATX (Agentic Transformation) methodology. The goal is to build a functional prototype for **Scenario 4: Community Content Moderation** from the FDE program scope, applying cognitive work assessment and agent design principles.

**Scenario Context:** MiniBase — UK-incorporated tabletop-miniature hobbyist community platform (~180K active users, 12K posts/day across 14 sub-forums). We are designing and building an AI agent to support the hybrid moderation team (8 volunteer moderators + 2 paid staff) in handling ~1,500 daily posts that enter the moderation queue.

This project is a learning exercise for understanding FDE engineering principles, not a production deployment. The focus is on demonstrating thoughtful delegation architecture, clear agent boundaries, and ATX methodology application.

## Repository Structure

```
FDE_ContentModerator_2/
├── FDE_Program/          # Program materials and ATX reference documents
│   ├── Week2/            # Week 2 materials including scenario briefs
│   │   ├── enriched_scenarios.md        # Full Scenario 4 details
│   │   ├── README-Participants-Week2.md # Week 2 requirements
│   │   └── references/                  # ATX methodology references
│   │       ├── atx-concepts.md          # Core ATX concepts
│   │       ├── atx-agent-mapping.md     # Agent design patterns
│   │       ├── atx-assessment.md        # Assessment methodology
│   │       ├── atx-scoring.md           # Delegation suitability scoring
│   │       └── atx-economics.md         # Economics of digital labour
│   └── Intro+Week1/      # Week 1 materials (for context)
├── Specification/        # Project specifications and analysis artifacts
├── Deliverables/         # Week 2 deliverables (7 required artifacts)
└── CLAUDE.md            # This file
```

## Core Entities (MiniBase Scenario 4)

### Post
Represents user-generated content on the MiniBase platform.

Attributes:
- `id`: UUID, immutable
- `author_id`: foreign key to User, required
- `subforum_id`: foreign key to Subforum, required (one of 14 subforums or gallery)
- `content`: text, required, max 10,000 characters
- `created_at`: ISO 8601 timestamp, immutable
- `edited_at`: ISO 8601 timestamp, nullable (last edit)
- `status`: enum [PUBLISHED, FLAGGED, UNDER_REVIEW, REMOVED, APPROVED], default PUBLISHED
- `flag_count`: non-negative integer (user reports)
- `flagged_reasons`: array of strings (spam, harassment, off-topic, commercial, ip-claim)
- `moderation_history`: array of ModerationAction objects

State machine:
- PUBLISHED → FLAGGED (when flag_count >= 4, or moderator samples, or automated detection)
- FLAGGED → UNDER_REVIEW (moderator claims the case)
- UNDER_REVIEW → APPROVED (moderator clears, post returns to PUBLISHED state)
- UNDER_REVIEW → REMOVED (moderator removes)
- REMOVED is terminal (unless appealed)

### ModerationAction
Nested in Post, tracks moderation decisions.

Attributes:
- `action_id`: UUID
- `moderator_id`: foreign key to Moderator (nullable if agent)
- `agent_id`: identifier if action taken/proposed by agent
- `action_type`: enum [NO_ACTION, WARNING, REMOVAL, BAN_USER, ESCALATE]
- `rationale`: text, required for REMOVAL and BAN_USER
- `confidence`: float 0-1 (agent confidence score, null for human actions)
- `reviewed_by_human`: boolean (true if human reviewed agent proposal)
- `timestamp`: ISO 8601 timestamp
- `policy_reference`: string (which rule/norm applied)

### Subforum
Represents content categories with distinct norms.

Key subforums:
- Painters sub: "no critique without invitation" norm (not in global policy)
- Historical sub: more permissive on historically-charged imagery
- Japanese painters sub: English critiques may read harsher than intended
- Gallery: different moderation patterns (focus on IP claims, self-promotion)

Each subforum has:
- `norm_overrides`: JSON object defining subforum-specific rules
- `escalation_required_for`: array of action types requiring escalation for this subforum

### IPClaim
Separate workflow from post moderation.

Attributes:
- `claim_id`: UUID
- `claimant_email`: string, required
- `post_id`: foreign key to Post
- `claim_type`: enum [COPYRIGHT, TRADEMARK]
- `description`: text, required
- `evidence_urls`: array of strings
- `status`: enum [PENDING, UNDER_REVIEW, RESOLVED_TAKEDOWN, RESOLVED_NO_ACTION, DISPUTED]
- `assigned_to`: "Tom" (Community Manager) or "Senior Moderator"
- `resolution_time_avg`: 30 minutes + escalation

State machine:
- PENDING → UNDER_REVIEW (Tom claims)
- UNDER_REVIEW → RESOLVED_TAKEDOWN (claim valid)
- UNDER_REVIEW → RESOLVED_NO_ACTION (claim invalid)
- UNDER_REVIEW → DISPUTED (complex, needs legal review)

## The Four Work Streams (from Scenario 4)

Of ~12K daily posts, 12.5% (~1,500/day) enter moderation queue via flags, detection, or sampling:

1. **Routine spam / clear-violation removal** (~1,080/day; ~30 sec/case; 72% of queue)
   - Obvious spam, off-topic, miscategorized posts
   - High delegation suitability: fully agentic with human oversight sampling

2. **Grey-zone case review** (~360/day; ~5 min/case; 24% of queue)
   - Hobbyist critique that reads harsh, commercial posts from community members, regional disputes
   - Medium delegation suitability: agent-led with human review before action

3. **User dispute appeals** (~60/day; ~8 min/case; 4% of queue)
   - Appeals of prior moderation actions
   - Low delegation suitability: human-led with agent support (context gathering)

4. **IP-claim resolution** (~3-5/week; ~30 min/case)
   - Copyright/trademark claims
   - Very low delegation suitability: human-only with agent-assisted triage

## ATX Methodology — Key Concepts to Apply

When working on this project, apply these ATX principles:

### Delegation Archetypes
- **Fully agentic**: Agent decides and acts; human reviews samples for quality assurance
- **Agent-led with oversight**: Agent proposes action; human approves before execution
- **Human-led with agent support**: Human decides; agent gathers context and drafts
- **Human-only**: Agent has no role; preserve human judgment

**Critical**: Not everything should be "fully agentic." Week 2's primary anti-pattern is defaulting all tasks to full automation. Delegation boundaries must be justified by risk, reversibility, and business constraints.

### Lived Work vs. Documented Work
The 14-page MiniBase moderation policy is the **documented** work. The **lived** work includes:
- Subforum-specific norms (e.g., painters sub "no critique without invitation")
- Tom's pattern tracker for high-risk users and sponsors
- Volunteer moderator disagreements resolved in Discord
- The "2024 sponsor incident" that shapes current risk tolerance
- Cultural interpretation differences (Japanese sub English critiques)

**Build for lived work, not just policy.** Discovery questions to Tom (stakeholder) are essential for uncovering these gaps.

### Escalation Triggers
Define clear conditions when the agent must hand off to a human:
- Commercial posts from sponsor accounts (Tom reviews personally)
- IP claims from @sculpturedragon (established sculptor, full review every time)
- Historical sub content flagged for controversial imagery (requires Tom if uncertain)
- Any case where confidence < 0.7
- Posts with >12 reactions (high community engagement)

### Failure Modes
From Tom's briefing: **"False positives are survivable; one viral false negative is existential."**

This asymmetry shapes the agent's risk posture:
- Bias toward escalation on grey-zone cases
- Sponsor/VIP posts require extra scrutiny (never auto-remove)
- Harsh-but-accurate critique is acceptable; harassment is not (distinction is subtle)

## Project Deliverables (Week 2 Requirements)

When building or refining this project, work toward these 7 deliverables:

1. **Cognitive Load Map** — Jobs to be Done, cognitive zones, breakpoints for the 4 work streams
2. **Delegation Suitability Matrix** — Scoring each task cluster on delegation dimensions
3. **Volume × Value Analysis** — Plotting 4 work streams to identify primary agentic target
4. **Agent Purpose Document** — Purpose, scope, KPIs, autonomy matrix, escalation triggers
5. **System/Data Inventory** — What the agent needs to access (Discourse API, gallery API, Discord, Google Sheets, email)
6. **Discovery Questions** — Questions for Tom that would materially change the design
7. **This CLAUDE.md** — Workflow discipline and build guidance

Store deliverables in `Deliverables/` directory with clear naming (e.g., `cognitive_load_map.md`, `agent_purpose_document.md`).

## Tooling and System Constraints

MiniBase runs on:
- **Discourse** (forum platform, self-hosted AWS, REST APIs available)
- **In-house gallery** (Rails app, custom, limited API surface)
- **Stripe** (premium memberships, commissions)
- **Discord** (volunteer moderator coordination)
- **Google Sheets** (Tom's moderation patterns tracker)
- **Email** (IP-claim correspondence, legal record)

### Integration Notes
- Discourse API provides post content, flags, user history, subforum metadata
- Gallery API is limited — may require scraping or manual data entry for some fields
- Tom's Google Sheet patterns are not in any system — must be translated into agent rules
- Discord mod discussions are informal — agent should not auto-post there without explicit design

## The Closed Build Loop (Week 2 Requirement)

Before Thursday early afternoon, you must complete a **closed build loop** to validate the Agent Purpose Document:

1. **Build what you're confident about** from the Agent Purpose Document
2. **Identify gaps**: What questions did you ask? What couldn't you build? What did you build incorrectly?
3. **Diagnose gaps** using the Week 1 taxonomy + Week 2 delegation boundary gaps
4. **Revise the Agent Purpose Document** based on diagnosis (especially autonomy matrix and escalation triggers)
5. **Re-run and verify** the revised document produces better results

**Delegation boundary gaps** occur when the document doesn't specify whether a step should be fully agentic, agent-led, or human-led — and the builder defaults to whichever is easiest to implement.

If asked to "build the agent described in this document," respond with:
1. What you can build confidently without questions
2. What you need to clarify before building
3. Then build only the confident parts

## Agent Design Principles (From ATX)

When designing or implementing the moderation agent:

### Purpose Statement
"Support MiniBase's hybrid moderation team in triaging flagged posts, removing clear spam/violations, and escalating grey-zone cases to human moderators — while preserving subforum-specific norms and the platform's 'false negatives are existential' risk posture."

### Autonomy Matrix

**Agent decides alone (no human approval required):**
- Intent classification (spam, off-topic, miscategorized)
- Post metadata retrieval (author history, subforum, flag reasons)
- Drafting removal rationale for clear violations
- Auto-removal of obvious spam (e.g., link farms, gibberish) when confidence > 0.9
- Logging all actions for human audit

**Agent proposes, human approves before action:**
- Removal of grey-zone posts (harsh critique, commercial-adjacent, cultural ambiguity)
- Warning issuance to established community members
- Any action on sponsor account posts
- Any action on posts with >12 reactions (high engagement)

**Human takes over (agent supports):**
- User dispute appeals (agent gathers context, human decides)
- IP-claim resolution (agent triages urgency, Tom handles)
- Subforum norm conflicts (agent flags, volunteer mods discuss)
- Any case where confidence < 0.7

**Human-only (agent has no role):**
- Policy changes or norm updates
- Banning users (permanent action)
- Legal/compliance decisions

## Validation and Testing

When implementing features, validate against:

1. **Accuracy**: Can the agent correctly classify 85%+ of routine spam?
2. **Safety**: Does the agent escalate all grey-zone cases instead of auto-removing?
3. **Norm compliance**: Does the agent apply subforum-specific rules (e.g., painters sub invitation rule)?
4. **Auditability**: Is every action logged with rationale and confidence score?
5. **Escalation hygiene**: Does the agent include context in escalations so humans can decide quickly?

## Assumptions and Discovery Gaps

**Known unknowns** (require discovery questions to Tom):
- What exactly triggered the "2024 sponsor incident" and what are the consequences?
- How do volunteer moderators coordinate on grey-zone disagreements?
- Which established users have tribal status that affects moderation tolerance?
- What IP claim patterns distinguish legitimate claims from retaliatory reports?
- How does Tom's Google Sheet tracker actually get used day-to-day?

**Assumptions to validate**:
- Confidence threshold of 0.7 for escalation (needs calibration against real cases)
- 4 flags as the threshold for entering the queue (may vary by subforum or user reputation)
- Harsh critique vs. harassment distinction can be codified (may require human judgment)

## Build Commands and Workflow

This is a specification and design project, not a production codebase (yet). When building a prototype:

1. **Start with analysis**, not code:
   - Read `FDE_Program/Week2/enriched_scenarios.md` for full Scenario 4 context
   - Review `FDE_Program/Week2/references/atx-*.md` for methodology
   - Draft deliverables in `Deliverables/` directory

2. **When ready to prototype**:
   - Use Python or JavaScript/TypeScript (choose based on familiarity and API libraries)
   - Structure as: `src/agent.py` or `src/agent.ts` (main agent logic)
   - Include `src/escalation_rules.py` or `src/escalation_rules.ts` (delegation boundaries)
   - Mock Discourse API calls initially (use `tests/fixtures/` for sample data)

3. **Testing approach**:
   - Create test cases for each work stream (routine spam, grey-zone, appeals, IP)
   - Include subforum-specific test cases (painters critique, historical imagery)
   - Test escalation triggers explicitly (sponsor posts, high-engagement posts, low confidence)

4. **No production deployment**: This is a learning artifact. Focus on demonstrating sound design, not operational readiness.

## What NOT to Do

- **Do not** default everything to "fully agentic" — this is the Week 2 anti-pattern
- **Do not** build from the 14-page policy alone — lived work differs from documented work
- **Do not** ignore subforum-specific norms — they are critical to MiniBase's culture
- **Do not** auto-remove grey-zone content — escalate for human review
- **Do not** claim domain expertise you don't have — mark assumptions explicitly
- **Do not** skip the closed build loop — it's required to validate the Agent Purpose Document
- **Do not** create documentation files unless explicitly requested — focus on deliverables
- **Do not** treat Tom's patterns tracker as optional — it contains the lived rules

## Stakeholder Brief

**Tomasz "Tom" Włodarczyk**, Community Manager:
- Warsaw-based, ex-volunteer moderator promoted to paid role
- Risk-averse due to prior incidents: "False positives are survivable; one viral false negative is existential"
- Manages sponsor relationships (commercial constraint on content decisions)
- Coordinates 8 volunteer moderators across time zones
- Uses a Google Sheet tracker for high-risk patterns (not in formal systems)

When in doubt about a moderation decision, **ask what Tom would do** and whether it requires his personal review.

## Success Criteria

By Week 2 Friday, this project should demonstrate:
- Thoughtful cognitive work decomposition (not just task lists)
- Justified delegation archetypes (not "fully agentic" everywhere)
- Clear agent boundaries and escalation triggers
- Evidence of eliciting lived work (not just reading the policy)
- A buildable Agent Purpose Document (validated via closed build loop)
- Discovery questions that would materially change the design (not generic questions)

The goal is to show FDE-level thinking: understanding cognitive work, designing delegation architecture, and balancing automation value against operational risk.
