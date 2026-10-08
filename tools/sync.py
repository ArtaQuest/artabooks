#!/usr/bin/env python3
"""Mirror every PUBLISHED ArtaQuest notebook into this public repository.

Why this exists: Colab opens a notebook from Drive, GitHub, a gist or an upload. Its /gist/ route
asks the visitor to authorise GitHub (scope repo,gist) before it will show anything, so the old
gist links put an OAuth prompt in front of every reader. Its /github/ route opens a PUBLIC
repository's notebook with no prompt at all. Kaggle's import form (kernels/welcome?src=) also
reads a plain public URL. This repository is that public address, and nothing more.

The bytes are the site's own: GET /wp-json/aq/v1/notebooks/<id>/ipynb, written verbatim to
nb/<id>/<name>.ipynb, where <name> is the slug folded to [a-z0-9-] - the SAME fold the site uses
for its download filename (artaquest-web/src/lib/pykernel.ts ipynbHref), so the site can compute
this path without asking. Files are never deleted here: a title edit moves the canonical path,
and the old path keeps resolving for anyone who saved the link.

Standard library only; run by .github/workflows/sync.yml.
"""
import json, os, re, sys, time, urllib.request

SITE = os.environ.get("AQ_SITE", "https://artaquest.com").rstrip("/")
UA = {"User-Agent": "ArtaQuest-artabooks-sync", "Accept": "application/json"}


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - retried, then raised
            if i == tries - 1:
                raise
            print(f"retry {url}: {e}", file=sys.stderr)
            time.sleep(3 * (i + 1))


def fold(slug):
    s = re.sub(r"[^a-z0-9-]+", "-", (slug or "notebook").lower()).strip("-")[:60]
    return s or "notebook"


def published():
    items, cursor = [], 0
    while True:
        url = f"{SITE}/wp-json/aq/v1/notebooks" + (f"?cursor={cursor}" if cursor else "")
        d = json.loads(get(url))
        items += d.get("items") or []
        cursor = d.get("next")
        if not cursor:
            return items


def main():
    index, changed = [], 0
    for it in published():
        nid, name = int(it["id"]), fold(it.get("slug", ""))
        raw = get(f"{SITE}/wp-json/aq/v1/notebooks/{nid}/ipynb")
        nb = json.loads(raw)  # refuse to mirror anything that is not a notebook
        if not isinstance(nb, dict) or "cells" not in nb:
            print(f"#{nid}: not a notebook, skipped", file=sys.stderr)
            continue
        path = f"nb/{nid}/{name}.ipynb"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        old = open(path, "rb").read() if os.path.exists(path) else None
        if old != raw:
            with open(path, "wb") as fh:
                fh.write(raw)
            changed += 1
            print(f"#{nid}: {'updated' if old is not None else 'added'} {path}")
        index.append({"id": nid, "title": it.get("title", ""), "path": path,
                      "page": f"{SITE}/nb/{nid}/",
                      "colab": f"https://colab.research.google.com/github/ArtaQuest/artabooks/blob/main/{path}",
                      "kaggle": (it.get("kaggle") or {}).get("url") or it.get("kaggle_url") or ""})
    index.sort(key=lambda r: r["id"])
    body = json.dumps(index, indent=1, ensure_ascii=False) + "\n"
    old = open("index.json", encoding="utf-8").read() if os.path.exists("index.json") else ""
    if old != body:
        open("index.json", "w", encoding="utf-8").write(body)
    print(f"{len(index)} published, {changed} file(s) changed")


if __name__ == "__main__":
    main()
