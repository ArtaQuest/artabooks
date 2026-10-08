# artabooks

Every notebook published on [artaquest.com](https://artaquest.com), mirrored verbatim to a public
address so it opens **without any sign-in or permission prompt**:

| Where | How |
|-------|-----|
| Colab | `https://colab.research.google.com/github/ArtaQuest/artabooks/blob/main/nb/<id>/<name>.ipynb` |
| Kaggle | the original kernel's *Copy & Edit*, or `https://www.kaggle.com/kernels/welcome?src=<raw URL of the file>` |
| In the browser | the post's own *Run here* button (Pyodide, on your device) |

`index.json` lists every work with its post, Colab and Kaggle links. The files come verbatim from
the site's public API via `tools/sync.py` (standard library only: `python3 tools/sync.py`); they are
never edited by hand, and a file is never deleted (an old link keeps working after a title change).

**Automatic sync.** `.github/workflows/sync.yml` runs `tools/sync.py` every 15 minutes (and on
demand), committing only when a published notebook was added or changed. It uses the job's own
`GITHUB_TOKEN`; no secret is involved.

Each notebook belongs to its author and carries the licence stated on its ArtaQuest page.
