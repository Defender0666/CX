# Career OS Ultimate by Maccy Creations

**Developer:** SAKET YADAV  
**Company:** MACCY CREATIONS

An offline-first Flet application for technical career-path guidance and a local application tracker. The Live Jobs tab intentionally contains no sample listings; only verified vacancies should be shown.

## Run locally

```sh
python -m pip install -r flet_app/requirements.txt
flet run flet_app/main.py
```

## Automated builds and public URL

Every push to `main` runs [the GitHub Actions workflow](.github/workflows/build-and-deploy.yml). It builds an Android APK, attaches it to the rolling `android-latest` prerelease, and deploys the static Flet web app to GitHub Pages. Pull requests validate the builds without publishing them.

- Web app: <https://defender0666.github.io/CX/> (available after the first successful Pages deployment)
- APK download: <https://github.com/Defender0666/CX/releases/download/android-latest/Career-OS-Ultimate.apk> (available after the first successful APK build)
- Release notes/artifact status: <https://github.com/Defender0666/CX/releases/tag/android-latest>

The APK is not Play Store signed. Review the workflow and source before installing. The app does not require API keys or cloud credentials.
