# Vote Compass Israel 🗳️

A side-by-side political platform comparison tool for Israeli elections, inspired by GSMArena's phone comparison interface.

**Live site:** [maplemoosetools.github.io/voteCompassIsrael](https://maplemoosetools.github.io/voteCompassIsrael)

---

## What it does

- Compare any number of Israeli political parties side by side
- Filter by topics you care about (economy, security, religion & state, LGBTQ+ rights, etc.)
- Each platform position is tagged with multiple relevant topics
- Unchecked topics show a colored tally of how many hidden positions each party has on that topic — so you never miss something relevant

## How to deploy (GitHub Pages)

1. Fork this repository
2. Go to **Settings → Pages**
3. Set source to **Deploy from a branch**, branch: `main`, folder: `/ (root)`
4. Your site will be live at `https://yourusername.github.io/voteCompassSsrael`

## How to update party data

All party data lives in **`data.json`**. The structure is:

```json
{
  "topics": [
    { "id": "economy", "label": "Economy & Cost of Living" }
  ],
  "parties": [
    {
      "id": "likud",
      "name": "Likud",
      "color": "#1357BE",
      "leader": "Benjamin Netanyahu",
      "bloc": "Right",
      "positions": [
        {
          "id": "likud_1",
          "title": "Opposition to Palestinian State",
          "summary": "Opposes the establishment of a Palestinian state...",
          "topics": ["peace_process", "security"]
        }
      ]
    }
  ]
}
```

Each position can have **multiple topic tags** — a position on running public transit on Shabbat, for example, would be tagged `["public_transport", "secular_society", "religion_state"]`.

## Get in touch
Please email me at votecompassisrael(at)gmail.com

## License

MIT — free to use, fork, and adapt.
