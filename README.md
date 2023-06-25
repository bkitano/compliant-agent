# `compliant-agent`

## Overview
Regular agents will often just do stuff! Ours follows the law. 

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
- Compliance check
- Action or Finish
