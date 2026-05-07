# ============================================================
# model.py — Model loading, embeddings, chart helpers
# ============================================================

import torch
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import spacy
from transformers import AutoTokenizer, AutoModel

from config import MODEL_NAME, PURPLE, PINK, GREEN, YELLOW, RED


@st.cache_resource
def load_models():
    """Load spaCy NER model + RoBERTa tokenizer/model (cached across reruns)."""
    nlp       = spacy.load("en_core_web_sm")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model     = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    return nlp, tokenizer, model


def get_embedding(text: str, tokenizer, model, max_length: int = 512) -> np.ndarray:
    """Mean-pooled RoBERTa embedding for a block of text."""
    inputs = tokenizer(text, return_tensors="pt", max_length=max_length,
                       truncation=True, padding="max_length")
    with torch.no_grad():
        outputs = model(**inputs)
    token_emb   = outputs.last_hidden_state
    attn_mask   = inputs["attention_mask"]
    mask_expand = attn_mask.unsqueeze(-1).expand(token_emb.size()).float()
    return (torch.sum(token_emb * mask_expand, 1) /
            torch.clamp(mask_expand.sum(1), min=1e-9)).squeeze().numpy()


def set_dark_chart(fig, ax_list):
    """Apply dark theme styling to matplotlib figures."""
    fig.patch.set_facecolor("#0f0c29")
    for ax in (ax_list if isinstance(ax_list, list) else [ax_list]):
        ax.set_facecolor("#0f0c29")
        ax.tick_params(colors="#555")
        ax.xaxis.label.set_color("#555")
        ax.yaxis.label.set_color("#555")
        ax.title.set_color("#a78bfa")
        for spine in ax.spines.values():
            spine.set_edgecolor("#222")
