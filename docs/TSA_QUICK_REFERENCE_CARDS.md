# TSA QUICK REFERENCE CARDS
## Pocket Guides for Daily Work

---

# CARD 1: DAILY STANDUP CHEAT SHEET

```
┌─────────────────────────────────────────────────────┐
│           STANDUP QUICK GUIDE                       │
│                 (15 min max)                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  FORMAT:                                            │
│  1. Yesterday: What did I complete?                 │
│  2. Today: What will I work on?                     │
│  3. Blockers: What's in my way?                     │
│                                                     │
│  TIPS:                                              │
│  • Keep it under 2 minutes                          │
│  • Be specific (not "worked on stuff")              │
│  • Blockers = need help, not just hard              │
│  • Save discussions for after standup              │
│                                                     │
│  EXAMPLES:                                          │
│  Good: "Validated 5 QBO features for TCO"          │
│  Bad:  "Worked on QBO stuff"                        │
│                                                     │
│  Good: "Blocked: need AWS access to test"           │
│  Bad:  "Having some issues"                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 2: CUSTOMER CALL QUICK GUIDE

```
┌─────────────────────────────────────────────────────┐
│         CUSTOMER CALL SURVIVAL KIT                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  BEFORE THE CALL:                                   │
│  □ Review customer background in Salesforce         │
│  □ Check recent Slack threads about them            │
│  □ Prepare agenda (share 24h before)                │
│  □ Test your audio/video                            │
│  □ Have environment ready (if demo)                 │
│                                                     │
│  DURING THE CALL:                                   │
│  □ Start with introductions                         │
│  □ Confirm agenda and time                          │
│  □ Take notes (or assign note-taker)                │
│  □ Ask clarifying questions                         │
│  □ Summarize next steps before ending               │
│                                                     │
│  AFTER THE CALL:                                    │
│  □ Send summary email within 24h                    │
│  □ Update Salesforce notes                          │
│  □ Create Linear tickets for action items           │
│  □ Slack update to team if needed                   │
│                                                     │
│  MAGIC PHRASES:                                     │
│  • "Let me make sure I understand..."               │
│  • "What does success look like for you?"           │
│  • "I'll follow up on that by [date]"               │
│  • "That's a great question, let me check"          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 3: QBO VALIDATION QUICK GUIDE

```
┌─────────────────────────────────────────────────────┐
│          QBO FEATURE VALIDATION                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  LOGIN ACCOUNTS:                                    │
│  TCO: quickbooks-testuser-tco-tbxdemo@tbxofficial   │
│  CONST: quickbooks-test-account@tbxofficial         │
│  PRODUCT: quickbooks-tbx-product-team-test@...      │
│                                                     │
│  VALIDATION STEPS:                                  │
│  1. Login to correct QBO account                    │
│  2. Select correct company (e.g., Apex Tire)        │
│  3. Navigate to feature location                    │
│  4. Verify feature works as expected                │
│  5. Capture screenshot (full page)                  │
│  6. Annotate with arrows/highlights                 │
│  7. Save to G:\Meu Drive\TestBox\QBO-Evidence\      │
│  8. Update tracking spreadsheet                     │
│                                                     │
│  SCREENSHOT NAMING:                                 │
│  {DATE}_{PROJECT}_{CATEGORY}_{FEATURE}.png          │
│  Example: 2025-12-03_TCO_Traction_DTM_VendorNotes   │
│                                                     │
│  STATUS OPTIONS:                                    │
│  • Testing = In progress                            │
│  • Passed = Feature works correctly                 │
│  • Failed = Issue found (document it!)              │
│  • Blocked = Can't test (explain why)               │
│                                                     │
│  ESCALATION:                                        │
│  If feature fails → Document → QBO Lead → Intuit    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 4: ENVIRONMENT SETUP QUICK GUIDE

```
┌─────────────────────────────────────────────────────┐
│         ENVIRONMENT SETUP CHECKLIST                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  BEFORE YOU START:                                  │
│  □ Customer requirements documented?                │
│  □ Data specs received?                             │
│  □ Timeline confirmed?                              │
│  □ Approval from Solutions Lead?                    │
│                                                     │
│  SETUP SEQUENCE:                                    │
│  1. Create base environment                         │
│  2. Apply configuration template                    │
│  3. Create test users                               │
│  4. Import/configure data                           │
│  5. Set up integrations (if needed)                 │
│  6. Run validation checks                           │
│                                                     │
│  VALIDATION CHECKS:                                 │
│  □ All users can login                              │
│  □ Data displays correctly                          │
│  □ Core features work                               │
│  □ No error messages                                │
│  □ Performance acceptable                           │
│                                                     │
│  COMMON ISSUES:                                     │
│  • Data import fails → Check format                 │
│  • User can't login → Verify credentials            │
│  • Feature missing → Check permissions              │
│  • Slow performance → Clear cache/restart           │
│                                                     │
│  NEED HELP? → Slack #solutions-team                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 5: ESCALATION QUICK GUIDE

```
┌─────────────────────────────────────────────────────┐
│          WHEN & HOW TO ESCALATE                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ESCALATION PATH:                                   │
│                                                     │
│  Level 1: Buddy / Peer TSA                          │
│     ↓                                               │
│  Level 2: Senior TSA                                │
│     ↓                                               │
│  Level 3: Solutions Lead                            │
│     ↓                                               │
│  Level 4: VP/Director                               │
│                                                     │
│  WHEN TO ESCALATE:                                  │
│                                                     │
│  → To Buddy/Peer:                                   │
│    • "How do I do this?"                            │
│    • "Is this normal?"                              │
│    • Quick questions                                │
│                                                     │
│  → To Senior TSA:                                   │
│    • Complex technical issues                       │
│    • Customer relationship concerns                 │
│    • Process clarification                          │
│                                                     │
│  → To Solutions Lead:                               │
│    • Customer complaints                            │
│    • Timeline/scope changes                         │
│    • Resource needs                                 │
│    • Cross-team conflicts                           │
│                                                     │
│  → To VP/Director:                                  │
│    • Major incidents                                │
│    • Contract/legal issues                          │
│    • Strategic decisions                            │
│                                                     │
│  HOW TO ESCALATE:                                   │
│  1. Try to solve it yourself first (5-10 min)       │
│  2. Document what you tried                         │
│  3. Be specific about what you need                 │
│  4. Provide context (customer, timeline, impact)    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 6: SLACK ETIQUETTE

```
┌─────────────────────────────────────────────────────┐
│            SLACK COMMUNICATION GUIDE                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  KEY CHANNELS:                                      │
│  #solutions-team    Your home base                  │
│  #general           Company-wide                    │
│  #qbo-project       QBO validation work             │
│  #engineering       Tech questions                  │
│  #random            Fun stuff                       │
│                                                     │
│  RESPONSE TIME EXPECTATIONS:                        │
│  • Direct message: Same day                         │
│  • @mention: Within 2-4 hours                       │
│  • Channel post: Within 24 hours                    │
│  • Urgent? Say "URGENT" or use 🚨                   │
│                                                     │
│  DO:                                                │
│  ✓ Use threads for discussions                      │
│  ✓ Be clear and concise                             │
│  ✓ Use appropriate channel                          │
│  ✓ @mention specific people when needed             │
│  ✓ Set status when away                             │
│                                                     │
│  DON'T:                                             │
│  ✗ @channel or @here unless urgent                  │
│  ✗ Send multiple messages (combine them)            │
│  ✗ Discuss sensitive info in public channels        │
│  ✗ Expect instant responses                         │
│                                                     │
│  FORMATTING TIPS:                                   │
│  *bold* for emphasis                                │
│  `code` for technical terms                         │
│  > quote for referencing                            │
│  • bullets for lists                                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 7: LINEAR (TASK MANAGEMENT) QUICK GUIDE

```
┌─────────────────────────────────────────────────────┐
│              LINEAR BASICS                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CREATING TICKETS:                                  │
│  1. Click "+" or press "C"                          │
│  2. Write clear title (action + object)             │
│     Good: "Set up demo env for Acme Corp"           │
│     Bad:  "Acme stuff"                              │
│  3. Add description with context                    │
│  4. Set project and assignee                        │
│  5. Add labels if relevant                          │
│  6. Set priority and due date                       │
│                                                     │
│  PRIORITIES:                                        │
│  🔴 Urgent    = Today/ASAP                          │
│  🟠 High      = This week                           │
│  🟡 Medium    = This sprint                         │
│  🟢 Low       = Backlog                             │
│                                                     │
│  STATUS FLOW:                                       │
│  Backlog → Todo → In Progress → Done                │
│                                                     │
│  KEYBOARD SHORTCUTS:                                │
│  C = Create new issue                               │
│  I = Change assignee                                │
│  P = Set priority                                   │
│  L = Add labels                                     │
│  Cmd/Ctrl + Enter = Save                            │
│                                                     │
│  TSA-SPECIFIC LABELS:                               │
│  • customer-request                                 │
│  • environment-setup                                │
│  • qbo-validation                                   │
│  • documentation                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 8: SECURITY & DATA HANDLING

```
┌─────────────────────────────────────────────────────┐
│         SECURITY ESSENTIALS                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  GOLDEN RULES:                                      │
│  1. Never share credentials via Slack/email         │
│  2. Never store customer data on personal devices   │
│  3. Always use company-approved tools               │
│  4. Report suspicious activity immediately          │
│  5. Lock your screen when away (Cmd+L / Win+L)      │
│                                                     │
│  CUSTOMER DATA:                                     │
│  ✓ OK: Access in approved environments              │
│  ✓ OK: Share via secure channels                    │
│  ✗ NO: Download to personal computer                │
│  ✗ NO: Share with unauthorized people               │
│  ✗ NO: Use real customer data for testing           │
│                                                     │
│  PASSWORD RULES:                                    │
│  • Use password manager (1Password/LastPass)        │
│  • Never reuse passwords                            │
│  • Enable 2FA everywhere                            │
│  • Change if compromised                            │
│                                                     │
│  INCIDENT? DO THIS:                                 │
│  1. Don't panic                                     │
│  2. Document what happened                          │
│  3. Notify Solutions Lead immediately               │
│  4. Don't try to "fix" evidence                     │
│                                                     │
│  CONTACT FOR SECURITY:                              │
│  Slack: #security or DM [Security Lead]             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 9: FIRST WEEK SURVIVAL KIT

```
┌─────────────────────────────────────────────────────┐
│           FIRST WEEK TIPS                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  IT'S OKAY TO:                                      │
│  • Ask "dumb" questions (there are none)            │
│  • Not know everything                              │
│  • Take notes constantly                            │
│  • Ask for help early and often                     │
│  • Make mistakes (that's how we learn)              │
│  • Feel overwhelmed (it passes)                     │
│                                                     │
│  YOUR BUDDY IS THERE FOR:                           │
│  • Any question, big or small                       │
│  • Context and "how things really work"             │
│  • Introductions to people                          │
│  • Moral support                                    │
│                                                     │
│  QUICK WINS FOR WEEK 1:                             │
│  □ Complete Slack profile                           │
│  □ Introduce yourself in #general                   │
│  □ Schedule coffee chats with teammates             │
│  □ Read one customer case study                     │
│  □ Watch one recorded demo                          │
│  □ Explore the platform on your own                 │
│                                                     │
│  WHAT TO ASK YOUR BUDDY:                            │
│  • "What do you wish you knew on Day 1?"            │
│  • "Who should I definitely meet?"                  │
│  • "What's the biggest gotcha?"                     │
│  • "What's the best thing about working here?"      │
│                                                     │
│  REMEMBER:                                          │
│  Everyone was new once. We've got your back! 💪     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# CARD 10: KEY CONTACTS WALLET CARD

```
┌─────────────────────────────────────────────────────┐
│            KEY CONTACTS                             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  SOLUTIONS TEAM:                                    │
│  Solutions Lead ........... @[handle]               │
│  Senior TSA ............... @[handle]               │
│  QBO Project Lead ......... @[handle]               │
│  Your Buddy ............... @[handle]               │
│                                                     │
│  CROSS-FUNCTIONAL:                                  │
│  Engineering Lead ......... @[handle]               │
│  Product Lead ............. @[handle]               │
│  Sales Lead ............... @[handle]               │
│  Customer Success ......... @[handle]               │
│  DevOps ................... @[handle]               │
│  HR ....................... @[handle]               │
│                                                     │
│  FOR HELP WITH:                                     │
│  Technical issues → #engineering                    │
│  Customer questions → Senior TSA                    │
│  QBO validation → QBO Project Lead                  │
│  Tool access → IT / DevOps                          │
│  HR matters → HR                                    │
│  Anything else → Your buddy!                        │
│                                                     │
│  EMERGENCY ESCALATION:                              │
│  If truly urgent and no one responds:               │
│  Solutions Lead → VP/Director → CEO                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# PRINT INSTRUCTIONS

These cards are designed to be printed:
- **Format:** One card per page, landscape orientation
- **Paper:** Card stock recommended
- **Lamination:** Optional but helpful
- **Distribution:** Give to new TSA on Day 1

Digital version available in:
- Google Drive: /TSA Onboarding/Quick Reference Cards
- Notion: TSA Knowledge Base > Reference Cards

---

*Last Updated: December 2025*
*Questions? Contact Solutions Lead*
