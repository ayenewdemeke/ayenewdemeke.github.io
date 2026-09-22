# ayenewdemeke.me: academic website

Personal academic site of **Ayenew Yihune Demeke** (PhD student, Civil, Construction and Environmental Engineering, North Dakota State University). It's built on the academicpages Jekyll template and served by GitHub Pages at https://ayenewdemeke.me (`CNAME`).

**The site has one goal: make the papers easy to find in Google, Google Scholar, and AI search engines, so they get cited.** Keep the template's default look. Don't spend effort on design. AGENTS.md describes the template in general; where it conflicts with this file, follow this file.

## Layout

- `_publications/*.md`: one file per paper. The body is normally empty, and `_layouts/publication.html` renders everything from front matter.
- `_includes/head/scholar.html`: Google Scholar (Highwire Press) `citation_*` meta tags and schema.org `ScholarlyArticle` JSON-LD. They're emitted **only** on publication pages. No other include may emit `citation_*` tags.
- `files/`: public PDFs, named `<firstauthorlastname><year>-<3-6-word-slug>.pdf`, e.g. `demeke2026-dynamic-hazard-zone-proximity-detection.pdf`.
- `_pages/about.md`: home page bio. Link each paper from the bio when it fits a research theme.
- `_config.yml`: profile. `author.scholar_name` must equal the author's "Last, First" string used in publication `authors` lists (for bolding and JSON-LD `sameAs`).
- `scripts/add_pdf_cover.py`: prepends a license or notice cover page to a PDF.
- Raw inputs (publisher files, original PDFs, BibTeX exports) live **outside** the repo in `../website-inputs/` and are never committed.

## Procedure: "add this paper"

Input: a PDF plus a DOI (or a BibTeX entry). Follow every step, in order.

1. **Metadata.** Fetch it from Crossref: `curl -s https://api.crossref.org/works/<DOI>`. Get the exact title, all authors (given and family), venue, volume, issue, pages or article number, publisher, dates and license. Use the Crossref title and author forms. Don't invent anything. If a field is unknown, leave it out or ask.
2. **Name form.** Write the site owner as `Demeke, Ayenew Yihune` in `authors` and as "Ayenew Yihune Demeke" in prose. Keep multi-word family names intact, e.g. `Younesi Heravi, Moein`.
3. **Which PDF may be posted.** Check the PDF's first pages to identify its version (submitted, accepted or published). Also check the Crossref `license` field and Unpaywall (`https://api.unpaywall.org/v2/<DOI>?email=ayenew.demeke@ndsu.edu`). Then apply the rule for the publisher:
   - **Publisher's typeset PDF:** never host it, unless the article is open access under CC BY. If it's free on the publisher's or society's site but has no open license ("bronze"), set `external_pdf` and `external_pdf_host` instead of `pdf`.
   - **Elsevier accepted manuscript:** allowed on a personal site immediately. Prepend a cover page with "© <year>. This manuscript version is made available under the CC-BY-NC-ND 4.0 license https://creativecommons.org/licenses/by-nc-nd/4.0/" and the DOI link. Put the same text in `pdf_note`.
   - **ASCE accepted manuscript:** prepend the cover line "This material may be downloaded for personal use only. Any other use requires prior permission of the American Society of Civil Engineers. This material may be found at https://doi.org/<DOI>". Put it in `pdf_note` too.
   - **Springer accepted manuscript:** host it unmodified; the AM terms forbid reformatting. `pdf_note` says it's subject to Springer Nature's AM terms.
   - **SAGE:** the accepted version is allowed on a personal site. CC BY articles may host the published PDF.
   - **arXiv preprint:** may be hosted, labeled as a preprint in `pdf_note`.
   - **Unsure, or a publisher not listed here:** check the publisher's self-archiving policy (or Sherpa Romeo). **Ask Ayenew before hosting.**
4. **Build the PDF** into `files/` with the naming rule above. For a cover page, run `python scripts/add_pdf_cover.py …` from a venv outside the repo that has `pypdf` and `reportlab`. The cover page's first line must be the exact paper title, because Scholar reads the PDF's first page. Keep each PDF under about 10 MB.
5. **Write the front matter** in `_publications/<year>-<firstauthorlastname>-<slug>.md`. Copy an existing file as the template. The fields are:
   - `title`, `collection: publications`
   - `category`: `manuscripts` (journal) or `conferences`
   - `permalink: /publication/<pdf-basename>/`
   - `date` (YYYY-MM-DD, used for sort order)
   - `citation_date`: `"YYYY/MM/DD"` if the exact date is known, else `"YYYY"`; use the year on the issue or proceedings
   - `citation_online_date`, if it differs
   - `venue`, `publisher`, `volume`, `issue`
   - `firstpage` and `lastpage`, or the article number in `firstpage`
   - `doi`, `authors` (a list of "Last, First" strings)
   - `pdf` or `external_pdf`, and `pdf_note`
   - `keywords` (from the paper)
   - `excerpt`
   - `abstract` (verbatim from the paper; the published version if available)
   - `citation` (APA, as HTML, with a DOI link)
   - `bibtex` (with the DOI)
6. **Write `excerpt`: a plain-language summary** of 2–3 sentences. State the method and the key quantitative finding directly, using only facts from the abstract or paper, with no hype and no claims beyond the paper. It becomes the meta description and the text AI search engines quote.
7. **Link the paper from `_pages/about.md`** under the matching research theme.
8. **Build and verify** (see below). Check that the new page's `<head>` has citation_title, one citation_author per author, citation_publication_date, citation_journal_title or citation_conference_title, citation_doi, citation_pdf_url (an absolute URL, only if `pdf` is set) and citation_abstract_html_url. Check that the JSON-LD parses and that the page appears in `_site/sitemap.xml`.
9. **Show Ayenew the summary and the meta tags, and wait for approval** before committing and pushing.

## Local build

GitHub Pages uses the `github-pages` gem (Jekyll 3.10). That needs **Ruby 3.3**, not Homebrew's default Ruby 4:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
bundle config set --local path vendor/bundle   # once
bundle install                                  # once / after Gemfile changes
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
bundle exec jekyll serve                        # preview at http://localhost:4000
```

`_site/`, `vendor/` and `Gemfile.lock` are gitignored.
