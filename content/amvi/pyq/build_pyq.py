#!/usr/bin/env python3
"""Build the AMVI past-question (PYQ) cards from the YAML files in papers/.

Usage:
    python pyq/build_pyq.py                 # all papers -> dist/amvi-pyq-pack.json + dist/pyq-review.csv
    python pyq/build_pyq.py papers/x.yaml   # only the given files

One paper file = one Kerala PSC question paper. Each kept question becomes:
  * a fact card  "pyq.<paper>.q<N>"  — the fact the question tests, in simple words,
    with the PSC question as the recall question and the exam/category/year tag;
  * an MCQ test item with the real four options, covering that card.

Questions outside the current AMVI syllabus are listed under `skipped:` with a reason
and are not turned into cards.
"""
import csv
import glob
import json
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
AMVI = os.path.dirname(HERE)
sys.path.insert(0, AMVI)
from build import COURSE, LANG, t  # noqa: E402

LETTERS = "ABCD"


def paper_tag(p):
    cat = f", Cat. No. {p['cat']}" if p.get("cat") else ""
    return f"Kerala PSC {p['exam']}{cat} — {p['date'][:4]} (Q.P. {p['code']}, {p['date']})"


def load_topics():
    with open(os.path.join(HERE, "topics.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)["topics"]


def build(files):
    topics = load_topics()
    topic_ids = {tp["id"] for tp in topics}
    cards, questions, skipped = [], [], []
    for path in files:
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        p = doc["paper"]
        tag = paper_tag(p)
        for q in doc.get("questions", []):
            n = q["n"]
            if q["topic"] not in topic_ids:
                raise SystemExit(f"{path} Q{n}: unknown topic {q['topic']}")
            ans = LETTERS.index(q["key"])
            cid = f"pyq.{p['id']}.q{n}"
            src = f"{tag}, Q{n}; key from {p.get('key_source', 'PSC answer key')}"
            card = {
                "id": cid,
                "topic": q["topic"],
                "type": "fact",
                "difficulty": q.get("difficulty", 2),
                "source": src,
                "status": q.get("status", "needs_review"),
                "learn": t(q["learn"]),
                "why": t(q["why"]),
                "example": t(f"Asked in: {tag}, Q{n}."),
                "recall_q": t(q["q"]),
                "recall_a": t(q["options"][ans] if "a" not in q else q["a"]),
                "explain_simple": t(q.get("simple", q["learn"])),
                "pyq": {"exam": p["exam"], "category": p.get("cat", ""), "qp_code": p["code"],
                        "date": p["date"], "year": int(p["date"][:4]), "q_no": n},
            }
            if "note" in q:
                card["review_note"] = q["note"]
            cards.append(card)
            questions.append({
                "id": f"q.{cid}",
                "topic": q["topic"],
                "kind": "mcq",
                "q": t(q["q"]),
                "options": [t(o) for o in q["options"]],
                "answer": ans,
                "explain": t(q["why"]),
                "source": src,
                "covers": [cid],
            })
        for s in doc.get("skipped", []):
            skipped.append((p["id"], s))
    used = {c["topic"] for c in cards}
    tps = [{"id": tp["id"], "subject": tp["subject"], "title": t(tp["title"]), "order": i + 1,
            "freq": 0.5} for i, tp in enumerate(topics) if tp["id"] in used]
    # Topic frequency from past papers: newer papers weigh more.
    w = {}
    for c in cards:
        w[c["topic"]] = w.get(c["topic"], 0) + 1 + 0.15 * (c["pyq"]["year"] - 2019)
    top = max(w.values() or [1])
    for tp in tps:
        tp["freq"] = round(w.get(tp["id"], 0) / top, 2)
    course = dict(COURSE, id="amvi", title={LANG: "AMVI Exam Prep — PSC previous questions"})
    return {"schema_version": "1.0", "course": course, "topics": tps, "cards": cards,
            "questions": questions}, skipped


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "papers", "*.yaml")))
    pack, skipped = build(files)
    dist = os.path.join(AMVI, "dist")
    os.makedirs(dist, exist_ok=True)
    out = os.path.join(dist, "amvi-pyq-pack.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, indent=1)
    with open(os.path.join(dist, "pyq-review.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "topic", "exam", "category", "qp_code", "date", "q_no", "question",
                     "answer", "card text", "status"])
        for c in pack["cards"]:
            y = c["pyq"]
            wr.writerow([c["id"], c["topic"], y["exam"], y["category"], y["qp_code"], y["date"],
                         y["q_no"], c["recall_q"][LANG], c["recall_a"][LANG], c["learn"][LANG],
                         c["status"]])
    print(f"cards {len(pack['cards'])}, skipped (outside syllabus / cancelled) {len(skipped)}")
    r = subprocess.run([sys.executable, os.path.join(AMVI, "tools", "validate_pack.py"), out])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
