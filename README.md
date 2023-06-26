# `compliant-agent`

## Overview
Regular agents will often just do stuff! Ours follows the law. 

### Installation
`poetry`

## Technical details
We're modifying the Zero-shot ReACT agent with Chain-of-Thought to also check for compliance.

The old agent:
- Observation
- Thought
- Action

Our agent:
- Observation
- Thought
- Proposed Action
- ***Compliance check***
- Action or Finish

### Knowledge Base
We have a vector database for retrieving relevant regulations and case law.

### Compliance Chain
Compliance chain is an agent Chain-of-Thought reasoning for determining if an action is compliant.

v0
1. Take in the action, embed it, and then look up the most relevant case law in FAISS.
1. Based on the case law, decide whether the action is legal or not. 
1. If it is, do the action. If it's not, flag with the relevant case law.

This agent is *not* conversational, it merely implements the Langchain Zero-shot ReACT pattern.

It's packaged as a tool, so that a tool-enabled conversational agent or another agent can invoke it via prompt, rather than having to modify the underlying agent orchestration.

### Example Chat Agent
The Example Chat Agent is a conversational Zero-shot ReACT agent.