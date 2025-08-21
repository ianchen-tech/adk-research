```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                Head Coach (Sequential)                                      │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────┐                                │
│  │               Reference Coach (Parallel)                │                                │
│  │                                                         │                                │
│  │          ┌─────────────────────────────────┐            │                                │
│  │          │        Data Coach (Loop)        │            │                                │
│  │          │                                 │            │                                │
│  │          │  ┌─────────┐    ┌─────────────┐ │            │    ┌─────────────────────────┐ │
│  │          │  │   SQL   │───▶│    Query    │ │            │───▶│     Analytics Coach     │ │
│  │          │  │  Coach  │    │    Coach    │ │            │    └─────────────────────────┘ │
│  │          │  └─────────┘    └─────────────┘ │            │                                │
│  │          └─────────────────────────────────┘            │                                │
│  │          ┌─────────────────────────────────┐            │                                │
│  │          │           Scout Coach           │            │                                │
│  │          └─────────────────────────────────┘            │                                │
│  │                                                         │                                │
│  └─────────────────────────────────────────────────────────┘                                │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

```
graph TD
    A[Head Coach - Sequential] --> B[Reference Coach - Parallel]
    B --> C[Data Coach - Loop]
    B --> D[Scout Coach]
    B --> E[Analytics Coach]
    C --> F[SQL Coach]
    C --> G[Query Coach]
    F --> G
```

```mermaid
graph TD
    A[Head Coach - Sequential] --> B[Reference Coach - Parallel]
    B --> C[Data Coach - Loop]
    B --> D[Scout Coach]
    B --> E[Analytics Coach]
    C --> F[SQL Coach]
    C --> G[Query Coach]
    F --> G
```

```mermaid
graph TD
    HC["🎯 Head Coach<br/>(Sequential)"] --> RC["🔄 Reference Coach<br/>(Parallel)"]
    
    RC --> DC["🔁 Data Coach<br/>(Loop)"]
    RC --> SC["🕵️ Scout Coach"]
    RC --> AC["📈 Analytics Coach"]
    
    DC --> SQL["📊 SQL Coach"]
    DC --> QC["🔍 Query Coach"]
    SQL --> QC
    
    style HC fill:#e1f5fe
    style RC fill:#f3e5f5
    style DC fill:#fff3e0
    style SC fill:#e8f5e8
    style AC fill:#fce4ec
```