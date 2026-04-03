# AGENTIC AI Hackathon — Case Study Document

**3rd April | 11:00 AM – 4:30 PM | Team Size: 1–3**

---

## What is an Agentic AI System?

An agentic AI system is a system that automates. Not just answering a question — but actually doing something about it.

The goal is automation. You give the system a goal, and it figures out the steps, picks the right tools, pulls the information it needs, makes decisions along the way, and produces a result — without you holding its hand through each step.

Think about the difference between a calculator and an accountant. A calculator answers what you ask. An accountant looks at your situation, decides what needs to happen, runs the numbers, cross-checks them, flags the anomaly, and hands you a finished report. That is the difference between a language model and an agent.

### The Building Blocks of an Agentic System

- **A goal** — what the system is trying to accomplish
- **A planning step** — breaking the goal into a sequence of actions
- **Tool access** — APIs, databases, search, external services the agent can call
- **Memory and context** — retaining what it learned in earlier steps to inform later ones
- **A decision loop** — evaluating progress and deciding what to do next
- **An output** — a meaningful, usable result

In this hackathon, you are building that. Not a chatbot. Not a prompt wrapper. A system that reads a real operational problem, plans an approach, calls the right tools, and delivers an end result that would have taken a human hours.

---

## The Company — Scrollhouse

Scrollhouse is a 60-person content company that creates short-form video content for brands. They have grown fast over the last two years — from 8 clients to over 22 active accounts — producing reels, scripts, briefs, and monthly performance reports across every vertical from skincare to fintech.

The content side works. The operations do not.

Everything described below is real. The workflows exist. The numbers are accurate. The broken systems are documented. Your job is to pick one problem and build an agent that fixes it — end to end.

---

## The Operations Manager's Account

The following is a direct account from Scrollhouse's operations manager, given on the first day of an internal review. Read every section carefully before selecting your problem statement.

---

## PS-01 — Client Onboarding

### What is currently happening

Every time Scrollhouse signs a new brand, the account manager responsible for that client has to manually execute a four-step onboarding sequence:

1. Write and send a welcome email to the brand
2. Create a shared Google Drive folder with standard subfolder structure
3. Set up a Notion page from a template
4. Add the client to the internal Airtable tracker

This entire sequence takes **45 minutes per client** when nothing goes wrong. Scrollhouse onboards between 6 and 10 new clients every month — that is between **4.5 and 7.5 hours** of an account manager's time, every month, on work that is entirely procedural and requires zero creative thinking.

But it does go wrong. The operations manager estimates that in roughly **half of all onboardings**, at least one step is missed or done incorrectly. The most common failure: the Airtable entry is either not created or is created with missing fields. The second most common: the Notion page is created from the wrong template version.

### Why this is a real business problem

A missed onboarding step has a compounding effect. If the Airtable entry is incomplete, invoices are delayed. If invoices are delayed, cash flow is affected. If the Google Drive folder isn't set up correctly, the first brief handover gets disorganised. If the Notion template is wrong, the first week of client communication happens without proper structure.

Three clients in the last six months have flagged onboarding issues in their first check-in call. One client asked whether Scrollhouse had done this before because the setup felt unstructured. That client renewed, but it was a close call.

### What the agent needs to do — end to end

1. **Receive the new client trigger** — a form submission or CRM update containing: brand name, account manager name, brand category, contract start date, monthly deliverable count, billing contact email, and invoice cycle
2. **Send the welcome email** — personalised with the brand name, account manager's name, a brief explanation of the Scrollhouse process, what the client can expect in the first two weeks, and a calendar link for the kickoff call
3. **Create the Google Drive folder** — under the correct parent directory, with the standard subfolder structure: `/Briefs`, `/Scripts`, `/Approved`, `/Footage`, `/Reports` — named with the brand name and contract start date
4. **Generate the share link and set permissions** — shared with the client's billing contact (comment-only access) and with the account manager (edit access)
5. **Create the Notion client hub** — from the current master template, populated with brand name, account manager, contract start date, deliverable count, and an auto-generated content calendar for the first month
6. **Add the client to Airtable** — with all required fields populated: brand name, account manager, start date, deliverable count, invoice date, billing contact, Google Drive link, Notion page link
7. **Send a completion summary to the account manager** — confirming all four steps are done, with direct links to the Drive folder, Notion page, and Airtable record
8. **Log the onboarding** — timestamp, steps completed, any errors encountered, resolution status

### Inputs

- New client form or CRM record
- Google Drive API
- Notion API
- Airtable API
- Email service

### Expected Outputs

- Welcome email sent to the brand's billing contact
- Google Drive folder created with correct structure and permissions
- Notion client hub created and populated from current template
- Airtable record created with all fields filled
- Completion summary sent to the account manager with links to all three
- Onboarding log entry with timestamp and step confirmation

### Edge Cases the Agent Must Handle

- **Email bounces** — flag to the account manager immediately and pause the welcome email step
- **Updated Notion template** — always pull the latest version, not a cached copy
- **Duplicate brand name in Airtable** — flag and request confirmation before creating a new record
- **Contract start date in the past** — flag and ask for confirmation rather than creating a retroactive record
- **Unrecognised account manager name** — flag the mismatch rather than creating a record with an unknown name
- **Google Drive API failure** — log the failure, retry once; if still failing, alert the account manager with manual instructions

### Tools This Problem is Suited For

| Tool | Use |
|------|-----|
| LangChain | Orchestrating the sequential multi-tool workflow |
| LangGraph | Managing conditional branches (duplicate check, error handling, retry logic) |
| n8n | Connecting to Google Drive, Notion, Airtable, and email APIs via webhook triggers |
| LangSmith | Auditing every step, every API call, and every field populated |

---

## PS-02 — Content Brief to Script Pipeline

### What is currently happening

Scrollhouse's clients submit content briefs through a Google Form. Once submitted, a content coordinator manually rewrites each brief into Scrollhouse's internal format — a step that takes **20 to 30 minutes per brief**. Scrollhouse processes **40 to 60 briefs every month**, totalling **13 to 30 hours per month** of coordinator time on a largely repeatable task.

After the internal brief is written, it is copied into a Notion page and the scriptwriter is tagged in Slack. On average, there is a **4 to 6 hour lag** between form submission and scriptwriter notification.

### Why this is a real business problem

The lag kills turnaround time. A brand submits a brief expecting a script within 48 hours — but 6 of those hours are gone before the scriptwriter even knows the brief exists.

There is also a quality consistency problem. Different coordinators interpret briefs differently. Two scripts have been returned by clients this quarter for being off-brief — in both cases, the issue was traced back to the interpretation step, not the scriptwriting.

### What the agent needs to do — end to end

1. **Detect the new brief** — via a Google Sheets webhook or polling trigger when a new row appears
2. **Parse the raw form response** — extract brand name, content type, topic, key message, target audience, mandatory inclusions, reference content URLs, and free-text notes
3. **Retrieve the brand context** — tone of voice guidelines, previous content examples, recurring themes, client-specific rules
4. **Interpret the client's intent** — identify the core hook opportunity, determine the emotion or insight the content should lead with, flag ambiguous or under-specified areas
5. **Rewrite into the internal brief format** — populate hook direction (2–3 options ranked by strength), tone of voice, visual treatment suggestion, scriptwriter notes, and a one-line brief summary
6. **Create the Notion brief page** — from the internal brief template, linked to the client's hub page
7. **Notify the assigned scriptwriter** — via Slack with brief summary, Notion link, content type, deadline, and urgency flags
8. **Update the brief tracker in Airtable** — status: Brief Received → Brief Processed, timestamp, scriptwriter assigned, Notion link
9. **Flag ambiguous briefs** — if the agent cannot confidently populate a critical field, flag for coordinator review before sending to the scriptwriter

### Inputs

- Google Form submission
- Brand database (tone of voice, content guidelines, past briefs, client-specific rules)
- Internal brief template
- Scriptwriter roster
- Slack and Notion API access
- Airtable access

### Expected Outputs

- Fully populated internal brief in Notion, linked to client hub
- Slack notification to scriptwriter with summary, Notion link, content type, and deadline
- Airtable tracker updated with status, timestamp, scriptwriter name, and Notion link
- Ambiguity flag (if applicable) sent to coordinator with specific fields needing clarification

### Edge Cases the Agent Must Handle

- **Critical fields left blank** — flag the brief as incomplete and send a follow-up request to the client before proceeding
- **Broken reference content URL** — note in the brief and proceed with available information
- **New content type for this client** — flag the lack of precedent for coordinator awareness
- **Unrecognised brand name** — flag as a potential new client or data entry error
- **Two briefs submitted simultaneously for the same client** — process independently; ensure they do not overwrite each other in the tracker
- **Assigned scriptwriter is on leave** — reassign to the backup scriptwriter and note the change in the tracker

### Tools This Problem is Suited For

| Tool | Use |
|------|-----|
| LangChain | Interpretation and rewriting step, pulling brand context and generating the internal brief |
| LangGraph | Conditional pipeline (missing fields → flag, complete brief → process and notify) |
| FAISS | Semantic retrieval of past briefs and brand guidelines from the knowledge base |
| n8n | Google Sheets webhook trigger, Slack notification, Notion page creation, and Airtable update |
| LangSmith | Tracing the interpretation step — what the agent read, inferred, and wrote |

---

## PS-03 — Content Approval Loop

### What is currently happening

Once a scriptwriter finishes a script, it is sent to the client via WhatsApp or email — and then tracked entirely in the team lead's head. There is no centralised system. No one at Scrollhouse knows, at any given moment, which scripts are waiting for feedback, approved, pending revisions, or sitting unseen in a client's inbox.

Scrollhouse manages **22 active clients**. At any point, there are between **8 and 15 scripts** in the approval loop simultaneously. The team lead described managing this as *'running 15 different conversations in my head at the same time.'*

### Why this is a real business problem

Scrollhouse has missed production deadlines because scripts sat in a client's inbox for 5 days without a follow-up. One client approved a script via WhatsApp and the message was never seen — the script went into a backlog and wasn't produced for 11 days. By then, the product launch it was meant to support had already happened.

The team lead spends an estimated **3 to 4 hours per week** on manual follow-up chasing.

### What the agent needs to do — end to end

1. **Receive the script submission** — triggers when a scriptwriter marks a script as 'Ready for Approval' in the tracker
2. **Retrieve the script and client contact details** — script text, client name, primary contact, preferred communication channel, and response SLA (usually 48 hours)
3. **Format and send the approval request** — channel-appropriate message with the script, a clear CTA (Approve / Request Revisions / Reject with reason), and a response deadline
4. **Log the send event** — timestamp, script ID, client, channel, and deadline
5. **Monitor for response** — check for client reply at defined intervals
6. **Send a follow-up at 24 hours** if no response — polite reminder referencing the original send and the deadline
7. **Send a second follow-up at 48 hours** if still no response — more direct message flagging that production is blocked
8. **Escalate to the account manager at 72 hours** — if no response after two follow-ups, alert the account manager with the script link and full follow-up history
9. **Process the client response:**
   - **Approved** → update status, notify scriptwriter and producer, move to production queue
   - **Revision requested** → extract revision notes, create a revision task assigned to the scriptwriter with client's comments attached
   - **Rejected** → log rejection with reason, escalate to account manager
10. **On revision resubmission** — repeat the approval request loop from step 3, tagged as a revised version

### Inputs

- Script submission trigger (status change in the content tracker)
- Script text from Notion or linked document
- Client contact record (name, preferred channel, contact details, SLA setting)
- WhatsApp Business API or email service
- Content tracker (Airtable or Notion)

### Expected Outputs

- Approval request sent to the client via the correct channel
- All follow-ups sent on schedule with context preserved
- Escalation triggered to account manager at 72 hours with full history
- Status updated in tracker at every stage
- Revision task created and assigned to scriptwriter when revisions are requested
- Production queue updated when script is approved

### Edge Cases the Agent Must Handle

- **Informal approval language** (e.g. thumbs-up emoji, 'looks good') — recognise as an approval rather than requiring a formal response
- **Partial feedback** — separate approved sections from revision requests
- **Out-of-sequence reply** — match the response to the correct script version
- **Client requests a call instead of written feedback** — log this, notify account manager to schedule the call, pause the automated follow-up loop
- **Client reviewing wrong script version** — include a version label in every approval request and flag version mismatches
- **Manual override by account manager** — respect pause requests without disrupting the tracking state

### Tools This Problem is Suited For

| Tool | Use |
|------|-----|
| LangChain | Formatting approval messages, parsing client responses, extracting revision notes from unstructured text |
| LangGraph | Managing the stateful follow-up loop with conditional branches |
| n8n | WhatsApp Business API and email integrations, tracker status updates, and scheduled follow-up triggers |
| LangSmith | Tracing every message sent, every response received, and every classification decision |

---

## PS-04 — Performance Reporting

### What is currently happening

At the end of every month, Scrollhouse sends each of its 22 active clients a performance report. The current process requires a team member to manually log into Instagram Insights and YouTube Studio for each client, note down metrics, paste them into a Google Sheet template, and write a short summary paragraph.

This process takes **2 to 3 hours per client**. With 22 active clients, the total monthly reporting effort is **44 to 66 person-hours**. Three people spend the majority of the first week of every new month doing nothing but this.

Reports are always late. Clients typically receive them between the **8th and 14th** of the following month. Clients start requesting them from the 3rd.

### Why this is a real business problem

Late reports create a trust problem. A client who doesn't receive their January performance data until January 14th cannot make informed decisions about their February content budget. Two clients have independently reduced their monthly spend with Scrollhouse, citing a lack of visibility into how previous content performed.

The commentary quality also degrades under volume — generic insights start appearing across multiple consecutive reports. One client printed the last three months of their reports side by side and pointed out that two summary paragraphs were identical except for the month name.

There is also a data integrity issue. Two clients received reports last quarter with incorrect follower counts. Both caught it. One escalated it.

### What the agent needs to do — end to end

1. **Trigger on the 1st of each month** — automatically, for all active clients in the Airtable roster
2. **Pull performance data** — from Instagram Graph API and YouTube Data API: total reach, impressions, profile visits, follower count (start and end of month), per-post metrics for every piece of content published
3. **Validate the data** — check for missing metrics, zero-value anomalies, and tracking gaps; flag inconsistencies
4. **Calculate derived metrics** — engagement rate per post, average engagement rate, follower growth rate, top 3 and bottom 3 performing posts, and month-over-month delta for all key metrics
5. **Retrieve client context** — content goals for the month, content types produced, topics covered, and client-specific KPIs from the Notion client hub
6. **Retrieve the previous month's report** — to reference trends over time and avoid repeating the same recommendations
7. **Generate the performance narrative** — 3 to 5 paragraphs covering: what happened this month, what worked and why, what underperformed and a hypothesis for why, and month-over-month comparison
8. **Generate the recommendations section** — 3 to 5 specific, data-backed actions for next month, specific to this client's data (not generic advice)
9. **Format the report** — summary metrics table, per-post performance table, narrative section, recommendations section, and an overall health label: **On Track / Needs Attention / Strong Month**
10. **Send the report to the client** — via email to the billing contact, with the account manager CC'd, and a personalised subject line referencing the brand and the month
11. **Update the tracker** — mark report as sent, timestamp, attach the report link

### Inputs

- Active client roster from Airtable
- Instagram Graph API
- YouTube Data API
- Notion client hub (content goals, KPIs, content calendar)
- Previous month's report
- Report template

### Expected Outputs

- Fully formatted performance report per client — on or before the 3rd of the month
- Report emailed to client with account manager CC'd
- Tracker updated with report sent status, timestamp, and link
- Data anomaly flags for any clients with inconsistent data
- Overall health label appended to each report

### Edge Cases the Agent Must Handle

- **Expired API access for a client** — flag immediately to the account manager with reconnection instructions; skip that client's report rather than sending partial or stale data
- **Client published zero content** — generate a report noting the gap; do not fabricate performance data
- **Viral post skewing averages** — identify the outlier, report it separately, and calculate averages both with and without it
- **Instagram account switched from personal to business mid-month** — flag the transition and note the data gap explicitly
- **No previous month's report (new client)** — generate without month-over-month comparison and note it's the first report on record
- **Posts deleted after publishing** — note the gap in the per-post table; do not treat missing data as zero performance

### Tools This Problem is Suited For

| Tool | Use |
|------|-----|
| LangChain | Data interpretation, narrative generation, and recommendation writing |
| LangGraph | Per-client pipeline with conditional branches (API failure → flag, anomaly → review, complete data → generate) |
| LangDB | Querying structured performance data and storing historical report records |
| FAISS | Retrieving past reports and client context to ensure narrative continuity |
| n8n | Scheduled monthly triggers, API calls to Instagram and YouTube, email delivery, and tracker updates |
| LangSmith | Auditing what data was pulled, what the model interpreted, and what was sent |

---

## Permitted Tools

| Tool | Recommended Use |
|------|----------------|
| LangChain | Agent orchestration, chain-of-thought reasoning, tool binding, and prompt management |
| LangGraph | Stateful multi-step agent flows, conditional branching, loop management |
| LangDB | Managed AI infrastructure, structured data querying, and model routing |
| LangSmith | Agent tracing, step-level debugging, and output quality evaluation |
| FAISS | Vector similarity search for semantic retrieval and RAG pipelines |
| n8n | Workflow automation, API triggers, webhook integrations, and scheduled tasks |

You may combine these however your architecture requires. You are not restricted to only these — but your core agent logic must involve at least one tool from this list.

---

## Rules

- Team size is **1 to 3 participants**. No exceptions.
- Each team must select **exactly one problem statement**. You cannot split across two.
- You may use any AI model, any additional libraries, and any stack you want.
- You must **build during the event**. Pre-built systems submitted as original work are disqualified.
- Using AI to help you code is expected. Submitting someone else's work is not.
- A clean working solution that handles real inputs beats an over-engineered system that breaks on the first edge case.

---

> **A chatbot speaks. An agent acts.**
>
> Good luck. We are genuinely excited to see what you build.
