## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Publishing a post

1. Run `python3 scripts/make-og.py` to build the social preview image from the header illustration.
2. Remove `draft: true` (and any working comments) from the post's front matter, build, commit, push: GitHub Actions deploys to https://blog.lepee.dev.
3. Announce it on **Bluesky (@lepee.me)** and **X (@alepee)**: a short post in English with a link card using the post's header illustration. Show the text to Antoine and wait for his go before sending.

## Documentation

Full documentation: https://docs.astro.build
