#!/usr/bin/env python3
"""Build the AMVI flashcard pack from the YAML unit files.

Usage:
    python build.py            # build dist/amvi-pack.json + dist/review.csv, then validate
    python build.py units/u1_fluid.yaml   # build and validate only the given files

Each unit file has `topics:` and `cards:` (and optional `mcq:`). Plain strings
are wrapped into {"en": "..."} text objects. Card ids are written short in YAML
and become "<topic>.<id>" in the pack.
"""
import csv
import glob
import json
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = "en"
SYLLABUS = "Kerala PSC AMVI syllabus, Cat. No. 517/2022"

COURSE = {
    "id": "amvi",
    "title": {"en": "AMVI Exam Prep — Assistant Motor Vehicle Inspector"},
    "audience": "adult",
    "languages": [LANG],
    "exam": {
        "name": "Kerala PSC Assistant Motor Vehicle Inspector (next notification)",
        "date": "2027-06-30",
        "status": "estimated",
        "source": "https://www.keralapsc.gov.in",
    },
}

FACT_KEYS = {"learn": "learn", "why": "why", "example": "example", "q": "recall_q",
             "a": "recall_a", "simple": "explain_simple"}


def t(s):
    return {LANG: str(s).strip()}


def build_card(c, topic_titles):
    topic = c["topic"]
    kind = c.get("type", "fact")
    out = {
        "id": f"{topic}.{c['id']}",
        "topic": topic,
        "type": kind,
        "difficulty": c.get("difficulty", 2),
        "source": c.get("source", f"{SYLLABUS} — {topic_titles[topic]}; standard diploma textbook"),
        "status": c.get("status", "needs_review"),
    }
    if "review_note" in c:
        out["review_note"] = c["review_note"]
    if kind == "fact":
        for k, dest in FACT_KEYS.items():
            if k in c:
                out[dest] = t(c[k])
    elif kind == "summary":
        out["title"] = t(c.get("title", topic_titles[topic]))
        out["points"] = [t(p) for p in c["points"]]
    elif kind == "steps":
        out["title"] = t(c["title"])
        out["steps"] = [{"text": t(s["text"]), **({"explain": t(s["explain"])} if "explain" in s else {})}
                        for s in c["steps"]]
        out["summary"] = [t(p) for p in c["summary"]]
        out["recall_q"] = t(c["q"])
        out["recall_a"] = t(c["a"])
    else:
        raise SystemExit(f"card {out['id']}: type {kind} not supported by build.py yet")
    return out


def build(files):
    topics, cards, questions = [], [], []
    order = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            unit = yaml.safe_load(f)
        titles = {}
        for tp in unit["topics"]:
            order += 1
            titles[tp["id"]] = tp["title"]
            topics.append({"id": tp["id"], "subject": unit["subject"], "title": t(tp["title"]),
                           "order": order, "freq": tp.get("freq", 0.5)})
        for c in unit.get("cards", []):
            cards.append(build_card(c, titles))
        for i, q in enumerate(unit.get("mcq", []), 1):
            questions.append({
                "id": f"q.practice.{unit['unit']}.{i}",
                "topic": q["topic"],
                "kind": "mcq",
                "q": t(q["q"]),
                "options": [t(o) for o in q["options"]],
                "answer": q["answer"],
                "explain": t(q["explain"]),
                "source": "Practice — exam pattern (not from a past paper)",
                "covers": [f"{q['topic']}.{x}" if not x.startswith(q["topic"]) else x for x in q["covers"]],
            })
    return {"schema_version": "1.0", "course": COURSE, "topics": topics, "cards": cards,
            "questions": questions}


def review_sheet(pack, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "topic", "type", "key text", "recall answer", "source", "status"])
        for c in pack["cards"]:
            key = (c.get("learn") or c.get("title") or {}).get(LANG, "")
            w.writerow([c["id"], c["topic"], c["type"], key, c.get("recall_a", {}).get(LANG, ""),
                        c["source"], c["status"]])


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "units", "*.yaml")))
    pack = build(files)
    os.makedirs(os.path.join(HERE, "dist"), exist_ok=True)
    out = os.path.join(HERE, "dist", "amvi-pack.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=1)
    review_sheet(pack, os.path.join(HERE, "dist", "review.csv"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "tools", "validate_pack.py"), out])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
