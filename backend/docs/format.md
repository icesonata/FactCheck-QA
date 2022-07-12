`Retriever`:
```json
{
    "full-text": {
        "count": <int>,
        "max_score": <float>,
        "min_score": <float>,
        "docs": [
            {
                "id": <str>,
                "content" <str>,
                "text_score": <float>,
                "semantic_score": <float>,
            },
            ...
        ]
    },
    "re-ranking": {
        "sentences": {      // id: sentence
            <int>: <str>,
            ...
        },
        "documents": [
            {
                "id": <str>,
                "content" <str>,
                "text_score": <float>,
                "semantic_score": <float>,
            }
            ...
        ]
    }
}
```

`Retriever`-`Reader`:
```json
{
    "answer": <str>,
    "document": {
        "content": <str>,
        "id": <str>,
        "semantic_score": <float>,
        "text_score": <float>,
    },
    "query": <str>
}
```

`Retriever`-`Inferrer`:
```json
{
    "claim": <str>,
    "data": [
        {
            "context": {
                "content": <str>,
                "id": <str>,
                "semantic_score": <float>,
                "text_score": <float>
            },
           "evidence": <str>,
           "inference_score": <float>,
           "label": <str>,  // `support` or `neutral` or `refute`
           "sent_id": <int>,
        },
           ...
    ],
    "insight": {
        "refute": <int>,
        "support": <int>,
        "neutral": <int>,
        "total": <int>,
    }
}
```
