# ExploreDH

## Ziel

ExploreDH ermöglicht einen explorativen Zugang zu den eingereichte Beiträgen der DHd 2019 sowie interessante Einblicke in die Forschungsschwerpunkte der beteiligten Universitäten.

[vollständiger Projekt Pitch](https://docs.google.com/document/d/1C9cPurW8cZGsN6hhObTlgjH8w_00AFenBmFrk83p4k0/edit#)


## Funktionalität

ExploreDH konzentriert sich auf die Geovisualisierung von geeigneten Informationen aus dem DHD Datensatz aus dem Jahr 2019. Dabei werden zunächst drei Aspekte dargestellt:
1. Beiteiligung einzelner Standorte an den Digital Humanities
2. ~~Forschungsschwerpunkt einzelner Standorte anhand der verwendeten Keywords~~
3. Zusammanarbeit der verschiedenen Standorte anhand gemeinsamer Artikel
4. Suchen und Anzeigen der Artikel

## Get Started

Start dev environment:
- navigate to `./src/`
- run `npm install` (this will install all necessary packages)
- to start the webserver run `npm start`
- connect via `localhost:5012` on Chrome or Firefox (port may differ, check terminal output on npm start)

Start live environment (this requires a linux server with `screen`):
- navigate to `./src/`
- run `npm install` (this will install all necessary packages)
- run `npm run publish` (this will check and build the code into the `/build` folder)
- run `npm run start:live` (this will start the server in a detached screen-session)
- use `screen -r` to access the servers screen-session

Use the parser:
- install Python3 (3.7) with requests
- navigate to `./src/scripts`
- run `python parser_main.py`, you can use flag `-d` to trigger a database rewrite or `-r` to trigger a new parser (as standard, data is pulled from cache)
- afterwards you can use all files with `processing_` prefix, py using `python [filename]`

## Navigation

```
∟ data: files from the DHD Data Repo and output directory for the parser
   ∟ db: sql database
   ∟ output: used to output json/other files
   ∟ preprocessed: [read only] xml files with preprocessed info from DHD Data Repo
   ∟ TEI: [read only] xml files from DHD Data Repo, not preprossed

∟ docs: documentation and graphics for markdown files

∟ src: source files, files for the webserver are on this level, for more information read src/readme.md
   ∟ scripts: [python]: contains parser, for more info read src/scripts/readme.md
   ∟ www: [html/css/js]: clientside code for the website
```