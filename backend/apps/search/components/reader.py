from typing import Dict, List, Union

from transformers import pipeline


class Reader:
    """Control Question Answering model."""

    def __init__(
        self,
        model: str,
        device: int,
        mode: str = "concat",
    ) -> None:
        self._config = {
            "model": model,
            "device": device,
        }
        self.mode = mode
        self.qa_pipeline = pipeline(
            "question-answering",
            model=model,
            tokenizer=model,
            device=device,
        )

    # Step 13, 14, 15, 16
    def get_answer(
        self,
        sentences: Dict[int, str],
        query: str,
    ) -> Dict[str, Union[List[int], int, float, str]]:
        """Extract answer from given sentences in dictionary.

            Args:
                sentences (Dict[int, str]): mapping bewteen sentences' index and sentences' value
                {
                    <int>: <str>,
                    ...
                }
                query (str): user's query
                mode (str): using `concatenation` or `answers ensemble` method  

            Returns:
                dict: combinations of extracted answer and relevant information
                    Format:
                    {
                        "sent_id": [<int>],     // one or multiple answers
                        "answer": <str>,
                        "score": <float>,
                        "start": <int>,
                        "end": <int>
                    }
        """

        qa_result = None
        answer_sent_id = None

        if self.mode.lower() == "concat":
            # A mapping between start position of sentence and sentence's id
            sent_start_map = []     # list of tuple
            full_paragraph = ""
            for sent_id, sent in sentences.items():
                sent_start_map.append((len(full_paragraph), sent_id))
                full_paragraph += sent + " "

            qa_input = {
                "question": query,
                "context": full_paragraph,
            }
            qa_result = self.qa_pipeline(qa_input)
            
            # Get sentence's id by start index of answer in the full paragraph,
            # by brute forcing, assuming that the index ids are in ascending order
            answer_start_id = qa_result.get("start")
            answer_sent_id = []  # in case there're more than one answers
            prev_start_idx, prev_sent_id = sent_start_map[0]
            for i in range(1, len(sent_start_map)):
                start_idx, sent_id = sent_start_map[i]
                # Get index for the first match in full text
                if (
                    answer_start_id >= prev_start_idx and
                    answer_start_id <= start_idx
                ):
                    break
                prev_start_idx = start_idx
                prev_sent_id = sent_id

            answer_sent_id.append(prev_sent_id)

        elif self.mode.lower() == "ensemble":
            answers = {
                sent_id: self.qa_pipeline(dict(question=query, context=sent))
                for sent_id, sent in sentences.items()
            }
            # Get answer and corresponding sentence's index with maximum score
            answer_sent_id, qa_result = max(
                answers.items(),
                key=lambda elem: elem[1]["score"],
            )
            # Sync with concatenation implementation
            # in case we want to get more than one relevant answer in the future
            answer_sent_id = [answer_sent_id]

        else:
            raise ValueError("Inappropriate value for mode.")

        return {
            **qa_result,
            "sent_id": answer_sent_id,
        }

    def __str__(self) -> str:
        return "model={!r}; device={}; mode={!r}".format(
            self._config["model"],
            self._config["device"],
            self.mode,
        )

    def __repr__(self) -> str:
        return "{}(model={!r},device={},mode={!r})".format(
            self.__class__.__name__,
            self._config["model"],
            self._config["device"],
            self.mode,
        )
