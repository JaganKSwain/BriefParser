# Evaluation Guide
### Agentic AI Hackathon | 3rd April

---

## How Scoring Works

Every submission is evaluated across two equal halves. Each half carries 50 points, for a total of 100.

| Component | Weight | Method |
|---|---|---|
| Faculty Review | 50 points | Live presentation of your system at 2:30 PM( you must conitnue building it until 4 30, you will be called for 10 minutes for know what you have built |
| Workflow Verification | 50 points | Live deployment test or local run after the event is over by the team and evaluate on certain parameters |

Both components are mandatory. A team that does not present at 2:30 PM scores zero on the first half. A team whose system cannot be run scores zero on the second half.

---

## Component 1: Faculty Review (50 Points)

### What This Is

Starting at 2:30 PM, each team will present their system to a faculty panel. This is not a pitch. It is a technical walkthrough. You will be asked to explain how your system works, walk through your architecture, and answer direct questions about the decisions you made.

Presentations will be short. The panel will move through teams quickly. Be ready before your slot. Come with your architecture diagram open, your code accessible, and your summary document up.

### What You Will Be Evaluated On

**System understanding.** Can every member of your team explain what the system does, how it does it, and why it is built the way it is? Generic answers about "using AI to automate the workflow" will not score well. Specific answers about what the LLM decides at each step, what tools it calls, and how the system recovers from failure will.

**Architecture clarity.** Is your system well-designed? Does the architecture make sense for the problem you chose? Are the components connected logically, or did you bolt things together and hope for the best?

**Agentic design.** Where exactly is the LLM making decisions? What happens if you remove the LLM from that step? If the honest answer is "nothing changes," that step is not agentic.

**Edge case awareness.** Do you know where your system breaks? Do you know which edge cases you handled and which you did not? Teams that know their own limitations score higher than teams that discover them live.

**Technical depth.** You will be asked questions about the specific tools, APIs, and models you used. Surface-level familiarity will be visible immediately.

### Questions You Should Be Ready For

The panel will ask questions across the following areas. These are not the exact questions, but they cover the ground that will be covered.

**On your API and model setup**

What model are you using and why did you choose it over alternatives available to you today?

What is the rate limit on the API you are calling most frequently, and how does your system behave when it hits that limit?

If your API key stops working mid-demo, what happens to the rest of the pipeline?

How are you managing secrets and environment variables? Where does the API key live in your codebase?

What happens if the LLM returns a malformed response? Does your system handle that or does it crash?

Did you encounter any token limit constraints during building, and if so, how did you handle them?

**On your architecture and tools**

Why did you pick the specific orchestration framework or approach you used?

Walk us through one full agent loop from trigger to output. What happens at each step?

Which parts of your system are deterministic and which parts depend on LLM output? Where exactly is that boundary?

If the LLM hallucinates or produces an incorrect classification at a decision point, what does your system do?

**On the problem you chose**

What is the actual business cost of the problem you solved, and does your system fully address it?

Which edge cases from the problem statement did you not handle, and why?

---

## Component 2: Workflow Verification (50 Points)

### What This Is

Judges will run your system on a real or realistic input and observe what it does. This is not a presentation. This is execution. Your system either works or it does not.

### How Testing Will Happen

**If your system is deployed**, share the live link in your summary document. Judges will access it directly and run test inputs. You do not need to share API keys or environment files. This is the recommended path.

**If your system is not deployed**, share your repository. Judges will clone it and run it locally. For Python-based systems, this means running it via a local Python environment. For Node-based systems, this means running it via npm. Your README must make this possible without asking you for help. If a judge has to ask you how to run your own project, that is a deduction.

Hosting is strongly recommended. It removes the dependency on your machine, eliminates environment compatibility issues, and means you do not have to hand over your .env file or API keys to anyone. If you can get it deployed before 2:30 PM, do it.

### What Judges Will Test

A standard input will be run through your system. This input will be a realistic version of the input your chosen problem statement describes. For example, a new client form submission for PS-01, or a new brief form response for PS-02.

After the standard input, at least one edge case will be introduced. Judges will pick from the edge cases listed in your problem statement.

Judges will observe the following during the run:

Does the system complete the pipeline without manual intervention at any step?

Does the output land in the expected place in the expected format?

Do the LLM-driven steps produce outputs that make sense given the input?

Does the system handle the edge case gracefully, or does it fail silently, crash, or produce incorrect output?

Do the logs or traces show what the agent decided and why?

### Scoring Within This Component

| Criteria | Points |
|---|---|
| System runs end to end on standard input without errors | 20 |
| Output is complete, correctly formatted, and usable | 10 |
| At least one edge case handled correctly during the test | 10 |
| Agent decision points are visible and traceable in logs or output | 10 |

If the system cannot be run at all due to setup failure, missing dependencies, or broken environment configuration, the maximum score for this component is 10 points, awarded only if the code demonstrates a working architecture that would have functioned given a working setup.

---

## Honest Disclosure

Teams that disclosed known limitations in their summary document will not be penalised for those limitations during testing. Teams whose limitations are discovered by judges during the run, and were not disclosed, will be penalised.

Overstating the agentic percentage in your summary document and having that contradicted by the code is treated as a credibility failure. It affects scoring across both components, not just one.

---

## Timeline for the Day

| Time | Event |
|---|---|
| 11:00 AM | Hackathon begins |
| 2:30 PM | Faculty review presentations begin |
| 4:15 PM | Submission deadline, pull request must be open |
| 4:30 PM | Workflow verification begins |

---

*Judges' decisions are final. Evaluation criteria will not be adjusted after the event begins.*
