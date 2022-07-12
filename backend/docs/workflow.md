Core features:
- `api/search`: Search for relevant documents
  - Statistical-based search
  - Semantic re-ranking search
  - **Responsible components: Retriever**
- `api/inference`: Check the inference (correctness) of a given information
  - Get label and corresponding score of the inference result between the given premise (user query) with the data the system has.
  - **Responsible components: Retriever-Inferrer**
- `api/answering`: Search for an answer (including confidence score)
  - Check semantic score
  - Check statistical-based score
  - **Responsible components: Retriever-Reader**
- (Future) Add new data to the system (pipeline required)
 