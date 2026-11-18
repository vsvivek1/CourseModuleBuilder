"""Convert the AMVI Recallio packs into a QuizKerala course pack.

    python3 tools/to_quizkerala.py OUT.json

Reads dist/amvi-pack.json (topic cards) and dist/amvi-pyq-pack.json (PSC
previous questions). Each syllabus topic becomes one or more lessons of at most
MAX_CARDS cards: every card is a point, the topic summary is "remember", and the
questions are the practice MCQs plus one recall MCQ per card (its answer
against other answers from the same topic). PSC questions become "exam-"
lessons per unit, which the app puts at the end of each unit.
"""
import json, math, sys, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MAX_CARDS = 15
UNITS = {
    "u1": "Unit I: Fluid mechanics and machinery",
    "u2": "Unit II: Thermal engineering",
    "u3": "Unit III: Strength of materials",
    "u4": "Unit IV: Machine elements",
    "u5": "Module V: Automobile engines",
    "u6": "Module VI: Chassis, brakes, steering, suspension",
    "u7": "Module VII: Transmission and electrical",
    "u8": "Module VIII: Transport management and modern tech",
    "dl": "Driving licence: Regulations 2017, MV Act Ch II",
    "law": "Job related: MV Act 1988 and KMVT Act 1976",
}

def en(x):
    return (x or {}).get("en", "").strip() if isinstance(x, dict) else (x or "").strip()

def clip(s, n):
    s = " ".join(s.split()) if "\n" not in s else s.strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def rng(seed):
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    while True:
        h = (h * 6364136223846793005 + 1442695040888963407) % 2**64
        yield h / 2**64

def shuffle(q, seed):
    r = rng(seed)
    order = list(range(len(q["options"])))
    for i in range(len(order) - 1, 0, -1):
        j = int(next(r) * (i + 1)); order[i], order[j] = order[j], order[i]
    right = q["options"][q["answer"]]
    q["options"] = [q["options"][i] for i in order]
    q["answer"] = q["options"].index(right)
    return q

def point(c):
    if c["type"] == "steps":
        lines = [f"{en(c['title'])}"] + [f"- {en(s['text'])}" + (f" ({en(s['explain'])})" if s.get("explain") else "") for s in c["steps"]]
        return clip("\n".join(lines), 1200)
    s = en(c["learn"])
    if en(c.get("why")): s += f"\n\nWhy: {en(c['why'])}"
    if en(c.get("example")) and not en(c["example"]).startswith("Asked in"): s += f"\n\nExample: {en(c['example'])}"
    return clip(s, 1200)

def mcq(q, src=None):
    out = {"q": clip(en(q["q"]), 500), "options": [clip(en(o), 200) for o in q["options"]], "answer": q["answer"],
           "why": clip(en(q.get("explain")) or "See the lesson.", 500 if not src else 480)}
    if src: out["why"] = clip(out["why"] + f" (Asked in: {src})", 500)
    return out if len(set(out["options"])) == len(out["options"]) else None

def recall_mcq(c, pool):
    a = clip(en(c.get("recall_a")), 200); qtext = en(c.get("recall_q"))
    if not a or not qtext: return None
    r = rng(c["id"])
    others = sorted({clip(x, 200) for x in pool if x and clip(x, 200) != a}, key=lambda x: (abs(len(x) - len(a)), next(r)))
    picks = others[:3]
    if len(picks) < 2: return None
    return {"q": clip(qtext, 500), "options": [a] + picks, "answer": 0, "why": clip(en(c.get("explain_simple")) or a, 500)}

def main(out):
    main_p = json.load(open(HERE / "dist/amvi-pack.json"))
    pyq_p = json.load(open(HERE / "dist/amvi-pyq-pack.json"))
    lessons = []
    for t in main_p["topics"]:
        tid = t["id"]; unit = UNITS[tid.split(".")[0]]
        cards = [c for c in main_p["cards"] if c["topic"] == tid]
        summary = next((c for c in cards if c["type"] == "summary"), None)
        body = [c for c in cards if c["type"] != "summary"]
        pool = [en(c.get("recall_a")) for c in body]
        practice = [q for q in main_p["questions"] if q["topic"] == tid]
        n = max(1, math.ceil(len(body) / MAX_CARDS)); size = math.ceil(len(body) / n)
        for k in range(n):
            part = body[k * size:(k + 1) * size]
            ids = {c["id"] for c in part}
            qs = [mcq(q) for q in practice if (set(q.get("covers", [])) & ids) or (k == 0 and not set(q.get("covers", [])) & {c["id"] for c in body})]
            qs += [recall_mcq(c, pool) for c in part]
            qs = [q for q in qs if q][:30]
            if k == n - 1 and summary:
                remember = [clip(en(p), 300) for p in summary["points"]][:6]
            else:
                remember = [clip(f"{en(c['recall_q'])} {en(c['recall_a'])}", 300) for c in part if en(c.get("recall_q"))][:4]
            title = en(t["title"]) + (f" (part {k + 1} of {n})" if n > 1 else "")
            lessons.append({"slug": f"{tid.replace('.', '-')}-{k + 1}"[:40], "unit": unit, "title": clip(title, 200), "language": "en",
                            "source": "Kerala PSC AMVI syllabus (Cat. No. 517/2022); cards need review",
                            "points": [point(c) for c in part], "remember": remember,
                            "questions": [shuffle(q, f"{tid}|{k}|{q['q']}") for q in qs]})
    # PSC previous questions: exam lessons per unit, 25 questions each.
    byunit = {}
    for c in pyq_p["cards"]:
        byunit.setdefault(c["topic"].split(".")[0], []).append(c)
    qbycard = {q["covers"][0]: q for q in pyq_p["questions"]}
    for u, cards in byunit.items():
        n = math.ceil(len(cards) / 25); size = math.ceil(len(cards) / n)
        for k in range(n):
            part = cards[k * size:(k + 1) * size]
            qs = [mcq(qbycard[c["id"]], en(c.get("example")).replace("Asked in: ", "").rstrip(".")) for c in part if c["id"] in qbycard]
            qs = [shuffle(q, f"pyq|{q['q']}") for q in qs if q]
            lessons.append({"slug": f"exam-{u}-{k + 1}", "unit": UNITS[u], "title": f"PSC previous questions: {UNITS[u].split(': ', 1)[1]} ({k + 1} of {n})",
                            "language": "en", "source": "Kerala PSC question papers and final answer keys (see each answer)",
                            "points": [point(c) for c in part][:30],
                            "remember": [clip(en(c["learn"]), 300) for c in part[:4]], "questions": qs[:30]})
    # Mix units in proportion (exam lessons last in each unit), one lesson a day, revision every 6, 4 model tests.
    order = list(UNITS)
    byu = {}
    for l in [l for l in lessons if not l["slug"].startswith("exam-")] + [l for l in lessons if l["slug"].startswith("exam-")]:
        byu.setdefault(l["unit"], []).append(l)
    mixed = [x[0] for x in sorted(((l, (i + 0.5) / len(ls)) for u in [UNITS[o] for o in order] for ls in [byu.get(u, [])] for i, l in enumerate(ls)), key=lambda x: x[1])]
    days = []
    for i in range(0, len(mixed), 6):
        wk = [l["slug"] for l in mixed[i:i + 6]]
        days += [{"kind": "lesson", "lessons": [s]} for s in wk] + [{"kind": "revision", "lessons": wk}]
    days += [{"kind": "mock", "mock": m} for m in range(1, 5)]
    pack = {"name": "AMVI (Kerala PSC Assistant Motor Vehicle Inspector)", "lessons": mixed, "days": days}
    Path(out).write_text(json.dumps(pack, ensure_ascii=False, indent=1) + "\n")
    bad = [l["slug"] for l in mixed if len(l["questions"]) < 2]
    print(f"{len(mixed)} lessons, {sum(len(l['points']) for l in mixed)} points, {sum(len(l['questions']) for l in mixed)} questions, {len(days)} days; <2 questions: {bad}")

if __name__ == "__main__":
    main(sys.argv[1])
