# SEO implementation notes — Joor Kon Berim

This repository contains the Django **API**, not the public website's frontend.
The deployment file references a frontend at `./jourkonberim2`, but that directory
is not included in this repository. Consequently, changes here **do not**
make Google index tour pages or change their HTML title tags by themselves.

## Implemented in this branch
- Tour API responses expose `seo_title`, `seo_description`, and `image_alt`
  as backward-compatible, read-only fields; no DB migration is required.
- Text descriptions are whitespace-normalized, stripped of HTML tags,
  and shortened to approximately 155 characters.
- Tests cover basic Persian metadata and excerpt length.

## Frontend integration required
1. Locate the actual frontend repository/deployment and verify canonical URL
   patterns for tour pages. Don't invent routes based on the API's URLs.
2. Render a distinct HTML `<title>` and `<meta name="description">` for each
   indexable tour page **in the server response**. API fields are fallbacks
   and should be manually edited for top landing pages when possible.
3. Add self-referencing canonical links using the actual public page URL.
4. Generate an XML sitemap on the **public frontend domain**, with only
   accessible canonical pages (active tours, destinations, articles).
   Add its location to the public site's `robots.txt`.
5. Add structured data for pages only where its information matches visible
   content; do not invent ratings, tour dates, or availability.
6. Verify status codes, mobile rendering, internal links, image dimensions,
   alt text, and Google Search Console indexing after deployment.

## Production / security concerns spotted during code review
- `config/settings.py` presently hardcodes a development secret and
  `DEBUG=True`. Check real deployment environment and rotate exposed secrets.
- `.env`, `db.sqlite3`, and `__pycache__` appear committed to the Git
  repository. Review and remove sensitive artifacts **with a deliberate secret
  rotation plan**; simply deleting a file does not erase Git history.
- Do not expose an API-specific sitemap as the main public site's sitemap.

## Test
`python manage.py test tours.tests` (requires configured Django environment).
