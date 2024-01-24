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


classDef db_color fill:#F7B801,stroke:#F18701,stroke-width:2px;
classDef ai_color fill:#7678ED,stroke:3d348b,stroke-width:4px;
classDef user_color fill:#7eb09b,stroke:#519e8a,stroke-width:4px;

    class A,D db_color
    class F,C,I,H,B ai_color
    class J,E user_color


style A color:#FFF;
style B color:#FFF;
style C color:#FFF;
style D color:#FFF;
style E color:#FFF;
style F color:#FFF;
style H color:#FFF;
style I color:#FFF;
style J color:#FFF;
```

```
