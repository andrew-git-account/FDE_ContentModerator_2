# Discovery Phase: MiniBase Content Moderation - Lived Work Analysis

**Project**: MiniBase Community Content Moderation Agent  
**Phase**: Discovery & Cognitive Work Mapping  
**Date**: 2026-04-29  
**Version**: 1.0

---

## Executive Summary

This document captures findings from discovery interviews with MiniBase's moderation team to understand **how moderation work actually happens** (lived work) vs. how the 14-page policy describes it (documented work).

### Key Discoveries

1. **70% of moderation time is spent on mindless spam removal** that follows clear patterns and could be automated
2. **The real delegation boundary is tribal knowledge, not policy** - subforum norms, Tom's watchlist, Discord precedents are not documented
3. **Context-gathering consumes 20% of moderator time** - navigating between Discourse, Discord, Google Docs, user profiles
4. **Grey-zone decisions require 4-5 minutes** but could be reduced to 1-2 minutes with automatic context aggregation
5. **Moderator risk tolerance differs from management** - volunteers prioritize community protection, Tom prioritizes business continuity
6. **Tool fragmentation creates coordination overhead** - no integration between moderation queue, watchlists, precedents, or subforum rules

### Primary Opportunities

| Opportunity | Current State | Potential Impact |
|-------------|---------------|------------------|
| **Automate routine spam** | 9 hrs/day manual removal | Save 7 hrs/day (77% reduction) |
| **Aggregate context for grey-zone** | 2-3 min manual gathering per case | Save 12-18 hrs/day across team |
| **Codify tribal knowledge** | Tom's Sheet, Discord logs, personal notes | Reduce inconsistency, enable faster training |
| **Integrate escalation workflow** | Discord + email + Discourse | Reduce coordination overhead 5% → 2% |

---

## Discovery Methodology

### Interview Approach

**ATX Discovery Pattern**: Broad funnel → Narrow funnel → Probe funnel

**Interviewee**: Sarah (Volunteer Moderator)
- 3 years experience
- Based in UK
- Primary coverage: Painters sub-forum + general queue
- Representative of 8 volunteer moderators

**Interview Structure**:
1. **Broad funnel (10 min)**: How do you spend your time? What consumes attention?
2. **Narrow funnel (20 min)**: Walk through a specific grey-zone case step-by-step
3. **Probe funnel (15 min)**: What are the decision rules? When do you escalate? What patterns do you match?

**Limitations**:
- Single moderator perspective (need to validate with Tom, Senior Moderator, other volunteers)
- UK timezone bias (Aki in Japan, Klaus in Germany may have different patterns)
- Did not observe actual moderation session (interview recall may differ from live work)

### Validation Plan

To confirm these findings:
1. **Shadow observation**: Watch 2-hour moderation sessions with 3 different moderators
2. **Tom interview**: Validate against management perspective, uncover watchlist patterns
3. **Discord log analysis**: Extract precedent decisions, coordination patterns, common questions
4. **Discourse data analysis**: Volume/type distribution, flag patterns, resolution times

---

## Current Process: As Lived by Moderators

### Mermaid Diagram: Moderation Workflow

```mermaid
flowchart TD
    Start([Moderator Opens Queue<br/>8pm UK time]) --> Sort[Sort by Flag Count]
    
    Sort --> CheckFlags{Flag Count?}
    
    CheckFlags -->|≥6 flags| Urgent[Review Immediately<br/>MANUAL: Read post, assess severity<br/>BREAKPOINT: Is this genuine harm?<br/>RISK: Missing urgent harassment]
    
    CheckFlags -->|<6 flags| Routine[Process in Order<br/>MANUAL: Click through queue<br/>BREAKPOINT: Pattern match spam vs. grey<br/>RISK: Mindless clicking → miss edge cases]
    
    Routine --> QuickScan[Quick Scan Post<br/>~2 seconds<br/>MANUAL: URLs? New user? Gibberish? Off-topic?<br/>BREAKPOINT: Clear pattern or needs investigation?<br/>RISK: False pattern match]
    
    QuickScan --> IsSpam{Clear Spam Pattern?}
    
    IsSpam -->|Yes - Link farm, bot, gibberish| RemoveSpam[Auto-Remove<br/>~30 seconds total<br/>MANUAL: Click remove, select reason<br/>BREAKPOINT: None - routine action<br/>RISK: 1% false positive on edge cases]
    
    IsSpam -->|No - Grey zone| CheckSponsor{Sponsor Account?}
    
    CheckSponsor -->|Yes - Has 'Sponsor' badge| EscalateTom[Escalate to Tom<br/>MANUAL: Message in Discord or flag in system<br/>BREAKPOINT: Wait for Tom's decision<br/>RISK: Delayed response if Tom offline - EXISTENTIAL if wrong action taken]
    
    CheckSponsor -->|No| CheckEngagement{High Engagement?<br/>>20 reactions?}
    
    CheckEngagement -->|Yes| EscalateDiscord[Post in Discord for Consensus<br/>MANUAL: Screenshot, ask other mods<br/>BREAKPOINT: Wait 10-30 min for responses<br/>RISK: Timezone gaps, inconsistent opinions]
    
    CheckEngagement -->|No| ContextGather[Gather Context<br/>4-5 minutes<br/>MANUAL WORK:<br/>- Open user profile in new tab<br/>- Check post history<br/>- Read subforum-specific rules<br/>- Search personal notes/precedents<br/>- Scroll Discord for similar cases<br/>BREAKPOINT: Pattern emerging or still uncertain?<br/>RISK: 20% of time spent navigating tools]
    
    ContextGather --> CheckSubforum{Subforum-Specific<br/>Norm Applies?}
    
    CheckSubforum -->|Painters - Invited critique?| CheckInvitation{Thread Title<br/>or OP Asked for<br/>Feedback?}
    
    CheckInvitation -->|Yes - Invited| AssessTone[Assess Tone:<br/>Critique vs. Harassment<br/>MANUAL: Read full comment, user intent, OP reaction<br/>BREAKPOINT: Targets work or person?<br/>RISK: Cultural interpretation, sarcasm detection]
    
    CheckInvitation -->|No - Uninvited| RemoveCritique[Remove for Subforum Norm Violation<br/>MANUAL: Remove, message user with rule explanation<br/>BREAKPOINT: None - clear norm violation<br/>RISK: User disputes 'invitation' interpretation]
    
    CheckSubforum -->|Historical - Sensitive imagery?| ApplyPermissive[Apply Permissive Standard<br/>MANUAL: Assess historical accuracy vs. hate symbol<br/>BREAKPOINT: Genuine historical vs. dogwhistle?<br/>RISK: Context collapse - viral Twitter backlash]
    
    CheckSubforum -->|Japanese sub| CheckCultural[Check for Cultural<br/>Interpretation Issues<br/>MANUAL: English phrasing, intent assessment<br/>BREAKPOINT: Harsh tone or translation artifact?<br/>RISK: Remove legitimate feedback from Japanese user]
    
    CheckSubforum -->|No special norm| StandardAssess[Standard Assessment]
    
    AssessTone --> DecisionPoint{Decision Confidence?}
    CheckCultural --> DecisionPoint
    ApplyPermissive --> DecisionPoint
    StandardAssess --> DecisionPoint
    
    DecisionPoint -->|High confidence - Clear call| TakeAction[Take Action<br/>MANUAL: Remove or approve, log rationale<br/>BREAKPOINT: None<br/>RISK: Wrong call on edge case]
    
    DecisionPoint -->|Medium confidence - 50/50| CheckPrecedent[Check Personal Notes<br/>MANUAL: Search Google Doc for similar cases<br/>BREAKPOINT: Found precedent or still split?<br/>RISK: Precedents not shared across mods]
    
    CheckPrecedent -->|Found precedent| TakeAction
    CheckPrecedent -->|Still uncertain| AskDiscord[Ask in Discord #mod-decisions<br/>MANUAL: Explain case, wait for input from Aki/Klaus<br/>BREAKPOINT: 10-30 min wait, timezone dependent<br/>RISK: Inconsistent responses, no formal record]
    
    AskDiscord -->|Consensus reached| TakeAction
    AskDiscord -->|No response / Still split| EscalateToSenior[Escalate to Tom or Senior Mod<br/>MANUAL: Flag in system, explain uncertainty<br/>BREAKPOINT: Wait for decision (hours to 1 day)<br/>RISK: Delayed moderation, harm persists]
    
    DecisionPoint -->|Low confidence - Uncertain| EscalateToSenior
    
    TakeAction --> LogDecision[Log in Personal Notes<br/>MANUAL: Add edge case to Google Doc<br/>BREAKPOINT: Worth documenting?<br/>RISK: Tribal knowledge not shared]
    
    LogDecision --> NextPost{More Posts<br/>in Queue?}
    
    RemoveSpam --> NextPost
    RemoveCritique --> NextPost
    Urgent --> NextPost
    
    NextPost -->|Yes| QuickScan
    NextPost -->|No - Queue empty or 2hr session done| EndSession([End Session<br/>Post summary in Discord])
    
    EscalateTom -.->|Tom decides later| TomDecision[Tom Reviews<br/>MANUAL: Tom checks watchlist, history, context<br/>BREAKPOINT: Business risk assessment<br/>RISK: Tom unavailable - delayed decision]
    
    EscalateToSenior -.->|Async decision| TomDecision
    
    TomDecision -.->|Decision made| NotifyModerator[Notify Original Moderator<br/>MANUAL: Discord message or system notification<br/>BREAKPOINT: Learn from decision<br/>RISK: Feedback loop incomplete]
    
    style RemoveSpam fill:#90EE90
    style TakeAction fill:#90EE90
    style EscalateTom fill:#FFB6C1
    style EscalateDiscord fill:#FFD700
    style EscalateToSenior fill:#FFB6C1
    style ContextGather fill:#87CEEB
    style AskDiscord fill:#FFD700
    style CheckPrecedent fill:#87CEEB
```

### Diagram Legend

**Colors:**
- 🟢 **Green** (Light): Automated actions - clear patterns, low cognitive load
- 🔵 **Blue** (Light): Context-gathering - high manual effort, tool navigation
- 🟡 **Yellow**: Coordination - Discord communication, waiting for consensus
- 🔴 **Pink**: Escalation - high-stakes handoff to Tom/Senior Mod

**Annotations:**
- **MANUAL**: What the moderator physically does (clicks, reading, typing, searching)
- **BREAKPOINT**: Where the moderator pauses to think, decide, or wait
- **RISK**: What could go wrong at this step (errors, delays, inconsistencies)

---

## Detailed Findings: Lived Work vs. Documented Work

### 1. Moderation Time Allocation (Actual vs. Policy)

| Work Type | Policy Expectation | Actual Practice (Sarah) | Gap Analysis |
|-----------|-------------------|------------------------|--------------|
| **Routine spam removal** | "Review each case carefully" | 60% of time, 2-sec pattern match, ~30 sec/case | Policy assumes thoughtful review; reality is mindless clicking |
| **Grey-zone assessment** | "Apply policy guidelines" | 35% of time, 4-5 min/case, context-gathering heavy | Policy doesn't account for subforum norms, tribal knowledge |
| **Escalation** | "Escalate when uncertain" | 1 in 10 grey cases (~10%), rest decided independently | Policy says escalate uncertainty; reality is selective escalation to avoid overload |
| **Coordination** | Not mentioned in policy | 5% of time, Discord-based, informal | Policy assumes solo work; reality is distributed decision-making |
| **Tool navigation** | Not mentioned | ~20% of grey-zone time (3 windows, 4-5 tabs) | Policy assumes integrated tools; reality is fragmented |

### 2. Spam Pattern Recognition ("Vibes")

Sarah can identify spam in ~2 seconds using implicit pattern matching. When asked to articulate the patterns:

#### Link Farm Spam
**Observable signals:**
- 3+ URLs in post body
- Minimal or generic text ("Check this out!", "Great deals here")
- New account (<1 week old)
- Username pattern: brand-ish + numbers ("shopdirect2024", "dealsofficial")
- Posted in off-topic subforum

**Confidence**: 99% accurate self-assessment  
**Decision time**: 2 seconds to identify, 30 seconds to remove  
**Codifiability**: **High** - all signals are objective and observable

#### Crypto/Forex Bot Spam
**Observable signals:**
- Formulaic text structure: "I was [struggling] until I found [name], now I [success metric], DM for info"
- Posted across multiple subforums within seconds
- New account
- Username pattern: generic + numbers ("sarah8472", "trader_crypto_official")

**Confidence**: 99% accurate  
**Decision time**: 2 seconds  
**Codifiability**: **High** - regex-matchable patterns, timing analysis

#### Gibberish Spam
**Observable signals:**
- Random characters or word salad
- No semantic meaning
- Often includes URLs
- New account

**Confidence**: 100% accurate  
**Decision time**: <2 seconds  
**Codifiability**: **High** - language model perplexity scoring

#### Off-Topic Commercial
**Observable signals:**
- Sales language ("Buy my...", "For sale:", "Check out my store")
- Posted in wrong subforum (e.g., "Buy 3D prints" in painters sub, should be in marketplace)
- New or low-history account

**Confidence**: 95% accurate (5% false positives on established members selling old miniatures)  
**Decision time**: 2-5 seconds  
**Codifiability**: **Medium-High** - requires subforum context and account age/history

**Key insight**: These patterns are **fully automatable** with >95% accuracy. Sarah explicitly said "just make it go away."

### 3. Grey-Zone Decision Patterns (Hard to Codify)

Grey-zone cases require **4-5 minutes** of investigation and integrate multiple contextual signals.

#### Harsh Critique vs. Harassment

**The boundary** (Sarah's articulation): "Harassment targets the person, critique targets the work."

**Reality**: This boundary is ambiguous and context-dependent.

**Examples from Sarah:**

| Post Content | Sarah's Classification | Reasoning |
|--------------|----------------------|-----------|
| "Your edge highlighting is non-existent, color choices are baffling, you clearly haven't watched tutorials. Don't post WIPs until you've learned basics." | **Critique** (approved) | - Posted in "any tips?" thread (invited)<br/>- Targets technique, not person<br/>- Commenter is established helpful member<br/>- OP replied positively ("brutal but fair") |
| "You have no talent and shouldn't be in this hobby." | **Harassment** (remove) | - Targets person's inherent ability<br/>- No constructive feedback<br/>- Discourages participation |
| "You clearly haven't practiced enough to post here yet." | **??? Ambiguous** | - Targets skill level (person) or work quality?<br/>- Depends on: tone, invitation, user history<br/>- Sarah would escalate this one |

**Signals Sarah integrates**:
1. **Invitation context**: Did OP ask for feedback? ("any tips?" in thread title, "feedback wanted" tag)
2. **Target**: Work/technique vs. person/ability
3. **Constructive content**: Does it explain what's wrong and how to improve?
4. **User history**: Is commenter helpful or trolling?
5. **OP reaction**: Did they take it as helpful or harmful?
6. **Subforum norms**: Painters sub "no uninvited critique" rule
7. **Cultural context**: Japanese English, sarcasm detection

**Codifiability**: **Low** - requires multi-signal integration, cultural interpretation, intent assessment  
**Sarah's trust in AI**: **None** - "That boundary is so cultural, so context-dependent... I think AI would either be too aggressive or too permissive."

**Delegation recommendation**: Agent gathers signals, human decides.

#### Commercial Content from Established Members

**The boundary**: "Is this spam or legitimate community participation?"

**Policy**: "No commercial posts outside marketplace subforum."

**Lived work exception**: Established members (3+ years, active participation) can post about selling old miniatures in gallery if contextually relevant.

**Example**: User selling painted miniatures in gallery after 3 years of posting painting tutorials.
- **Policy**: Remove (commercial content in wrong subforum)
- **Sarah's decision**: Approve (established member, community contribution history)
- **Reasoning**: "They've earned some latitude. This isn't spam, it's a community member sharing their work."

**Codifiability**: **Medium** - requires account age, participation history, commercial intent assessment  
**Risk**: Inconsistent application (Sarah approves, another mod removes)

#### Subforum-Specific Norms (Not in Global Policy)

**Discovery**: Each subforum has unwritten norms that override the 14-page global policy.

| Subforum | Norm | Source | Codifiability |
|----------|------|--------|---------------|
| **Painters** | "No critique without invitation" - only critique if OP explicitly asks | Tribal knowledge, enforced by Aki | **Medium** - can detect invitation in thread title/tags |
| **Historical** | Permissive on historically-charged imagery (WWII swastikas if historically accurate) | Subforum culture, precedent-based | **Low** - requires historical context assessment |
| **Japanese Painters** | English critiques may read harsher than intended - escalate if uncertain | Aki's guidance, cultural awareness | **Low** - requires cultural interpretation |
| **Gallery** | Established members can post about selling prints; new members cannot | Enforced by Tom, based on account age/reputation | **Medium-High** - account age + participation history |

**The problem**: These norms are not documented. New moderators learn by:
1. Making mistakes and being corrected
2. Watching other moderators' decisions
3. Asking in Discord

**Training time**: ~1 month "training wheels" period with high escalation rate.

**Codifiability implications**:
- **Painters sub invitation rule**: Can be partially automated (detect "feedback wanted", "tips?", "critique?" in thread)
- **Historical sub permissiveness**: Requires human judgment on historical accuracy vs. hate symbols
- **Cultural interpretation**: Requires human judgment, but can flag for moderator attention
- **Gallery commercial posts**: Can check account age + post history, but intent assessment is subjective

### 4. Tribal Knowledge: The Hidden System of Record

#### Tom's Google Sheet Watchlist

**What it contains** (inferred from Sarah's description):
- Sponsor accounts (require Tom's personal review)
- Established sculptors with IP claim history (@sculpturedragon)
- Users with fraud patterns (multiple returns, suspicious activity)
- High-risk users (prior incidents, complaints)

**Who has access**: Tom only

**How moderators learn about it**: Discord messages ("heads up, @sculpturedragon just filed an IP claim, flag anything involving them to me")

**Problem**: Moderators must maintain mental notes of who's on the watchlist based on temporal Discord messages. No persistent, shared system.

**Risk**: Inconsistent application - moderators who miss the Discord message may not escalate.

**Codifiability**: **High** - can be converted to structured watchlist with escalation rules  
**Agent design implication**: Watchlist should be codified as agent escalation trigger (sponsor badge, known sculptor, etc.)

#### Moderators' Personal Note Systems

**Discovery**: Multiple moderators keep personal Google Docs of edge-case precedents.

**Sarah's note system:**
- Edge cases and how she decided them
- Ambiguous posts with resolution rationale
- Used for self-consistency ("Did I handle a similar case before?")

**Problem**: Notes are not shared. Different moderators may decide the same case differently.

**Example inconsistency**: Sarah and another mod both review harsh critique posts, Sarah applies painters sub "invitation" rule strictly, other mod is more permissive. Users experience inconsistent moderation.

**Codifiability**: **Medium** - precedent cases can be structured as training data or decision trees  
**Agent design implication**: Agent maintains shared case library, suggests similar precedents during grey-zone review

#### Discord #mod-decisions Channel

**Purpose**: Real-time coordination, second opinions, precedent discussion

**Usage patterns**:
- "This post - within painters norm or harassment?" 
- "I approved this, if you disagree override me"
- "Heads up, sponsor X is sensitive this week"

**Response time**: 10-30 minutes, timezone-dependent (Klaus in Germany, Aki in Japan, Sarah in UK)

**Problem**: No formal record, no searchable precedent database, timezone gaps leave moderators isolated

**Codifiability**: **Medium** - Discord logs can be mined for precedent patterns, but informal language makes extraction difficult  
**Agent design implication**: Agent escalation should integrate with Discord (post escalation, get human response, close loop)

### 5. Context-Gathering Overhead (20% of Grey-Zone Time)

**Sarah's workflow for a grey-zone case:**

1. **Read flagged post** (10 seconds)
2. **Open user profile in new tab** (5 seconds)
3. **Review user post history** (30-60 seconds) - looking for: account age, participation quality, prior violations
4. **Check subforum-specific rules** (20-30 seconds) - navigate to subforum, read pinned rules thread
5. **Search personal notes** (15-30 seconds) - Ctrl+F in Google Doc for similar cases
6. **Search Discord #mod-decisions** (30-60 seconds) - scroll back through channel for precedents or current discussions
7. **Check if user is on Tom's watchlist** (10-20 seconds) - scroll Discord for Tom's messages or guess based on memory

**Total context-gathering time**: 2-3 minutes per grey-zone case

**With 360 grey-zone cases/day across team**: 12-18 hours/day spent on context-gathering

**What Sarah wants**: "If I clicked on a flagged post and immediately saw: user history summary, subforum-specific rules that might apply, whether they're on any watchlists, similar past cases and how they were resolved... I'd save maybe 2-3 minutes per grey-zone case."

**Agent opportunity**: Aggregate context automatically, present to moderator in single view, reduce 2-3 min to 10-20 seconds.

### 6. Escalation Patterns (Actual vs. Policy)

**Policy**: "Escalate when uncertain."

**Sarah's practice**: Escalates ~1 in 10 grey cases (~10% escalation rate)

**Why the gap?**  
Sarah: "If I escalated every grey case, Tom would murder me."

**Escalation triggers** (Sarah's actual decision tree):

1. **Always escalate**:
   - Sponsor accounts (100% - existential risk after 2024 incident)
   - High engagement (>20 reactions - community backlash risk)
   - Users on Tom's watchlist (when aware of them)

2. **Escalate if uncertain**:
   - 50-50 split after context-gathering
   - No precedent in personal notes
   - Subforum norm ambiguity (e.g., historical imagery sensitivity)

3. **Don't escalate** (decide independently):
   - Clear patterns (even if grey) with precedent
   - Painters sub invitation rule violations (clear norm)
   - Off-topic commercial from new users (clear policy)

**Escalation channels**:
- **Discord #mod-decisions** (peer consensus, 10-30 min response)
- **Direct flag to Tom/Senior Mod** (high-stakes cases, hours to 1-day response)
- **Email** (IP claims, appeals - outside moderation queue)

**The friction**: Escalation creates wait time. If Sarah escalates 30% of grey cases and wait time is 20 minutes average, that's 36 hours/day of moderator wait time across the team.

**Balance**: Moderators self-filter escalations to avoid overloading Tom and avoid delays.

**Agent implication**: Agent can escalate more freely than humans (no social cost, no overload perception), but escalations must include rich context to avoid creating Tom backlog.

### 7. Tool Fragmentation & Coordination Overhead

**Sarah's screen setup during moderation:**

| Window/Tab | Purpose | Pain Point |
|------------|---------|------------|
| **Discourse moderation queue** | Flagged posts list | No context visible - must click into each post |
| **Discourse user profile** (new tab) | Check account age, post history | Manual navigation, slow loading |
| **Discord #mod-decisions** (2nd monitor) | Ask questions, see discussions | No link to specific posts, scroll-heavy |
| **Google Doc** (personal notes) | Precedent search | Not shared, inconsistent naming |
| **Subforum rules thread** (new tab) | Check subforum-specific norms | Buried in pinned posts, not indexed |
| **Tom's Discord messages** (scroll back) | Watchlist awareness | Temporal, no persistence, easy to miss |

**The problem**: No integration. Every grey-zone case requires 3-5 window/tab switches and manual search.

**Coordination overhead**: Sarah estimates 20% of grey-zone time is tool navigation, not decision-making.

**Agent opportunity**: Single-pane-of-glass context view - all relevant info in one escalation card.

### 8. Risk Tolerance Asymmetry (Moderators vs. Management)

**Sarah's risk hierarchy:**
1. **Missing harassment** - "If someone is genuinely targeted and we don't catch it, that's a failure."
2. **Wrongly removing established members' content** - "They've built reputation over years - if we remove their post, they lose trust in us."
3. **Sponsor incidents** - "Those are existential because they threaten revenue."

**Tom's risk hierarchy** (from stakeholder brief):
1. **Sponsor incidents** - "False negatives are existential" (revenue-critical)
2. **Viral false negatives** - Public backlash, community trust erosion
3. **Missing harassment** - Community safety

**The tension**: Sarah (volunteer, community-focused) prioritizes user protection. Tom (management, business-focused) prioritizes business continuity.

**Impact on moderation decisions**:
- Sarah errs toward **not removing** ambiguous critique ("better to escalate than censor")
- Tom wants **aggressive removal** of potential viral content ("false positives are survivable")

**Agent design implication**: Agent risk posture must align with **Tom's hierarchy** (management owns the risk), but moderators need transparency to understand why agent makes decisions differently than they would.

### 9. Training & Onboarding (Hidden Learning Curve)

**New moderator onboarding** (Sarah's description):

1. **Week 1**: Tom gives 14-page policy, 30-min call, access to Discourse/Discord
2. **Weeks 2-4**: "Training wheels" - new mod escalates everything, Tom/Senior Mod reviews decisions
3. **Weeks 5-8**: Gradually reduce escalation rate as new mod learns subforum norms, tribal knowledge, patterns
4. **Month 2+**: Independent moderation with occasional questions

**What's NOT in the policy**:
- Subforum-specific norms (learned by watching or being corrected)
- Spam patterns (learned by pattern exposure)
- Watchlist awareness (learned from Discord mentions)
- Escalation etiquette (when to ask peers vs. Tom)

**Learning sources**:
- Observation (watching other moderators' decisions)
- Correction (Tom/Aki overrides + explanation)
- Discord osmosis (reading #mod-decisions)

**Codifiability**: **High** - training materials can be structured from discovered patterns  
**Agent opportunity**: Agent training mode - explains why it made decisions, surfaces precedents, trains new moderators faster

### 10. Exception Workflows (Outside Standard Queue)

#### IP Claims (Separate Channel)

**Trigger**: Sculptor emails Tom claiming copyright on posted miniature photo

**Workflow**:
1. Tom receives email
2. Tom triages: Legitimate sculptor or troll?
3. If legitimate: Tom or Senior Mod investigates (30-45 min)
   - Check sculptor's website
   - Verify claim against user's post
   - Read commercial license fine print
   - Assess whether user credited sculptor
4. Tom decides: Takedown, no action, or disputed (legal review)

**Volume**: ~3-5 per week (low volume)

**Complexity**: High - legal sensitivity, relationship management (sculptors may be sponsors or community VIPs)

**Agent suitability**: **Very low** - human-only, but agent could assist with triage (urgency scoring, evidence gathering)

#### User Appeals (Async Handoff)

**Trigger**: User whose post was removed appeals the decision

**Workflow**:
1. User submits appeal via Discourse message or email
2. Tom reviews appeal
3. Tom asks original moderator to justify decision
4. Tom decides: Uphold removal, restore post, or partial action
5. Tom notifies user (24-48 hr SLA)

**Volume**: ~60/day (from scenario brief)  
**Effort per case**: ~45 min (Tom review + moderator justification + resolution)  
**Total**: ~45 hrs/day (?? - this doesn't match the 8 hrs/day in problem statement, need to validate)

**Sarah's experience**: Overturned once in 3 years (missed "feedback wanted" in thread title)

**Agent suitability**: **Low** - human-led, but agent could gather context (original post, moderation rationale, similar cases, user history) to speed up Tom's review

#### Appeals Math Discrepancy

**Problem statement claim**: 60 appeals/day, 8 min/case = 8 hrs/day  
**Sarah's description**: Tom's appeals take ~45 min each (review + back-and-forth)  
**Calculation**: 60 × 45 min = 45 hrs/day (!)

**Hypothesis**: Either:
1. Most appeals are simple (user checks a box, Tom auto-responds) - only complex ones take 45 min
2. Appeals are lower volume than 60/day in practice
3. Tom batches appeals and spends 8 hrs/day total, ~8 min average but high variance

**Action**: Validate with Tom in discovery interview.

---

## Cognitive Load Analysis

### High Cognitive Load Activities

These activities require active reasoning, pattern integration, or judgment:

1. **Grey-zone assessment** (harsh critique vs. harassment)
   - **Cognitive demand**: High - multi-signal integration, cultural interpretation
   - **Frequency**: 360/day across team
   - **Effort**: 4-5 min per case

2. **Subforum norm application** (invitation rule, historical context)
   - **Cognitive demand**: Medium-High - requires subforum-specific knowledge
   - **Frequency**: ~20% of grey-zone cases (72/day)
   - **Effort**: 1-2 min additional per case

3. **Escalation decision** ("Should I escalate or decide?")
   - **Cognitive demand**: Medium - meta-decision about confidence
   - **Frequency**: Every grey-zone case (360/day)
   - **Effort**: 10-20 seconds

4. **Context integration** (user history + subforum norms + precedents)
   - **Cognitive demand**: Medium - information retrieval and synthesis
   - **Frequency**: Every grey-zone case (360/day)
   - **Effort**: 2-3 min per case (mostly manual tool navigation)

5. **IP claim investigation** (copyright assessment, legal implications)
   - **Cognitive demand**: Very High - legal reasoning, relationship management
   - **Frequency**: 3-5/week
   - **Effort**: 30-45 min per case

### Low Cognitive Load Activities (Automatable)

These activities require pattern matching but minimal reasoning:

1. **Spam pattern recognition** (link farms, bots, gibberish)
   - **Cognitive demand**: Very Low - instant pattern match
   - **Frequency**: 1,080/day
   - **Effort**: 2 sec to identify, 30 sec to remove

2. **Clear policy violations** (hate speech, doxxing)
   - **Cognitive demand**: Low - obvious boundary transgression
   - **Frequency**: Small subset of queue (estimated 5%, ~75/day)
   - **Effort**: 10-20 sec

3. **Logging/documentation** (click buttons, select reasons)
   - **Cognitive demand**: None - mechanical
   - **Frequency**: Every action (1,500/day)
   - **Effort**: 5-10 sec per action

### Cognitive Zones (Where Humans Get Stuck)

**ATX concept**: Cognitive Zones are phases within a Job to be Done where effort is concentrated.

For moderation, the cognitive zones are:

| Zone | Description | Effort Distribution | Automation Potential |
|------|-------------|---------------------|----------------------|
| **Pattern Recognition** | Is this spam or not? | 5% (spam is obvious) | **Very High** - 95%+ accuracy achievable |
| **Context Gathering** | What's the user history, subforum norm, precedent? | 40% of grey-zone time | **High** - automate retrieval, human consumes |
| **Judgment** | Is this critique or harassment? | 50% of grey-zone time | **Low** - requires human cultural reasoning |
| **Action Execution** | Click remove, log reason | 5% | **Medium** - can automate if judgment is clear |

**Insight**: 40% of grey-zone effort (context gathering) is **high-effort, low-judgment** - prime automation target.

### Breakpoints (Where Humans Pause to Think)

**ATX concept**: Breakpoints are moments where work stops flowing and requires human decision.

Breakpoints in moderation workflow:

1. **"Is this spam or grey?"** (after quick scan)
   - **Frequency**: Every post (1,500/day)
   - **Resolution time**: 2 sec (spam) or 4-5 min (grey)
   - **Automation potential**: High for spam, low for grey

2. **"Does subforum norm apply?"** (painters invitation, historical permissiveness)
   - **Frequency**: ~20% of grey cases (72/day)
   - **Resolution time**: 30-60 sec (check rules)
   - **Automation potential**: Medium (can detect invitation patterns)

3. **"Should I escalate or decide?"** (confidence check)
   - **Frequency**: Every grey case (360/day)
   - **Resolution time**: 10-20 sec
   - **Automation potential**: Medium (agent can estimate confidence)

4. **"Waiting for Discord response"** (peer consultation)
   - **Frequency**: ~10% of grey cases (36/day)
   - **Resolution time**: 10-30 min wait
   - **Automation potential**: Low (human consensus needed) but workflow can be streamlined

5. **"Waiting for Tom decision"** (high-stakes escalation)
   - **Frequency**: Sponsor posts, high-engagement, 50-50 splits (estimated 50/day)
   - **Resolution time**: Hours to 1 day
   - **Automation potential**: Low (Tom decision needed) but context can be prepared

**Key insight**: Breakpoints #2, #3, #5 can be **accelerated** by agent context-gathering, even if human judgment is still required.

---

## Delegation Suitability Assessment

Based on discovery findings, here's the preliminary delegation suitability for each work stream:

### Work Stream 1: Routine Spam Removal

**Volume**: 1,080/day  
**Effort**: 9 hrs/day  
**Cognitive demand**: Very Low (pattern matching)  
**Sarah's quote**: "Just make it go away."

**Delegation suitability**: ⭐⭐⭐⭐⭐ **Fully Agentic**

**Rationale**:
- Clear patterns (link farms, bots, gibberish)
- Sarah matches patterns in 2 seconds with 99% accuracy
- Low risk (false positives are survivable, easily reversed)
- High volume justifies automation
- Moderators explicitly want this automated

**Delegation design**:
- Agent auto-removes when confidence >0.9
- Human sampling: 10-20% random audit daily
- User appeal path: moderator reviews within 24 hrs

### Work Stream 2: Grey-Zone Case Review

**Volume**: 360/day  
**Effort**: 30 hrs/day  
**Cognitive demand**: High (cultural interpretation, judgment)

**Delegation suitability**: ⭐⭐⭐ **Agent-led with Human Approval**

**Rationale**:
- Sarah explicitly doesn't trust AI with harsh critique vs. harassment boundary
- Risk of false negative (miss harassment) or false positive (censor critique) is high
- BUT: 40% of effort is context-gathering, which can be automated

**Delegation design**:
- Agent gathers context: user history, subforum norms, similar precedents, flag reasons
- Agent highlights key signals: invitation?, targets work or person?, user reputation
- Agent estimates confidence: "This looks like invited critique (0.8 confidence)"
- Human reviews context and decides: approve, remove, or escalate
- **Goal**: Reduce 4-5 min per case to 1-2 min with agent-prepared context

### Work Stream 3: User Dispute Appeals

**Volume**: 60/day  
**Effort**: 8 hrs/day (45 min per case if Sarah's description is accurate)  
**Cognitive demand**: Medium-High (requires review of original decision + justification)

**Delegation suitability**: ⭐⭐ **Human-led with Agent Context Support**

**Rationale**:
- Tom must personally review (management responsibility)
- Requires judgment call on whether original moderation was correct
- Low volume doesn't justify full automation
- BUT: Agent can prepare context (original post, moderation rationale, similar cases, user history)

**Delegation design**:
- Agent gathers appeal context when user submits
- Agent presents: original post, removal rationale, moderator who decided, similar past appeals, user's appeal argument
- Tom reviews and decides
- **Goal**: Reduce 45 min to 20 min with agent-prepared context

### Work Stream 4: IP Claim Resolution

**Volume**: 3-5/week  
**Effort**: 2 hrs/week  
**Cognitive demand**: Very High (legal reasoning, relationship management)

**Delegation suitability**: ⭐ **Human-only (Tom + Senior Mod)**

**Rationale**:
- Legal sensitivity (copyright law, commercial licenses)
- Relationship management (sculptors may be sponsors, community VIPs)
- Very low volume doesn't justify automation
- Requires Tom's business judgment

**Delegation design**:
- Agent could assist with triage: urgency scoring (established sculptor vs. unknown), evidence gathering (sculptor's website, license info)
- But decision remains 100% human

---

## Discovery Gaps & Next Steps

### What We Learned

✅ Spam patterns are clear and automatable  
✅ Context-gathering is high-effort, low-judgment (automation target)  
✅ Grey-zone boundary (critique vs. harassment) is hard to codify  
✅ Subforum norms are tribal knowledge, not documented  
✅ Tom's watchlist is not shared with moderators  
✅ Discord is the real coordination layer  
✅ Moderators want spam automated but don't trust AI with grey zones  
✅ Tool fragmentation creates 20% overhead  

### What We Still Need to Discover

❓ **Tom's perspective**: What's on the watchlist? What are the business constraints? What's the real 2024 sponsor incident story?  
❓ **Volume validation**: Are appeals really 60/day, or is that scenario fiction?  
❓ **Other moderators**: Do Klaus (Germany), Aki (Japan) have different patterns than Sarah (UK)?  
❓ **Discord log mining**: Can we extract precedent patterns from #mod-decisions history?  
❓ **Discourse data analysis**: What's the actual distribution of spam vs. grey-zone vs. clear violations?  
❓ **Subforum-specific data**: Does painters sub really have higher grey-zone rate than others?  
❓ **Sponsor account list**: Who are the 8-10 sponsors? What's their posting frequency?  

### Next Discovery Actions

1. **Interview Tom** (Community Manager, 60 min)
   - Validate findings from Sarah's perspective
   - Uncover watchlist patterns, sponsor relationships, 2024 incident details
   - Understand business constraints and risk tolerance
   - Clarify appeals volume and effort

2. **Interview Aki** (Japan-based volunteer moderator, 45 min)
   - Cultural interpretation challenges
   - Japanese painters sub norms
   - Timezone coordination issues

3. **Interview Klaus** (Germany-based volunteer moderator, 45 min)
   - Historical sub norms and sensitivity
   - Cross-timezone coordination with UK/US mods
   - Edge case patterns

4. **Discord log analysis** (8 hours)
   - Mine #mod-decisions for precedent patterns
   - Extract common questions, consensus decisions, escalation triggers
   - Map coordination patterns and response times

5. **Discourse data pull** (4 hours)
   - Pull 30 days of moderation queue data
   - Validate volume distribution: spam vs. grey-zone vs. clear violations
   - Analyze flag patterns, resolution times, moderator consistency
   - Extract actual post examples for test dataset

6. **Shadow observation** (6 hours - 2 hrs × 3 moderators)
   - Watch live moderation sessions
   - Time each step: scan, decide, context-gather, escalate
   - Observe tool navigation, Discord coordination in real-time
   - Capture edge cases that interviews might miss

---

## Implications for Agent Design

### Primary Design Principles (From Discovery)

1. **Automate what moderators resent, preserve what they value**
   - Sarah resents: "Clicking through crypto bots for the 500th time"
   - Sarah values: "Making nuanced cultural/artistic judgments"
   - **Design**: Agent handles spam, supports grey-zone judgment

2. **Make moderators faster and smarter, don't replace judgment**
   - Sarah's dream: "AI gathers context, I decide in 1 minute instead of 5"
   - Sarah's nightmare: "AI makes grey-zone calls and I have to fix mistakes"
   - **Design**: Agent = context aggregator + confidence estimator, human = decision-maker

3. **Transparency is trust prerequisite**
   - Sarah: "Show me why it made each decision. Let me audit. Make overrides easy."
   - **Design**: Every agent action logged with rationale, confidence, policy reference; daily human audit

4. **Start small, prove safety, then expand**
   - Sarah: "Automate spam first, prove it works. If it tries grey-zone on day one and fails, I'll never trust it."
   - **Design**: Phase 1 = spam only, Phase 2 = grey-zone context support after validation

5. **Bias toward escalation on ambiguity**
   - Tom's constraint: "False negatives are existential"
   - Sarah's practice: "Better to escalate than censor"
   - **Design**: Agent confidence threshold set conservatively (0.7+), escalate on uncertainty

### Escalation Triggers (From Discovery)

Based on Sarah's actual practice, agent should **always escalate** to human:

1. **Sponsor accounts** (100% - existential risk)
2. **High engagement** (>20 reactions - community backlash risk)
3. **Users on watchlist** (Tom's Sheet - business/relationship sensitivity)
4. **Confidence <0.7** (model uncertainty)
5. **Subforum norm ambiguity** (painters invitation unclear, historical imagery sensitivity)
6. **Cultural interpretation needed** (Japanese sub, sarcasm detection)
7. **Policy boundary cases** (commercial content from established members)

**Do not escalate** (agent decides):
- Clear spam patterns (link farms, bots, gibberish) with confidence >0.9
- Clear policy violations (hate speech, doxxing) with confidence >0.9
- Obvious off-topic posts from new users

### Context Aggregation Requirements

For grey-zone cases, agent must surface:

**User context:**
- Account age, post count, reputation score
- Post history quality (helpful contributions vs. trolling)
- Prior moderation actions (warnings, removals)
- Whether user is on watchlist

**Content context:**
- Subforum and subforum-specific norms that apply
- Thread context (invitation signals: "tips?", "feedback wanted")
- Post engagement (reaction count, replies)
- Flagging reasons and flag count

**Precedent context:**
- Similar past cases and how they were resolved
- Moderator who decided (if relevant)
- Outcome (approved, removed, appealed)

**Confidence estimate:**
- "This looks like [invited critique / harassment / spam] with [0.X] confidence"
- Key signals that drove the estimate
- What would change the decision (e.g., "If not invited, would be norm violation")

**Goal**: Moderator can decide in 30-60 seconds instead of 4-5 minutes.

---

## Appendix: Interview Transcript Excerpts

### On Spam Patterns

> **Sarah**: "I can spot spam in about 2 seconds - are there multiple URLs? Is the username gibberish or a brand name? Is it a new account? Is the post in a subforum that makes no sense? If yes to 2+ of those, I remove it. Maybe 30 seconds total including the clicks."

> **You**: "How often do you get it wrong?"  
> **Sarah**: "Maybe 1% of the time? And if I accidentally ban a human thinking they're a bot, they appeal, Tom reverses it, I apologize, we move on. Has happened maybe 3 times in 3 years."

### On Grey-Zone Decision-Making

> **Sarah**: "The difference is... context. Clear violations are context-independent. Grey zones require you to know the user, the subforum, the thread, the history."

> **You**: "Can you articulate the decision rule for harsh critique vs. harassment?"  
> **Sarah**: "*long pause* Not really. I think... harassment targets the person, critique targets the work? But that's not always clear."

### On Trust in AI

> **Sarah**: "If there was a system that auto-removed obvious spam and let me audit it later if I wanted, I'd spend my entire session on the cases that actually matter."

> **You**: "Would you trust AI to handle grey-zone cases?"  
> **Sarah**: "*firmly* No. Those require judgment. What I'd want is AI to gather the context - show me the user history, flag subforum-specific rules, highlight similar cases - and then I decide. Make me faster and smarter, don't replace my judgment."

### On the 2024 Sponsor Incident

> **Sarah**: "One of the moderators auto-removed a post from a sponsor account that was flagged as 'commercial spam.' It wasn't spam, it was the sponsor announcing a new product line, which they're contractually allowed to do. The sponsor emailed the platform owner threatening to pull their sponsorship. Tom implemented the rule: no automated action on sponsor accounts, ever."

### On Tool Fragmentation

> **Sarah**: "I have three windows open: Discourse queue, Discord, and my Google Doc. If I want to check if someone's on Tom's watchlist, I scroll back through Discord or ask directly. [...] Maybe 20% of my grey-zone time is just navigating between tools."

---

## Document Control

**Version History**:
- v1.0 (2026-04-29): Initial discovery findings from Sarah interview

**Next Steps**:
- Conduct Tom interview (validate findings, uncover watchlist/business context)
- Conduct Aki and Klaus interviews (validate cross-moderator consistency)
- Perform Discord log analysis and Discourse data pull
- Synthesize into Cognitive Load Map and Delegation Suitability Matrix

**Related Documents**:
- `01_Problem_Statement_and_Success_Metrics.md` (Business context)
- `03_Delegation_Suitability_Matrix.md` (ATX scoring - to be created)
- `04_Agent_Purpose_Document.md` (Agent design spec - to be created)
