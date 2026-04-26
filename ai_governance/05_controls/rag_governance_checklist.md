# RAG Governance Checklist

Retrieval-Augmented Generation systems require governance over both the model and the underlying knowledge sources.

## Source governance

- Are approved source repositories defined?
- Are source documents current and authoritative?
- Are document owners identified?
- Are outdated documents excluded?
- Are retention and records rules understood?

## Metadata and lineage

- Are documents tagged by owner, date, classification, and business function?
- Can AI outputs cite or identify the source documents used?
- Is there a process for removing deprecated content?
- Is there a process for correcting source documents?

## Access control

- Does the retrieval layer respect user permissions?
- Are confidential or restricted documents excluded for unauthorized users?
- Is access reviewed periodically?

## Output controls

- Are users told that generated answers require verification?
- Does the output include source references?
- Are hallucination checks performed?
- Are high-impact outputs reviewed before use?

## Monitoring

- Are failed answers or incorrect references logged?
- Are common retrieval gaps reviewed?
- Are source quality issues escalated to document owners?
