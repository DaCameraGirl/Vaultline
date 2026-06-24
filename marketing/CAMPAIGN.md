# Vaultline Campaign Plan

**Product:** Vaultline — AI training media governance (provenance, QC, compliance, releases)  
**Not:** Quantum Command 52 (separate personal tool — do not mix messaging)

---

## One sentence

**Prove what went into the model — every clip traced, QC-gated, and release-ready.**

---

## Who buys (ICP)

| Priority | Buyer | Company type |
|----------|-------|--------------|
| A | Head of ML Data / Dataset Lead | Voice AI (ASR, TTS, voice agents) |
| A | VP Engineering | Video/multimodal startups |
| B | Director AI Compliance | Enterprise AI vendors |
| B | Research Engineer | University multimodal labs |

**Not your customer:** casual creators, grant seekers, housing aid users, retail investors.

---

## 30-day campaign

### Week 1 — Proof
- Run `setup/verify.ps1` — all 9 smoke checks green
- Record 90-second screen capture: upload → QC → repair → audit download
- Post video on LinkedIn + X with caption below
- Send 10 LinkedIn DMs using `outreach-templates.md` Template A

### Week 2 — Outbound
- Work `leads/target-accounts.csv` A-tier (ElevenLabs, Deepgram, Runway, Speechmatics, HeyGen)
- 5 emails/day via Hunter.io verified addresses
- Attach `one-pager.md` PDF export on every reply

### Week 3 — Community
- Hugging Face: comment on dataset governance threads; offer audit export demo
- Post in r/MachineLearning, r/speechtech — **show audit JSON**, not marketing fluff
- MLOps Community / Latent Space Discord — dataset lineage pain thread

### Week 4 — Close loop
- Follow up every Week 1–2 contact
- Offer 15-min live demo (Desktop icon → their eyes on real QC)
- Log every touch in `leads/inbound/`

---

## Where to campaign (ranked)

| Channel | Why | Action |
|---------|-----|--------|
| **LinkedIn** | Buyers live here | Post + DM dataset leads |
| **Hugging Face forums/Discord** | Dataset publishers | Governance angle |
| **X (#VoiceAI #MLOps)** | Startup engineers | Short demo clips |
| **Interspeech / NeurIPS workshops** | Speech/multimodal | Submit talk or sponsor |
| **Product Hunt** | Only after hosted SaaS | Not yet for local-only |
| **Reddit r/speechtech** | ASR community | Technical post with audit sample |
| **GitHub** | Credibility | Public repo readme + demo GIF |

**Do not campaign on:** TikTok, grant Facebook groups, housing forums, crypto Discords.

---

## Post copy (LinkedIn / X)

```
Voice and video AI teams are getting the same procurement question:

"Prove what went into the model."

Spreadsheets and shared drives are failing audits.

We built Vaultline — catalog every training clip, run QC gates,
attach compliance metadata, export immutable audit bundles.

90-second demo ↓ [video]

DM if you're shipping speech or multimodal data this quarter.
```

---

## Quantum Command 52 — separate track

QC52 is **not** Vaultline. Do not sell them together.

| | Vaultline | Quantum Command 52 |
|--|-----------|-------------------|
| Audience | AI companies | Personal research / aid organization |
| Pain | Training data audits | Grants, housing links, quantum experiments |
| Monetization | B2B SaaS / enterprise | Portfolio piece / private license |
| Campaign | LinkedIn B2B | GitHub showcase, IBM Quantum community |

QC52 campaign (if any): IBM Quantum Discord, personal portfolio, **not** enterprise outbound.

---

## Success metrics (30 days)

- 50 outbound touches
- 10 demo conversations
- 2 pilot commitments
- 9/9 smoke tests passing before every demo

---

## Before every demo

```powershell
powershell -File setup/verify.ps1
```

Double-click Desktop **Vaultline** icon. Show: Run demo → Repair → Download audit JSON.