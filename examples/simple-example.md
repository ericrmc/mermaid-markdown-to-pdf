# Simple Example Document

This is a simple example demonstrating inline Mermaid diagrams.

## Introduction

This document shows how to use inline Mermaid code blocks that will be automatically converted to images in the PDF output.

## Basic Flow Chart

Here's a simple flowchart showing a basic process:

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

## Sequence Diagram

This sequence diagram shows a simple interaction:

```mermaid
sequenceDiagram
    participant User
    participant System
    participant Database
    
    User->>System: Request data
    System->>Database: Query
    Database-->>System: Results
    System-->>User: Display data
```

## Conclusion

Both diagrams above will be rendered as high-quality images in the PDF output.