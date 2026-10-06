#!/usr/bin/env python3
"""Literature search from the command line: OpenAlex + Semantic Scholar.

Standard library only. Run `python3 lit.py <command> --help` for options.

Commands
  search   QUERY      papers on a topic (both sources, merged and deduplicated)
  core     QUERY      the papers a topic's literature cites most ("everyone cites")
  similar  ID         nearest neighbours of a paper ("has someone done this?")
  citing   ID         newer papers that cite a paper
  paper    ID         full record of one paper, including the abstract
  verify   TEXT       check that a reference exists (title or full citation, or a DOI)

ID can be a DOI (10.xxxx/..., or a doi.org URL), an OpenAlex work ID (W123...),
or a Semantic Scholar paper ID.

Optional environment variables
  OPENALEX_API_KEY   free key, raises the OpenAlex daily budget
  S2_API_KEY         Semantic Scholar key, avoids the shared rate limit
"""

import argparse
import datetime as dt
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OA = "https://api.openalex.org"
S2 = "https://api.semanticscholar.org"
UA = "literature-search-skill/1.0 (python urllib)"
S2_FIELDS = "title,year,venue,citationCount,externalIds,authors,abstract,url,openAccessPdf"


# ---------------------------------------------------------------- http

def get(url, params=None, headers=None, tries=6):
    """GET JSON with retries on 429 and 5xx (exponential backoff)."""
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    hdr = {"User-Agent": UA, "Accept": "application/json"}
    hdr.update(headers or {})
    wait = 1.5
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(wait)
                wait *= 2
                continue
            raise RuntimeError(f"HTTP {e.code} for {url.split('?')[0]}") from None
        except urllib.error.URLError as e:
            if attempt < tries - 1:
                time.sleep(wait)
                wait *= 2
                continue
            raise RuntimeError(f"network error: {e.reason}") from None


def clean_q(q):
    """OpenAlex filter values break on punctuation such as ',', '?', ':' or quotes."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s\-]", " ", q)).strip()


def oa(path, **params):
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key
    return get(OA + path, params)


def s2(path, **params):
    key = os.environ.get("S2_API_KEY")
    return get(S2 + path, params, {"x-api-key": key} if key else None)


# ---------------------------------------------------------------- ids

def norm_doi(x):
    if not x:
        return None
    x = x.strip()
    x = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", x, flags=re.I)
    x = re.sub(r"^doi:", "", x, flags=re.I)
    return x.lower() if x.startswith("10.") else None


def classify(pid):
    """Return ('doi'|'openalex'|'s2', value)."""
    d = norm_doi(pid)
    if d:
        return "doi", d
    m = re.search(r"(W\d+)$", pid.strip(), flags=re.I)
    if m:
        return "openalex", m.group(1).upper()
    return "s2", pid.strip()


def oa_work(pid):
    kind, v = classify(pid)
    if kind == "doi":
        return oa(f"/works/doi:{v}")
    if kind == "openalex":
        return oa(f"/works/{v}")
    p = s2(f"/graph/v1/paper/{v}", fields="externalIds")
    d = (p or {}).get("externalIds", {}).get("DOI")
    return oa(f"/works/doi:{d.lower()}") if d else None


def s2_id(pid):
    kind, v = classify(pid)
    if kind == "doi":
        return f"DOI:{v}"
    if kind == "openalex":
        w = oa(f"/works/{v}")
        d = norm_doi((w or {}).get("doi"))
        if not d:
            raise RuntimeError(f"{v} has no DOI, so it cannot be looked up in Semantic Scholar")
        return f"DOI:{d}"
    return v


# ---------------------------------------------------------------- records

def abstract_from_index(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def biblio_str(b):
    if not b:
        return ""
    out = b.get("volume") or ""
    if b.get("issue"):
        out += f"({b['issue']})"
    if b.get("first_page"):
        out += (":" if out else "pp. ") + b["first_page"] + (f"-{b['last_page']}" if b.get("last_page") and b["last_page"] != b["first_page"] else "")
    return out


def rec_oa(w):
    authors = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
    loc = (w.get("primary_location") or {}).get("source") or {}
    oa_info = w.get("open_access") or {}
    return {
        "title": w.get("display_name") or w.get("title") or "",
        "year": w.get("publication_year"),
        "authors": authors,
        "venue": loc.get("display_name") or "",
        "cited_by": w.get("cited_by_count"),
        "doi": norm_doi(w.get("doi")),
        "openalex": (w.get("id") or "").rsplit("/", 1)[-1] or None,
        "type": w.get("type"),
        "oa_url": oa_info.get("oa_url"),
        "biblio": biblio_str(w.get("biblio")),
        "abstract": abstract_from_index(w.get("abstract_inverted_index")),
        "found_in": ["openalex"],
    }


def rec_s2(p):
    ext = p.get("externalIds") or {}
    pdf = p.get("openAccessPdf") or {}
    return {
        "title": p.get("title") or "",
        "year": p.get("year"),
        "authors": [a.get("name", "") for a in p.get("authors") or []],
        "venue": p.get("venue") or "",
        "cited_by": p.get("citationCount"),
        "doi": norm_doi(ext.get("DOI")),
        "s2": p.get("paperId"),
        "oa_url": pdf.get("url") or None,
        "abstract": p.get("abstract") or "",
        "found_in": ["semantic_scholar"],
    }


def tkey(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:80]


def merge(lists):
    """Merge records from several sources; dedupe on DOI, then on title."""
    out, by = [], {}
    for lst in lists:
        for r in lst:
            k = ("doi", r["doi"]) if r.get("doi") else ("t", tkey(r["title"]))
            alt = ("t", tkey(r["title"]))
            hit = by.get(k) or by.get(alt)
            if hit:
                for f, v in r.items():
                    if f == "found_in":
                        hit["found_in"] = sorted(set(hit["found_in"]) | set(v))
                    elif not hit.get(f) and v:
                        hit[f] = v
                if (r.get("cited_by") or 0) > (hit.get("cited_by") or 0):
                    hit["cited_by"] = r["cited_by"]
            else:
                out.append(r)
                by[k] = r
                by[alt] = r
    return out


# ---------------------------------------------------------------- output

def short_authors(a):
    if not a:
        return ""
    return a[0].split()[-1] + (" et al." if len(a) > 2 else (f" & {a[1].split()[-1]}" if len(a) == 2 else ""))


def link(r):
    if r.get("doi"):
        return f"https://doi.org/{r['doi']}"
    if r.get("openalex"):
        return f"https://openalex.org/{r['openalex']}"
    if r.get("s2"):
        return f"https://www.semanticscholar.org/paper/{r['s2']}"
    return ""


def emit(args, title, recs, meta=None, extra_cols=None):
    stamp = dt.date.today().isoformat()
    if args.json:
        print(json.dumps({"query": title, "retrieved": stamp, "meta": meta or {}, "results": recs},
                         ensure_ascii=False, indent=1))
        return
    print(f"## {title}")
    info = f"Retrieved {stamp}"
    if meta:
        info += " · " + " · ".join(f"{k}: {v}" for k, v in meta.items())
    print(info + "\n")
    if not recs:
        print("No results.")
        return
    cols = ["#", "Year", "Authors", "Title", "Venue", "Cited by"] + [c for c, _ in (extra_cols or [])] + ["Link"]
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for i, r in enumerate(recs, 1):
        title_txt = (r["title"] or "").replace("|", "/")
        row = [str(i), str(r.get("year") or ""), short_authors(r.get("authors")),
               title_txt[:120], (r.get("venue") or "")[:40].replace("|", "/"),
               str(r.get("cited_by") if r.get("cited_by") is not None else "")]
        row += [str(fn(r)) for _, fn in (extra_cols or [])]
        row.append(link(r))
        print("| " + " | ".join(row) + " |")
    if args.abstracts:
        print()
        for i, r in enumerate(recs, 1):
            if r.get("abstract"):
                print(f"**[{i}] {r['title']}**  \n{r['abstract'][:1200]}\n")


# ---------------------------------------------------------------- commands

OA_SORT = {"relevance": "relevance_score:desc", "cited": "cited_by_count:desc", "recent": "publication_date:desc"}


def oa_filters(args, base):
    f = [base]
    if args.since:
        f.append(f"from_publication_date:{args.since}-01-01")
    if args.until:
        f.append(f"to_publication_date:{args.until}-12-31")
    if getattr(args, "oa_only", False):
        f.append("is_oa:true")
    return ",".join(f)


def search_oa(args, n):
    q = clean_q(args.query)
    r = oa("/works", filter=oa_filters(args, f"title_and_abstract.search:{q}"),
           sort=OA_SORT[args.sort], per_page=min(n, 100))
    return [rec_oa(w) for w in r["results"]], r["meta"]["count"]


def search_s2(args, n):
    params = {"query": args.query, "limit": min(n, 100), "fields": S2_FIELDS}
    if args.since or args.until:
        params["year"] = f"{args.since or ''}-{args.until or ''}"
    if getattr(args, "oa_only", False):
        params["openAccessPdf"] = ""
    r = s2("/graph/v1/paper/search", **params)
    recs = [rec_s2(p) for p in r.get("data", [])]
    if args.sort == "cited":
        recs.sort(key=lambda x: -(x["cited_by"] or 0))
    elif args.sort == "recent":
        recs.sort(key=lambda x: -(x["year"] or 0))
    return recs, r.get("total")


def cmd_search(args):
    lists, meta, notes = [], {}, []
    if args.source in ("both", "openalex"):
        recs, total = search_oa(args, args.n)
        lists.append(recs)
        meta["OpenAlex hits"] = f"{total:,}"
    if args.source in ("both", "s2"):
        try:
            recs, total = search_s2(args, args.n)
            lists.append(recs)
            meta["Semantic Scholar hits"] = f"{total:,}" if total is not None else "?"
        except RuntimeError as e:
            notes.append(f"Semantic Scholar skipped ({e}); set S2_API_KEY or retry later")
    recs = merge(lists)
    if args.sort == "cited":
        recs.sort(key=lambda x: -(x.get("cited_by") or 0))
    elif args.sort == "recent":
        recs.sort(key=lambda x: -(x.get("year") or 0))
    meta["sort"] = args.sort
    emit(args, f"Search: {args.query}", recs[: args.n], meta,
         [("Found in", lambda r: "+".join("OA" if s == "openalex" else "S2" for s in r["found_in"]))])
    for n in notes:
        print(f"\nNote: {n}", file=sys.stderr)


def cmd_core(args):
    """Most-referenced works among the top `pool` papers on a topic."""
    q = clean_q(args.query)
    counts, pool_n, page = {}, 0, 1
    while pool_n < args.pool:
        r = oa("/works", filter=oa_filters(args, f"title_and_abstract.search:{q}"),
               sort="relevance_score:desc", per_page=min(100, args.pool - pool_n), page=page,
               select="id,referenced_works")
        if not r["results"]:
            break
        for w in r["results"]:
            for ref in w.get("referenced_works") or []:
                k = ref.rsplit("/", 1)[-1]
                counts[k] = counts.get(k, 0) + 1
        pool_n += len(r["results"])
        page += 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[: args.n]
    recs = []
    if top:
        ids = "|".join(k for k, _ in top)
        r = oa("/works", filter=f"openalex:{ids}", per_page=len(top))
        by = {rec_oa(w)["openalex"]: rec_oa(w) for w in r["results"]}
        for k, c in top:
            if k in by:
                by[k]["cited_in_pool"] = c
                recs.append(by[k])
    emit(args, f"Most-cited by the literature on: {args.query}", recs,
         {"pool": f"top {pool_n} OpenAlex results", "source": "OpenAlex references"},
         [(f"Cited by pool (of {pool_n})", lambda r: r.get("cited_in_pool", ""))])


def coupled(w, n, max_candidates=500):
    """Bibliographic coupling: works that share the most *specific* references with `w`.

    Each shared reference is weighted by 1/log(citations): sharing a niche trial
    counts far more than sharing a famous methods paper that everyone cites.
    """
    import math
    refs = [x.rsplit("/", 1)[-1] for x in w.get("referenced_works") or []]
    if len(refs) < 3:
        return []
    cites = {}
    for k in range(0, len(refs), 50):
        r = oa("/works", filter="openalex:" + "|".join(refs[k:k + 50]), select="id,cited_by_count", per_page=50)
        for x in r["results"]:
            cites[x["id"].rsplit("/", 1)[-1]] = x.get("cited_by_count") or 0
    weight = {k: 1 / math.log(3 + cites.get(k, 0)) for k in refs}
    specific = sorted(refs, key=lambda k: cites.get(k, 0))[:40]
    seed = w["id"].rsplit("/", 1)[-1]
    refset, score, shared, page = set(refs), {}, {}, 1
    while (page - 1) * 100 < max_candidates:
        r = oa("/works", filter="cites:" + "|".join(specific), select="id,referenced_works",
               sort="publication_date:desc", per_page=100, page=page)
        if not r["results"]:
            break
        for c in r["results"]:
            cid = c["id"].rsplit("/", 1)[-1]
            common = refset & {x.rsplit("/", 1)[-1] for x in c.get("referenced_works") or []}
            if cid != seed and len(common) >= 2:
                score[cid] = sum(weight[k] for k in common)
                shared[cid] = len(common)
        page += 1
    top = sorted(score, key=lambda k: -score[k])[:n]
    if not top:
        return []
    r = oa("/works", filter="openalex:" + "|".join(top), per_page=len(top))
    by = {rec_oa(x)["openalex"]: rec_oa(x) for x in r["results"]}
    out = []
    for k in top:
        if k in by:
            by[k]["shared_refs"] = f"{shared[k]} of {len(refs)}"
            out.append(by[k])
    return out


def cmd_similar(args):
    """Two complementary neighbour lists: OpenAlex bibliographic coupling (shared
    references, any year) and Semantic Scholar recommendations (embeddings, recent papers)."""
    w = oa_work(args.id)
    oa_recs, s2_recs, notes = [], [], []
    if w:
        oa_recs = coupled(w, args.n)
        if not oa_recs:
            notes.append("seed paper has too few references in OpenAlex for shared-reference matching")
    try:
        sid = s2_id(args.id)
        r = s2(f"/recommendations/v1/papers/forpaper/{urllib.parse.quote(sid, safe=':')}",
               limit=args.n, fields=S2_FIELDS)
        s2_recs = [rec_s2(p) for p in (r or {}).get("recommendedPapers", [])]
    except RuntimeError as e:
        notes.append(f"Semantic Scholar recommendations skipped ({e})")
    if not (w or s2_recs):
        sys.exit(f"Paper not found: {args.id}")
    for r in oa_recs:
        r["via"] = "shared refs " + r["shared_refs"]
    for r in s2_recs:
        r["via"] = "S2 recommended"
    recs = merge([oa_recs, s2_recs])
    seed = rec_oa(w)["title"] if w else args.id
    emit(args, f"Nearest neighbours of: {seed}", recs,
         {"OpenAlex shared-reference matches": len(oa_recs), "Semantic Scholar recommended (recent papers)": len(s2_recs)},
         [("Via", lambda r: r.get("via", "") + (" + S2" if len(r["found_in"]) > 1 else ""))])
    for n in notes:
        print(f"\nNote: {n}", file=sys.stderr)


def cmd_citing(args):
    w = oa_work(args.id)
    if not w:
        sys.exit(f"Paper not found: {args.id}")
    wid = w["id"].rsplit("/", 1)[-1]
    r = oa("/works", filter=oa_filters(args, f"cites:{wid}"), sort=OA_SORT[args.sort], per_page=min(args.n, 100))
    emit(args, f"Papers citing: {w.get('display_name')}", [rec_oa(x) for x in r["results"]],
         {"total citing (OpenAlex)": f"{r['meta']['count']:,}", "sort": args.sort})


def cmd_paper(args):
    w = oa_work(args.id)
    recs = [rec_oa(w)] if w else []
    try:
        p = s2(f"/graph/v1/paper/{urllib.parse.quote(s2_id(args.id), safe=':')}", fields=S2_FIELDS)
        if p:
            recs = merge([recs, [rec_s2(p)]])
    except RuntimeError:
        pass
    if not recs:
        sys.exit(f"Paper not found: {args.id}")
    r = recs[0]
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    print(f"## {r['title']}\n")
    print(f"- **Authors:** {', '.join(r['authors'][:12])}{' …' if len(r['authors']) > 12 else ''}")
    print(f"- **Year / venue:** {r.get('year')} · {r.get('venue')}" + (f" {r['biblio']}" if r.get("biblio") else ""))
    print(f"- **Cited by:** {r.get('cited_by')}  ·  **Type:** {r.get('type') or ''}")
    print(f"- **Link:** {link(r)}" + (f"  ·  **Open access:** {r['oa_url']}" if r.get("oa_url") else ""))
    print(f"- **Found in:** {', '.join(r['found_in'])}")
    print(f"\n**Abstract.** {r.get('abstract') or '(no abstract available)'}")


def title_guesses(text):
    """Plausible titles inside a free-text reference, best first."""
    out = []
    m = re.search(r"[\"“](.+?)[\"”]", text)
    if m:
        out.append(m.group(1))
    # split at '. ' before a capital letter (sentence ends), not at '?' or ':' inside titles
    parts = [p.strip(" .") for p in re.split(r"\.\s+(?=[A-Z])", text)]
    parts = [p for p in parts if len(p) > 15 and not re.match(r"^[A-Z][\w'’\-]+,? [A-Z]{1,3}\b", p)]
    out += sorted(parts, key=len, reverse=True)[:2]
    out.append(text)
    seen, res = set(), []
    for g in out:
        g = re.sub(r"\s+", " ", g).strip(" .")
        if g and g.lower() not in seen:
            seen.add(g.lower())
            res.append(g)
    return res[:3]


def match_score(guesses, title):
    t = tkey(title)
    best = 0.0
    for g in guesses:
        gk = tkey(g)
        best = max(best, difflib.SequenceMatcher(None, gk, t).ratio())
        if t and t in gk:  # whole title appears inside the reference text
            best = max(best, 0.95)
    return round(best, 2)


def detail_checks(text, c):
    """Compare year, first-author surname, and volume/pages stated in the reference."""
    notes = []
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    if years and c.get("year"):
        notes.append("year ✓" if str(c["year"]) in years else f"year ✗ (record: {c['year']})")
    m = re.match(r"\s*([A-Z][\w'’\-]+(?:\s(?:van|de|der|von)\s[A-Z][\w'’\-]+)?)", text)
    if m and c.get("authors"):
        sur = m.group(1).split()[-1].lower()
        notes.append("first author ✓" if sur in (c["authors"][0] or "").lower() else f"first author ✗ (record: {c['authors'][0]})")
    vp = re.search(r"\b(\d{1,4})\s*(?:\((\d{1,4})\))?\s*:\s*(e?\d+)", text)
    if vp and c.get("biblio"):
        ok = vp.group(1) in c["biblio"] and vp.group(3) in c["biblio"]
        notes.append("volume/pages ✓" if ok else f"volume/pages ✗ (record: {c['biblio']})")
    return ", ".join(notes)


def cmd_verify(args):
    text = args.text
    m = re.search(r"10\.\d{4,9}/\S+", text)
    d = norm_doi(text) or (norm_doi(m.group(0).rstrip(".,;)")) if m else None)
    guesses = [] if norm_doi(text) else title_guesses(text)
    cands = []
    if d:
        w = oa(f"/works/doi:{d}")
        if w:
            cands.append(rec_oa(w))
    if not cands or guesses:
        for g in guesses[:2]:
            q = clean_q(g)
            if q:
                r = oa("/works", filter=f"title.search:{q}", per_page=5)
                cands += [rec_oa(w) for w in r["results"]]
            try:
                r = s2("/graph/v1/paper/search/match", query=g, fields=S2_FIELDS)
                cands += [rec_s2(p) for p in (r or {}).get("data", [])]
            except RuntimeError:
                pass
    cands = merge([cands])
    for c in cands:
        c["title_match"] = "DOI" if (d and c.get("doi") == d) else match_score(guesses, c["title"])
    cands.sort(key=lambda c: -(1.0 if c["title_match"] == "DOI" else c["title_match"]))
    best = cands[0] if cands else None
    if best and best["title_match"] == "DOI":
        verdict = "FOUND (DOI resolves)"
    elif best and best["title_match"] >= 0.9:
        verdict = "FOUND (title matches)"
    elif best and best["title_match"] >= 0.7:
        verdict = "UNCERTAIN (similar title: compare the record below with the reference)"
    else:
        verdict = "NOT FOUND (treat as unverified; do not cite without a source)"
    checks = detail_checks(text, best) if best and verdict.startswith("FOUND") and guesses else ""
    if args.json:
        print(json.dumps({"input": text, "title_guesses": guesses, "verdict": verdict, "checks": checks,
                          "candidates": cands[:3]}, ensure_ascii=False, indent=1))
        return
    print(f"## Verify: {text[:150]}\n\n**Verdict: {verdict}**" + (f"  \nDetails: {checks}" if checks else "") + "\n")
    emit(argparse.Namespace(json=False, abstracts=False), "Closest records", cands[:3], None,
         [("Vol/pages", lambda r: r.get("biblio", "")), ("Title match", lambda r: r["title_match"])])


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, years=True):
        p.add_argument("--json", action="store_true", help="machine-readable output")
        p.add_argument("--abstracts", action="store_true", help="print abstracts under the table")
        if years:
            p.add_argument("--since", type=int, help="earliest publication year")
            p.add_argument("--until", type=int, help="latest publication year")

    p = sub.add_parser("search", help="papers on a topic")
    p.add_argument("query")
    p.add_argument("--n", type=int, default=15, help="number of results shown (default 15)")
    p.add_argument("--sort", choices=list(OA_SORT), default="relevance")
    p.add_argument("--source", choices=["both", "openalex", "s2"], default="both")
    p.add_argument("--oa-only", action="store_true", help="open-access papers only")
    common(p)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("core", help="papers the literature on a topic cites most")
    p.add_argument("query")
    p.add_argument("--n", type=int, default=15)
    p.add_argument("--pool", type=int, default=200, help="how many topic papers to scan (default 200)")
    common(p)
    p.set_defaults(fn=cmd_core)

    p = sub.add_parser("similar", help="nearest neighbours of a paper")
    p.add_argument("id")
    p.add_argument("--n", type=int, default=15)
    common(p, years=False)
    p.set_defaults(fn=cmd_similar)

    p = sub.add_parser("citing", help="papers that cite a paper")
    p.add_argument("id")
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--sort", choices=list(OA_SORT), default="cited")
    common(p)
    p.set_defaults(fn=cmd_citing)

    p = sub.add_parser("paper", help="full record of one paper")
    p.add_argument("id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_paper)

    p = sub.add_parser("verify", help="check that a reference exists")
    p.add_argument("text", help="a title, a full reference, or a DOI")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_verify)

    args = ap.parse_args()
    try:
        args.fn(args)
    except RuntimeError as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
