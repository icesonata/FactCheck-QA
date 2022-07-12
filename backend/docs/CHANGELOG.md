May 19, 2022:
- Change models/ to components/
- In models/, change absolute path to relative path, e.g., `from qa import QA` -> `from .qa import QA` or `import encoder_pb2 as encoder__pb2` -> `from . import encoder_pb2 as encoder__pb2`, so that the Django framework know and import the components.

May 28, 2022:
- Add Inferrer component to perform NLI task

Jun 1, 2022:
- Integrate the Inferrer with the Retriever.
- Modularize the Retriever such that the document retrieval feature is a separate feature.
- Compute `text-score` for retrieval results. Re-ranked results have another field related to semantic similarity, so-called `semantic-score`.
- Rename the `QA` module to `Reader`.
- Update the document in `docs/note.md` for `retrieve`, `retrieve_answer`, and `retrieve_inference` output formats.
- Complete inference, retrieve, question-answering services via APIs.
