# Persona Graph Memory

## Overview

This project implements a **generative memory-reasoning framework** built on Large Language Models (LLMs) to extract, structure, and reason over conversational or narrative data. The system builds an evolving **persona memory graph** where entities, traits, events, and beliefs are extracted and linked as a graph enriched with **vector embeddings** for semantic search.

Unlike simple memory logs, this framework models how beliefs and traits evolve over time using a **reasoning schema** and records inference traces to provide explainability behind conclusions. The goal is to reconstruct *how meaning, identity, and reasoning* emerge interactively from ongoing conversations.

## Architecture

- **Memory Extractor**: Uses LLM prompts to parse unstructured text and extract structured facts as memory entries.
- **Memory Graph**: Represents persona data as nodes and edges with typed relations, allowing complex entity and event linkage.
- **Vector Index**: Embeds memory summaries into vector space for semantic similarity search.
- **Reasoning Engine**: Updates beliefs and traits with logical inference, tracking contradictions and confirmations.
- **Thought Tracer & Explanation Engine**: Logs reasoning steps and generates human-readable explanations.
- **Persistence Layer**: Stores and reloads graph and vector data to disk.

## Features

- Extract and summarize persona traits, preferences, and beliefs from raw text.
- Store and link memory entries as a dynamic graph.
- Perform semantic search with vector embeddings for related memories.
- Support reasoning to update or contradict beliefs.
- Provide explanation of reasoning chains.
- Visualize the memory graph interactively.
- Add new conversational data dynamically via API or UI.

## Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) running locally (for LLM & embeddings)
- Install dependencies:

```bash
pip install -r requirements.txt
