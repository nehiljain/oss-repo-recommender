# oss-repo-recommender


# Flow of the application

```mermaid
graph TD
    A[Github Repos] -->|Markdown Chunking| B(Chunks)
    B --> C[AI Embedding Model]
    C -->|Embeddings| D[Atlas Vector DB]
    E((Question)) --> F[Same Embedding Model]
    F -->|Query Embeddings| D
    D --> |Semantic Similarity Search| H[Question + Context Documents]
    E -->  H
    H --> I[LLM]
    I --> J((Answer))


classDef db_color fill:#F7B801,stroke:#F18701,stroke-width:2px,color:white;
classDef ai_color fill:#7678ED,stroke:#3d348b,stroke-width:4px,color:white
classDef user_color fill:#7eb09b,stroke:#519e8a,stroke-width:4px,color:white

    class A,D db_color
    class F,C,I,H,B ai_color
    class J,E user_color
```
