from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

SYMPTOM_KEYWORDS: dict[str, list[str]] = {
    "fever": ["fever", "high temperature", "chills", "hot body"],
    "cough": ["cough", "coughing", "dry cough", "productive cough"],
    "headache": ["headache", "migraine", "head pain"],
    "fatigue": ["fatigue", "tired", "weakness", "exhausted"],
    "shortness_of_breath": ["shortness of breath", "breathless", "difficulty breathing", "dyspnea"],
    "chest_pain": ["chest pain", "pressure in chest", "tight chest"],
    "sore_throat": ["sore throat", "throat pain", "scratchy throat"],
    "nausea": ["nausea", "vomiting", "queasy"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool"],
    "dizziness": ["dizzy", "dizziness", "lightheaded"],
}


@dataclass
class ExtractionResult:
    tags: list[str]
    source: str


class SymptomExtractor:
    def __init__(self) -> None:
        self.labels = list(SYMPTOM_KEYWORDS.keys())
        corpus = [" ".join(SYMPTOM_KEYWORDS[label]) for label in self.labels]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        self.label_vectors = self.vectorizer.fit_transform(corpus)
        self._bert_encoder = self._load_distilbert_encoder()

    def _load_distilbert_encoder(self):
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer

            if not torch.cuda.is_available():
                logger.info("GPU unavailable. DistilBERT extractor disabled.")
                return None

            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            model = AutoModel.from_pretrained("distilbert-base-uncased")
            model.eval()
            return {"torch": torch, "tokenizer": tokenizer, "model": model}
        except Exception as exc:  # noqa: BLE001
            logger.warning("DistilBERT symptom extractor unavailable: %s", exc)
            return None

    def _keyword_extract(self, text: str) -> set[str]:
        lowered = text.lower()
        found = set()
        for tag, phrases in SYMPTOM_KEYWORDS.items():
            if any(re.search(rf"\b{re.escape(p)}\b", lowered) for p in phrases):
                found.add(tag)
        return found

    def _tfidf_extract(self, text: str) -> set[str]:
        vec = self.vectorizer.transform([text.lower()])
        scores = (self.label_vectors @ vec.T).toarray().ravel()
        return {self.labels[idx] for idx, score in enumerate(scores) if score >= 0.12}

    def _bert_extract(self, text: str) -> set[str]:
        if not self._bert_encoder:
            return set()

        encoder = self._bert_encoder
        torch = encoder["torch"]
        tokenizer = encoder["tokenizer"]
        model = encoder["model"]

        with torch.no_grad():
            text_tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            text_emb = model(**text_tokens).last_hidden_state.mean(dim=1)

            label_texts = [" ".join(SYMPTOM_KEYWORDS[label]) for label in self.labels]
            label_tokens = tokenizer(label_texts, return_tensors="pt", truncation=True, padding=True)
            label_emb = model(**label_tokens).last_hidden_state.mean(dim=1)

            similarities = torch.nn.functional.cosine_similarity(text_emb, label_emb)
            values = similarities.detach().cpu().numpy()

        return {self.labels[i] for i, v in enumerate(values) if float(v) > 0.55}

    def extract(self, text: str) -> ExtractionResult:
        keyword_tags = self._keyword_extract(text)
        tfidf_tags = self._tfidf_extract(text)
        bert_tags = self._bert_extract(text)

        tags = sorted(keyword_tags | tfidf_tags | bert_tags)
        if not tags:
            tags = ["general_malaise"]
        source = "distilbert+tfidf+keywords" if bert_tags else "tfidf+keywords"
        return ExtractionResult(tags=tags, source=source)


symptom_extractor = SymptomExtractor()
