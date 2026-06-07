# Assignment: Build a Personal Finance Assistant Agent using LangChain & SQLite

**Domain:** Agentic AI | **Tool:** LangChain
**Duration:** 90 Minutes | **Level:** Intermediate

---

## Problem Statement

Individuals often struggle to maintain a consistent and queryable record of their daily expenses. Existing solutions are either too complex, require paid subscriptions, or lack the ability to interact conversationally. There is a clear need for a lightweight, locally running personal finance assistant that can store, retrieve, update, and summarise transactions through natural language — without the user ever needing to open a spreadsheet or navigate a dashboard.

---

## Current Scenario

Most individuals track expenses either informally — through notes, memory, or rough spreadsheet entries — or not at all. This leads to a familiar set of problems:

- No reliable record of where money was spent across a week or month.
- Inability to query spending history in a natural, conversational way — for example, *"How much did I spend on food last week?"*
- Manual effort required to add, edit, or delete entries, which discourages consistent tracking.
- No single interface that can both store transactions and reason over them to surface useful insights.

A typical user ends up either abandoning expense tracking after a few days or relying on their bank statement at the end of the month — by which point it is too late to course-correct spending behaviour.

---

## Proposed Solution

Design and build a **LangChain-based Personal Finance Assistant Agent** backed by a **SQLite database** that serves as the persistent transaction store. The agent accepts natural language inputs from the user and autonomously decides which tool to invoke — whether that means adding a new expense, fetching a summary, updating a record, or deleting an entry.

The agent should be capable of:

- **Adding** a new transaction with details such as amount, category, date, and description.
- **Retrieving** transactions based on filters like category, date range, or amount threshold.
- **Updating** an existing transaction when the user wants to correct a detail.
- **Deleting** a transaction that was entered incorrectly.
- **Summarising** spending by category or time period to give the user a meaningful financial snapshot.

The SQLite database acts as the agent's persistent memory — ensuring that all recorded transactions survive across sessions and can be queried at any time.

---

## Assignment Objectives

### Learning Objectives
By the end of this assignment, participants will be able to:

1. Explain how a LangChain agent differs from a standard LLM call and why tool-based agents are better suited for tasks that require data persistence and multi-step operations.
2. Describe the role of each component in the agent pipeline — the LLM, the tool definitions, and the agent executor — and how they collaborate to fulfil a user request.
3. Articulate how an agent decides which tool to invoke based on the intent behind a natural language input.

### Implementation Objectives
By the end of this assignment, participants will be able to:

1. Design and initialise a SQLite database schema suitable for storing personal expense transactions.
2. Build individual LangChain tools that map to each CRUD operation — add, retrieve, update, and delete — along with a summary tool for aggregated insights.
3. Configure and initialise a LangChain agent that is wired to the above tools and backed by an appropriate LLM.
4. Interact with the agent using natural language inputs that trigger different tools and verify that the underlying database reflects the correct changes after each operation.
5. Handle a scenario where the user provides incomplete information — such as missing a category or amount — and observe or design how the agent responds in that situation.

---

## Scenario Walkthrough

To ground the implementation, participants will build the assistant for the following persona:

> **Arjun** is a 28-year-old software professional living in Bengaluru. He earns a monthly salary and wants to track his daily expenses across categories like Food, Transport, Utilities, Entertainment, and Miscellaneous. He wants to be able to add expenses quickly via chat, check how much he has spent in a category, fix wrongly entered records, and get a monthly summary — all without leaving a single conversational interface.

Participants will use Arjun's persona to design their test interactions and ensure the agent handles realistic, day-to-day financial queries.

---

## Suggested Tool Design

Participants are expected to define tools around the following operations. The exact implementation is left to the participant.

| Tool | Purpose |
|---|---|
| `add_transaction` | Add a new expense record to the database |
| `get_transactions` | Retrieve transactions filtered by category, date, or amount |
| `update_transaction` | Modify an existing transaction by its ID |
| `delete_transaction` | Remove a transaction from the database by its ID |
| `get_spending_summary` | Aggregate total spending by category or date range |

---
