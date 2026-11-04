# Reference sharing

Findings for resuming the team-library work after the November 4, 2026 M5
session. No PDFs or access settings were changed by this review.

## Workspace and publication

The current repository is `fjhickernell/Lattice-Sequence-Quality`. GitHub was
verified public, with only Fred configured as a collaborator and no forks,
Pages site or Actions workflows. Fred proposed making it private and said he
can also provide team GitHub usernames; await his further direction and
recheck the live state. Do not assume the visibility change has happened.
Overleaf access settings were not inspected or changed.

GitHub and Overleaf are a paired publication target. Adding a file to either
Git history can carry it to the other through the bridge. Do not treat the
Overleaf mirror as a separate private-only storage location while GitHub
remains public. Use the verified `Lattice-Sequence-Quality` binding in
SharedConfigs `settings/overleaf-sync.json`; preserve the existing branch and
upstream. The repository's `AGENTS.md` specifies the bridge command.

## Files and versions

The [literature inventory](../relevant%20articles/LITERATURE.md) identifies all
twelve references, their versions and sources. Four reading PDFs are already
tracked; eight additional reference PDFs are explicitly excluded by
`relevant articles/.gitignore` and remain on M5. Generated manuscript and
revision-note PDFs are a separate exclusion; their LaTeX sources are tracked.

The earlier blanket exclusion should be revisited paper by paper, especially
for Fred's own author manuscripts. Public availability of a download does
not by itself establish a redistribution license; author-retained rights may
provide a different sharing route. No new Creative Commons license should be
assigned to an author manuscript without a basis.

| Reference | Current copy and useful next step |
| --- | --- |
| JH19, Jagadeeswaran/Hickernell | The local 27-page file is the November 8, 2019 arXiv author version, not a publisher-layout PDF. Fred's author-sharing rights are a candidate route for including it. Confirm the version category and add the full citation, DOI and publisher acknowledgement. |
| ZLH06, Zeng/Leung/Hickernell | The local 14-page copy is an archived author manuscript. Check the proceedings author-sharing route below and include the publication notice/DOI appropriate to that version. |
| ZKH09, Zeng/Kritzer/Hickernell | The local 27-page PDF is the publisher version. A 21-page author manuscript was located in Fred's author archive; use that as a candidate replacement instead of treating the publisher PDF as freely repostable. |
| KKSS26, Kaarnioja/Klebanov/Schillings/Suzuki | The saved arXiv v3 uses arXiv's nonexclusive license; no broader redistribution permission was established. Retain the free version-pinned source link and check any private-sharing permission for the chosen workspace. |
| KS18, Karvonen/Sarkka | The publisher PDF is SIAM copyright; the arXiv version also uses the nonexclusive license. No freely redistributable alternative was established. Both the author-hosted PDF and arXiv v3 provide direct reading access. |
| BM09, Bini/Meini | The saved 35-page file is an author manuscript from Meini's site. No explicit redistribution license was found. Preserve its direct author-source link. |
| Madsen83 | The saved 19-page publisher PDF is in Elsevier's Open Archive under the Elsevier User License. Private scholarly sharing and public reposting have different terms; select a supported route after the team workspace is settled. |
| TAK07, Tsitsas/Alivizatos/Kalogeropoulos | The saved 18-page publisher PDF was obtained through Illinois Tech's ScienceDirect subscription. Elsevier's subscribed-user private-sharing terms are relevant; they do not establish permission for public GitHub posting. |

The ZKH09 candidate is in Fred's OneDrive author archive under
`Articles_Talks/Published Manuscripts/Pub2009/XiaoyanPeterLatticeNetsSplines/`,
named `SplineMethodsUsingIntegrationLatticesAndDigitalNetsByZengKritzerHickernell.pdf`.
Its adjacent `-1.pdf` is byte-identical. It is dated April 19, 2009 and uses
author layout; the archive metadata alone does not prove precise accepted-
manuscript status. SHA-256:
`02724e4bf6f29f4a788087884f22b4313cb9c2f4d4db06829166c0c34c50101c`.

## Primary policy and access sources

- [Springer electronic offprint and author-manuscript sharing](https://support.springernature.com/en/support/solutions/articles/6000081233-electronic-offprint-sharing): authors may privately send offprints to research colleagues; accepted manuscripts may be deposited after the stated embargo with source acknowledgement and publication link. Verify the relevant version before applying this route.
- [Springer book/proceedings policies](https://www.springernature.com/gp/open-science/policies/book-policies): proceedings author-manuscript sharing provisions and repository conditions.
- [Elsevier article/chapter sharing](https://www.elsevier.support/ecommerce/answer/do-i-need-permission-to-share-an-article-or-chapter): distinguishes private individual scholarly sharing by academic subscribers, private workgroups on partner sites and public posting. Do not assume an arbitrary private GitHub repository is a partner site.
- [Elsevier User License](https://www.elsevier.com/about/policies-and-standards/open-access-licenses/elsevier-user): relevant to the Madsen Open Archive copy.
- [arXiv reuse guidance](https://info.arxiv.org/help/license/reuse.html): a nonexclusive distribution license grants arXiv distribution rights, not a general reuse license to everyone. Fred's own retained author rights must be assessed separately.
- [KKSS26 v3 record](https://arxiv.org/abs/2501.09500v3) and [PDF](https://arxiv.org/pdf/2501.09500v3).
- [KS18 v3 record](https://arxiv.org/abs/1703.06359v3) and [PDF](https://arxiv.org/pdf/1703.06359v3).

Keep the paper-specific citations and download links in `LITERATURE.md` as
the file/version inventory. Update its current public/local-only explanation
when the agreed access or included versions change. Do not delete local
reading copies merely because they remain untracked.
