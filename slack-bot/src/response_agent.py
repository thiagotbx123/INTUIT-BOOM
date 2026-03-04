"""
Response Agent v6 - Detecta assunto, busca no tema certo
"""

import requests
from pathlib import Path

KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent.parent / "knowledge-base"
QBO_FILE = KNOWLEDGE_BASE_PATH / "qbo" / "QBO_DEEP_MASTER_v1.txt"
OLLAMA_URL = "http://localhost:11434/api/generate"


class ResponseAgent:
    def __init__(self):
        self.docs = ""
        if QBO_FILE.exists():
            try:
                self.docs = QBO_FILE.read_text(encoding="utf-8", errors="replace").replace("\x00", "")
            except Exception:
                pass

    def search_docs(self, query):
        words = query.lower().split()
        for i in range(0, len(self.docs), 1500):
            chunk = self.docs[i : i + 1500]
            if any(w in chunk.lower() for w in words):
                return chunk[:1000]
        return ""

    def search_web(self, query, topic=None):
        """Busca na web sobre o tema especifico."""
        try:
            from duckduckgo_search import DDGS

            search_query = f"{topic} {query}" if topic else query
            with DDGS() as d:
                r = list(d.text(search_query, max_results=3))
                return " ".join([x.get("body", "") for x in r])[:1000]
        except Exception:
            return ""

    def detect_topic(self, text):
        """Detecta o assunto principal da mensagem."""
        text_lower = text.lower()

        # Palavras-chave por tema
        qbo_words = [
            "quickbooks",
            "qbo",
            "invoice",
            "reconcile",
            "chart of accounts",
            "accounts payable",
            "accounts receivable",
            "journal entry",
        ]
        mailchimp_words = ["mailchimp", "email marketing", "campaign", "newsletter"]
        intuit_words = ["intuit", "wfs", "workforce", "hcm", "payroll"]

        if any(w in text_lower for w in qbo_words):
            return "qbo"
        elif any(w in text_lower for w in mailchimp_words):
            return "mailchimp"
        elif any(w in text_lower for w in intuit_words):
            return "intuit"
        else:
            return "general"

    def translate(self, text):
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": "llama3.2",
                    "prompt": f"Traduza o texto completo abaixo para portugues brasileiro. Traduza TUDO, cada frase. Responda APENAS com a traducao completa:\n\n{text}",
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 2000},
                },
                timeout=60,
            )
            return r.json().get("response", "").strip()
        except Exception:
            return ""

    def answer(self, question, docs, web, topic):
        prompt = f"""Answer this question about {topic}. Be direct and helpful.

Rules:
- Give practical advice or steps
- Simple words, short sentences
- No formatting, no bullets, no markdown
- Max 4-5 sentences

Context from search:
{web[:1500] if web else "No web results."}

{f"Internal docs: {docs[:1000]}" if docs else ""}

Question: {question}

Answer:"""
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 200},
                },
                timeout=45,
            )
            resp = r.json().get("response", "").strip()
            for c in ["**", "*", "#", "-", "`", "•"]:
                resp = resp.replace(c, "")
            return resp
        except Exception:
            return "Could not generate answer."

    def explain_pt(self, topic, docs, web):
        parts = []
        if docs:
            parts.append("docs internos")
        if web:
            parts.append("web")
        sources = " e ".join(parts) if parts else "nenhuma fonte"
        return f"Tema: {topic}. Usei {sources}."


_agent = None


def get_agent():
    global _agent
    if not _agent:
        _agent = ResponseAgent()
    return _agent
