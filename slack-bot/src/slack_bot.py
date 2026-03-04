"""
Slack Bot v6 - LIMPO, SEM ICONES, COM TRADUCAO
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from .response_agent import get_agent

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
pending = {}
MY_USER_ID = os.getenv("MY_SLACK_USER_ID")


def is_english(text):
    markers = [
        "the ",
        " is ",
        " are ",
        " have ",
        " has ",
        " been ",
        " will ",
        " would ",
        " this ",
        " that ",
        " with ",
        " from ",
        " they ",
        " what ",
        " when ",
        " how ",
        " does ",
        " did ",
        " don't ",
        " doesn't ",
        " i ",
        " you ",
        " we ",
        " my ",
    ]
    t = " " + text.lower() + " "
    return sum(1 for m in markers if m in t) >= 2


@app.event("message")
def handle_message(event, say, client):
    if event.get("bot_id") or event.get("subtype"):
        return

    text = event.get("text", "").strip()
    channel = event.get("channel")
    channel_type = event.get("channel_type", "")

    if not text:
        return

    # DM pro bot
    if channel_type == "im":
        handle_dm(text, say, client)
        return

    # Mencao ao Thiago em canal
    if MY_USER_ID and f"<@{MY_USER_ID}>" in text:
        handle_mention(event, text, channel, client)


def handle_dm(text, say, client):
    t = text.lower().strip()

    if t.startswith("aprovar "):
        do_approve(text, say, client)
    elif t.startswith("editar "):
        do_edit(text, say, client)
    elif t.startswith("ignorar "):
        rid = text.split(maxsplit=1)[1].strip() if len(text.split()) > 1 else ""
        if rid in pending:
            pending.pop(rid)
            say("ignorado")
        else:
            say("id nao encontrado")
    elif t in ["status", "pendentes"]:
        if pending:
            say("\n".join([f"{k}: {v['q'][:40]}" for k, v in pending.items()]))
        else:
            say("nada pendente")
    elif t in ["help", "ajuda", "?"]:
        say("comandos: aprovar, editar, ignorar, status")
    else:
        # Texto livre - verifica se é ingles
        if is_english(text):
            do_translate(text, say)
        else:
            do_question(text, say)


def do_translate(text, say):
    say("traduzindo...")
    agent = get_agent()
    traducao = agent.translate(text)
    if traducao:
        say(f"TRADUCAO:\n\n{traducao}")
    else:
        say("nao consegui traduzir")


def do_question(text, say):
    say("buscando...")
    agent = get_agent()

    # Detecta o assunto
    topic = agent.detect_topic(text)

    # So busca docs QBO se for sobre QBO
    docs = agent.search_docs(text) if topic == "qbo" else ""

    # Busca na web sobre o tema certo
    web = agent.search_web(text, topic if topic != "general" else None)

    resp = agent.answer(text, docs, web, topic)
    expl = agent.explain_pt(topic, docs, web)
    say(f"{resp}\n\n({expl})")


def handle_mention(event, text, channel, client):
    ts = event.get("thread_ts") or event.get("ts")
    user = event.get("user")
    question = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

    if not question:
        return

    try:
        # Info do canal e usuario
        try:
            ch_info = client.conversations_info(channel=channel)
            ch_name = ch_info.get("channel", {}).get("name", "canal")
        except Exception:
            ch_name = "canal"

        try:
            u_info = client.users_info(user=user)
            who = u_info.get("user", {}).get("real_name", "alguem")
        except Exception:
            who = "alguem"

        # Processa
        agent = get_agent()
        topic = agent.detect_topic(question)
        docs = agent.search_docs(question) if topic == "qbo" else ""
        web = agent.search_web(question, topic if topic != "general" else None)
        resp = agent.answer(question, docs, web, topic)
        expl = agent.explain_pt(topic, docs, web)

        rid = f"{channel}_{ts}"[:30]
        pending[rid] = {"ch": channel, "ts": ts, "resp": resp, "q": question[:80]}

        # Manda DM pro Thiago
        dm = client.conversations_open(users=[MY_USER_ID])
        dm_ch = dm["channel"]["id"]

        msg = f"""{who} te marcou em #{ch_name}:

"{question[:300]}"

RESPOSTA SUGERIDA:
{resp}

({expl})

Comandos:
aprovar {rid}
editar {rid} sua versao
ignorar {rid}"""

        client.chat_postMessage(channel=dm_ch, text=msg)

    except Exception as e:
        print(f"Erro: {e}")


def do_approve(text, say, client):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        say("uso: aprovar id")
        return
    rid = parts[1].strip()
    if rid not in pending:
        say("id nao encontrado")
        return
    p = pending.pop(rid)
    client.chat_postMessage(channel=p["ch"], thread_ts=p["ts"], text=p["resp"])
    say("postado!")


def do_edit(text, say, client):
    m = re.match(r"editar\s+(\S+)\s+(.+)", text, re.I | re.DOTALL)
    if not m:
        say("uso: editar id texto")
        return
    rid, novo = m.group(1).strip(), m.group(2).strip()
    if rid not in pending:
        say("id nao encontrado")
        return
    p = pending.pop(rid)
    client.chat_postMessage(channel=p["ch"], thread_ts=p["ts"], text=novo)
    say("postado!")


def start_bot():
    print(f"Bot v6 iniciando - monitorando @{MY_USER_ID}")
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    start_bot()
