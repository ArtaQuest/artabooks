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

**Automatic sync.** `tools/sync.workflow.yml` runs the sync every 15 minutes once it lives at
`.github/workflows/sync.yml`. Moving it there needs a GitHub credential with the `workflow`
scope, so it is staged here until someone with that scope moves it. Until it does, a newly
published work keeps the site's download-and-open Colab fallback (never an OAuth prompt) until the
next manual sync.

Each notebook belongs to its author and carries the licence stated on its ArtaQuest page.
