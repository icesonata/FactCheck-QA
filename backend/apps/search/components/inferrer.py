from typing import Dict, List, Union

from transformers import pipeline


class Inferrer:
    """Component responsible for inference."""

    DEFAULT_LB_POSITIVE = "entailment"
    DEFAULT_LB_NEUTRAL = "neutral"
    DEFAULT_LB_NEGATIVE = "contradiction"

    LB_POSITIVE = "support"
    LB_NEUTRAL = "neutral"
    LB_NEGATIVE = "refute"
    LABEL = {
        DEFAULT_LB_POSITIVE: LB_POSITIVE,
        DEFAULT_LB_NEUTRAL: LB_NEUTRAL,
        DEFAULT_LB_NEGATIVE: LB_NEGATIVE,
    }

    def __init__(
        self,
        model: str,
        device: int,
    ) -> None:
        self._config = {
            "model": model,
            "device": device,
        }
        self.inferrer = pipeline(
            "text-classification",
            model=model,
            tokenizer=model,
            device=device,
            framework="pt",
            return_all_scores=True,
            function_to_apply="softmax",
        )
        # self.inferrer = pipeline(
        #     "zero-shot-classification",
        #     model=model,
        #     tokenizer=model,
        #     device=device,
        #     framework="pt",
        #     candidate_labels=["entailment", "neutral", "contradiction"],
        # )

    def get_inference(
        self,
        sentences: Dict[int, str],
        query: str,
    ) -> Dict[str, Dict[str, Union[int, float, str]]]:
        """Get inference result between the given query and the retrieved results.

        Args:
            sentences (Dict[int, str]): list of retrieved sentences.
            {
                <int>: <str>,
                ...
            }
            query (str): user's query

        Returns:
            Dict: inference (confidence) scores with three criteria
            according to NLI task.
                Format:
                {
                    "insight":
                    {
                        "total": <int>,
                        "entailment": <int>,
                        "neutral": <int>,
                        "contradiction": <int>,
                    },
                    "data": [
                        {
                            "sent_id": <int>,
                            "hypothesis": <str>,
                            "label": <str>,
                            "score": <float>,
                        }
                    ]
                }
        """
        results = {
            "claim": query,
            "data": [],
            "insight": {
                "total": len(sentences),
                self.LB_POSITIVE: 0,
                self.LB_NEGATIVE: 0,
                self.LB_NEUTRAL: 0,
            }
        }
        for sent_id, evidence in sentences.items():
            output: List[List[Dict]] = self.inferrer(
                " ".join((query, evidence)))
            max_label: Dict = max(output[0], key=lambda elem: elem["score"])

            prob = max_label["score"]
            label = self.LABEL[max_label["label"].lower()]
            results["data"].append(
                {
                    "sent_id": sent_id,
                    "evidence": evidence,
                    "label": label,
                    "inference_score": prob,
                },
            )
            results["insight"][label] += 1

        return results

    def __str__(self) -> str:
        return "model={!r}; device={}".format(
            self._config["model"],
            self._config["device"],
        )

    def __repr__(self) -> str:
        return "{}(model={!r},device={})".format(
            self.__class__.__name__,
            self._config["model"],
            self._config["device"],
        )
