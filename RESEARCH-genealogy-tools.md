## Research: Genealogy Tools -- Gramps Web + Gramps MCP + MyHeritage
**Date:** 2026-04-04 | **Sources:** 18

---

### Key Findings

1. **Gramps Web + Gramps MCP = full AI-powered genealogy pipeline.** Self-host Gramps Web (Docker), connect the MCP server, and Claude can search, create, and analyze your entire family tree via natural language. 16 tools exposed -- search, create persons/families/events, trace ancestors/descendants.

2. **MyHeritage is a dead-end for automation.** Their Family Graph API is read-only, likely unmaintained (launched 2011), and no MCP server exists. The only useful workflow: manually export GEDCOM from MyHeritage, import into Gramps.

3. **Three MCP servers exist for genealogy, each with different strengths:**
   - **Gramps MCP** (cabout-me) -- best for structured DB work, 16 tools, full CRUD
   - **GEDCOM MCP** (Genealogy-MCP) -- works directly with .ged files, has Wikipedia enrichment
   - **FamilySearch MCP** (dulbrich) -- searches FamilySearch records online, good for Czech church records

---

### 1. Gramps Web

**What:** Open-source, self-hosted genealogy web app with full REST API. Python/Flask backend, React frontend. Backed by the Gramps project (20+ years of development).

**Data Model (9 entity types):**
| Entity | Description |
|--------|------------|
| People | Individuals with names, birth/death events |
| Families | Links between partners + children |
| Events | Birth, death, marriage, baptism, burial, etc. |
| Places | Locations with hierarchy (village > district > country) |
| Sources | Books, archives, church records |
| Citations | Specific references within sources |
| Repositories | Archives, libraries holding sources |
| Media | Photos, documents, scans |
| Notes | Free-text annotations on any object |

**REST API (OpenAPI v3, Swagger UI included):**
- `GET/POST /api/people` -- list/create persons
- `GET/PUT/DELETE /api/people/{handle}` -- read/update/delete person
- `GET/POST /api/families` -- list/create families
- `GET/POST /api/events` -- list/create events
- `GET/POST /api/places`, `/api/sources`, `/api/citations`, `/api/repositories`, `/api/media`, `/api/notes`
- `POST /api/objects` -- batch create multiple linked objects at once
- `GET /api/exporters/{extension}/file` -- export (GEDCOM, Gramps XML)
- `POST /api/importers/{extension}/file` -- import GEDCOM 5.5 or 7, Gramps XML
- `POST /api/transactions/history/{id}/undo` -- undo changes
- Token-based auth (JWT) + optional OIDC (Keycloak)

**Key API details:**
- Handles = UUIDv4 identifiers (not timestamps)
- Child-parent links: update family's `child_ref_list`, backlinks auto-populate
- Birth events: create event type "birth", reference in person's `event_ref_list`
- SQLite backend -- sequential writes recommended (or use `/api/objects` for batches)
- Latest version: **v3.10.0** (April 3, 2026)

**GEDCOM import/export:**
- Supports GEDCOM 5.5 and GEDCOM 7 (auto-detected)
- Import via web UI wizard on first run, or via API endpoint
- Export to GEDCOM or native Gramps XML

**Docker setup (3 containers):**
```yaml
services:
  grampsweb:          # Main app, port 80
    image: ghcr.io/gramps-project/grampsweb:latest
    ports: ["80:5000"]
    volumes: [gramps_users, gramps_index, gramps_thumb, gramps_cache, gramps_secret, gramps_db, gramps_media]
    environment:
      GRAMPSWEB_CELERY_CONFIG__broker_url: redis://grampsweb_redis:6379/0
      GRAMPSWEB_CELERY_CONFIG__result_backend: redis://grampsweb_redis:6379/0

  grampsweb_celery:   # Background task worker
    # Same image, runs: celery -A gramps_webapi.celery worker --loglevel=INFO --concurrency=2

  grampsweb_redis:    # Message broker
    image: redis:7.2.4-alpine
```
- 7 named volumes for persistence
- First-run wizard: create admin, import tree
- ARM supported (Raspberry Pi)
- For internet: MUST add HTTPS (nginx + Let's Encrypt)

---

### 2. Gramps MCP Server (cabout-me/gramps-mcp)

**What:** MCP server that bridges Claude (or any MCP client) to a running Gramps Web instance. 16 tools for full genealogy interaction.

**All 16 tools:**

| Category | Tool | What it does |
|----------|------|-------------|
| Search | `find_type` | Universal search using Gramps Query Language (filter by entity type) |
| Search | `find_anything` | Full-text search across all data |
| Search | `get_type` | Get detailed info about a person/family by ID |
| Create | `create_person` | Add a new person with validation |
| Create | `create_family` | Add a new family unit |
| Create | `create_event` | Add birth, death, marriage, etc. |
| Create | `create_place` | Add a location |
| Create | `create_source` | Add a source (book, archive) |
| Create | `create_citation` | Add a citation to a source |
| Create | `create_note` | Add a note |
| Create | `create_media` | Add a media object |
| Create | `create_repository` | Add a repository |
| Analysis | `tree_stats` | Get tree statistics |
| Analysis | `get_descendants` | Trace all descendants |
| Analysis | `get_ancestors` | Trace all ancestors |
| Analysis | `recent_changes` | Track recent modifications |

**Setup for Claude Code:**
```bash
claude mcp add --transport stdio gramps \
  "docker exec -i gramps-mcp-gramps-mcp-1 sh -c 'cd /app && python -m src.gramps_mcp.server stdio'"
```

**Or via Docker Compose** (MCP server + Gramps Web together):
1. Clone repo, create `.env` with Gramps Web URL + credentials + tree ID
2. `docker-compose up -d`
3. Server available at `http://localhost:8000/mcp` (HTTP transport) or stdio

**Prerequisites:**
- Running Gramps Web instance (see above)
- Gramps Web credentials (username + password)
- Tree ID (from Gramps Web System Information page)

**Limitations:**
- No delete operations documented
- `find_anything` does literal text match, not fuzzy
- Large datasets may timeout
- Requires Gramps Web to be up and accessible

---

### 3. MyHeritage

**Family Graph API:**
- REST API at familygraph.com (launched 2011)
- OAuth2 auth, JSON responses
- **READ-ONLY** -- cannot add, edit, or delete data
- Reads: users, sites, trees, individuals, photos, sources, relationships
- PHP SDK available (Apache 2.0)
- No usage fees, no NDA
- **Status: likely stale** -- no recent updates, documentation may be outdated
- familygraph.com returned 403 (possibly down/restricted)

**GEDCOM export from MyHeritage:**
- Free on any plan
- Go to Family Tree > Manage trees > Export
- Creates standard .ged file (text data only, no photos)
- Can then import into Gramps Web

**Smart Matches / Record Matches:**
- Smart Matches: algorithmically matches your tree people with other users' trees
- Record Matches: matches your people with historical records
- Both are UI-only -- no programmatic/API access to match results
- Manual review + extract workflow

**MCP server for MyHeritage:** None exists.

**MyHeritage.cz specifics:**
- Czech interface available
- Has Czech historical records
- But no programmatic access to Czech records

---

### 4. Other Genealogy MCP Servers

**GEDCOM MCP (Genealogy-MCP/gedcom-mcp):**
- Works directly with .ged files (no database needed)
- Can create, edit, query GEDCOM files
- **Wikipedia enrichment** -- extracts biographical data from Wikipedia pages
- Relationship analysis, duplicate detection, timeline generation
- Good for: quick GEDCOM manipulation without running a full Gramps Web instance

**FamilySearch MCP (dulbrich/familysearch-mcp):**
- Connects to FamilySearch.org online database
- Search persons by name, gender, dates, locations
- View detailed person info by ID
- Explore ancestors (8 gen) and descendants (3 gen)
- Requires FamilySearch account (free)
- **Critical for Czech research** -- FamilySearch has 4.6M+ images of Czech church books (1552-1981) from archives in Litomerice, Trebon, Opava, Zamrsk

**Ancestry MCP (reeeeemo/ancestry-mcp):**
- Basic: list, view, rename GEDCOM files
- No enrichment, no write beyond rename
- Minimal utility

---

### 5. Recommended Workflow

```
MyHeritage.cz                FamilySearch.org
     |                            |
     | GEDCOM export              | FamilySearch MCP
     v                            v
+------------------------------------------+
|           GRAMPS WEB (Docker)            |
|  Self-hosted, full REST API, SQLite DB   |
|  Import GEDCOM 5.5/7, Gramps XML        |
+------------------------------------------+
     ^                ^               ^
     |                |               |
  Gramps MCP      GEDCOM MCP    Manual research
  (Claude Code)   (offline .ged)  (web scraping)
     |
     v
+------------------------------------------+
|         CLAUDE CODE (via MCP)            |
|  - Search & analyze family tree          |
|  - Create persons, families, events      |
|  - Trace ancestors/descendants           |
|  - Cross-reference with FamilySearch     |
|  - Generate reports & timelines          |
+------------------------------------------+
```

**Step-by-step setup:**

1. **Deploy Gramps Web** (Docker on local Mac or VPS)
   ```bash
   mkdir ~/gramps-web && cd ~/gramps-web
   # Download docker-compose.yml from gramps-project/gramps-web-docs
   docker compose up -d
   # Open http://localhost:80, create admin, import GEDCOM
   ```

2. **Import existing data**
   - Export GEDCOM from MyHeritage.cz (Family Tree > Manage trees > Export)
   - Import into Gramps Web via first-run wizard or API

3. **Set up Gramps MCP for Claude Code**
   ```bash
   claude mcp add --transport stdio gramps \
     "docker exec -i gramps-mcp-gramps-mcp-1 sh -c 'cd /app && python -m src.gramps_mcp.server stdio'"
   ```
   Or add to `~/.claude/settings.json` with HTTP transport.

4. **Set up FamilySearch MCP** (for online record search)
   - Create free FamilySearch account
   - Install the MCP server, configure credentials
   - Use to search Czech church records, censuses, civil registers

5. **Enrichment workflow via Claude:**
   - "Find all people born in Bohemia before 1900"
   - "Search FamilySearch for marriage records of Josef Hoffmann in Praha"
   - "Create a new person: Anna Hoffmannova, born 1865, Plzen"
   - "Link Anna as daughter to family of Josef and Marie Hoffmann"
   - "Get all ancestors of [person handle] going back 8 generations"
   - "Export the tree as GEDCOM for backup"

---

### 6. Czech-Specific Genealogy Sources

| Source | What it has | Access |
|--------|------------|--------|
| FamilySearch | 4.6M+ images of Czech church books 1552-1981 | Free, MCP available |
| Porta Fontium | Czech-Bavarian cross-border church records | Free, web only |
| Actapublica.eu | Czech regional archive scans | Free, web only |
| DEMoS | Czech census/inhabitant registers | Free, web only |
| MyHeritage.cz | Some Czech records + Smart Matches | Paid, GEDCOM export |
| Matricula-online.eu | Catholic church books (Moravia) | Free, web only |

For Czech sources without APIs (Actapublica, Porta Fontium, DEMoS), the workflow is:
manual research > save findings > create entries via Gramps MCP.

---

### Sources

- [Gramps Web - GitHub](https://github.com/gramps-project/gramps-web) -- main project repo
- [Gramps Web API - GitHub](https://github.com/gramps-project/gramps-web-api) -- REST API backend (v3.10.0)
- [Gramps Web API Docs](https://gramps-project.github.io/gramps-web-api/) -- OpenAPI/Swagger spec
- [Gramps Web Deployment](https://www.grampsweb.org/install_setup/deployment/) -- Docker setup guide
- [Gramps MCP - GitHub](https://github.com/cabout-me/gramps-mcp) -- MCP server for Claude/AI
- [Gramps MCP Release Announcement](https://gramps.discourse.group/t/release-gramps-web-mcp-v1-0-connect-ai-assistants-to-your-family-tree/8541)
- [GEDCOM MCP - Glama](https://glama.ai/mcp/servers/@airy10/GedcomMCP) -- direct GEDCOM file manipulation MCP
- [FamilySearch MCP](https://mcp.aibase.com/server/1916341237915033601) -- FamilySearch online search MCP
- [Ancestry MCP - GitHub](https://github.com/reeeeemo/ancestry-mcp) -- basic GEDCOM file viewer
- [MyHeritage Family Graph API](https://www.familygraph.com/documentation) -- read-only REST API (likely stale)
- [MyHeritage GEDCOM Export](https://www.myheritage.com/help/en/articles/12851866) -- how to export
- [MyHeritage Scribe AI](https://blog.myheritage.com/2026/03/introducing-scribe-ai/) -- AI document transcription (2026)
- [FamilySearch Czech Records](https://www.familysearch.org/en/wiki/Czechia_Online_Genealogy_Records) -- Czech genealogy collections
- [Using Gramps Web API for adding info](https://gramps.discourse.group/t/using-gramps-web-api-for-adding-new-information/8652) -- POST endpoint details
- [FamilySearch Developer API](https://developers.familysearch.org/) -- official developer portal
- [Gramps Web API Releases](https://github.com/gramps-project/gramps-web-api/releases) -- changelog

---

### Recommendations

1. **Start with Gramps Web on Docker locally** -- it's the hub everything connects to. Takes 15 minutes to set up. Import your existing GEDCOM from MyHeritage.

2. **Install Gramps MCP first** -- this gives Claude Code direct access to your tree. The 16 tools cover everything you need for day-to-day genealogy work.

3. **Add FamilySearch MCP second** -- critical for Czech research. FamilySearch has the largest collection of Czech church records, and the MCP lets Claude search them directly.

4. **Skip building MyHeritage integration** -- their API is read-only and probably abandoned. Just export GEDCOM periodically and reimport.

5. **Consider the GEDCOM MCP as a supplement** -- useful for offline work, Wikipedia enrichment, and quick GEDCOM manipulation without the full Gramps Web stack.

6. **For Czech-specific enrichment**, plan manual research sessions on Actapublica.eu and Porta Fontium, then batch-enter findings via Gramps MCP. No APIs exist for these archives.
