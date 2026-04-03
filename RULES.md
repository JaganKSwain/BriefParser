# Hackathon Rules
### Agentic AI | 3rd April | 11:00 AM to 4:30 PM

---

## General

Team size is 1 to 3 participants. No exceptions.

Each team may select exactly one problem statement or as much they would want to from PS-01, PS-02, PS-03, or PS-04. You may split your work across two problem statements.

You must build during the event. Pre-built systems submitted as original work are grounds for immediate disqualification. Using AI to help you code is expected and encouraged. Submitting someone else's work is not.

A clean, working solution that handles real inputs will always be scored higher than an over-engineered system that breaks on the first edge case.

---

## API Keys and Model Access

You are responsible for sourcing your own API keys for any LLM provider you use. No keys will be provided at the event.

Free-tier options are acceptable and encouraged. Gemini Flash via Google AI Studio, open-source models via Hugging Face Inference API, Groq-hosted models, and similar free-access providers are all valid choices. There is no requirement to use a paid model.

You may use any model you want: Gemini, Claude, GPT, Mistral, LLaMA, Phi, anything. The model is not judged. The system built on top of it is.

---

## What Counts as Agentic

At least 60 percent of your system's operation must be genuinely agentic. This means LLM-driven decision making, not scripted branching.

The distinction matters. A system that calls an API in a fixed sequence is automation. A system where an LLM reads an input, decides what to do next, calls a tool, evaluates the result, and decides the next action is an agent. You are building the second thing.

Real agents must be present. This means at minimum: a reasoning step where the LLM determines what action to take, tool use where the LLM calls external services based on that reasoning, and a feedback loop where the result of one step informs the next.

LLM calls used only for text generation or formatting do not count toward the 60 percent agentic threshold. LLM calls used for planning, routing, classification, decision-making, error handling, and multi-step orchestration do.

---

## System Requirements

The system must be end to end and deterministic in its automation layer. Given the same inputs, the non-LLM parts of your system must produce the same operational outputs every time. No flaky triggers. No manual handoffs in the middle of the pipeline. No steps that require a human to move the process forward.

The agentic layer (LLM-driven decisions) may vary in phrasing and reasoning, but must not vary in what action it takes given the same input state. If the brief is incomplete, the agent must always flag it. Not sometimes. Every time.

Edge cases listed in your chosen problem statement must be handled. A system that only works on the happy path will be scored accordingly.

---

## Tech Stack

You may use any stack, any language, any framework, any library. There are no restrictions.

The tools listed in the problem document (LangChain, LangGraph, LangDB, LangSmith, FAISS, n8n) are recommended but not mandatory. If you can build a better system without them, do it.

Use whatever helps you move fastest. Claude Code, GitHub Copilot, Cursor, Codex, local models, anything. The only requirement is that what you submit is your team's own work, built today.

---

## MUST HAVES:

Systems must follow the following:

**Does it actually work.** Run it with a real or realistic input. Does it complete the pipeline without manual intervention?

**Is it genuinely agentic.** Where does the LLM make a decision rather than follow a script? How many real decision points exist in the agent loop?

**Does it handle edge cases.** Pick two or three edge cases from your problem statement and demonstrate them live.

**Is the output usable.** Would the output land in someone's inbox, tracker, or system in a state they could actually use? Or does it need cleanup before it's useful?

**Code quality and explainability.** You must be able to explain every component of your system. If you cannot explain why a part exists, it should not be in the submission.
---

*Additional rules may be appended before the event begins.*
