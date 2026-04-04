## Research: FamilySearch for Czech Genealogy (Hoffmann Rodokmen)
**Date:** 2026-04-04 | **Sources:** 18

---

### Key Findings

1. **FamilySearch MCP server exists** -- `@dulbrich/familysearch-mcp` by David Ulbrich. 9 tools including search-persons, get-ancestors (8 gen), search-records. Works with Claude Desktop. GitHub: https://github.com/dulbrich/familysearch-mcp

2. **GEDCOM upload is transitioning to CET (Controlled Edit Trees)** -- no longer read-only Pedigree Resource File. Your GEDCOM becomes a live, editable tree with Record Hints, collaboration (2 co-owners), and future third-party sync. This is the way to go.

3. **Czech church books from Zamrsk archive cover Rtyne and Dvur Kralove** -- Collection "Czech Republic, Church Books, 1552-1981" has 4.6M+ images. Zamrsk archive handles NE Bohemia (Trutnov district). Records are digitized at https://aron.vychodoceskearchivy.cz/ and partially indexed on FamilySearch.

4. **FamilySearch API is free** but production access requires certification. OAuth 2.0 auth. Rate limits are processing-time-based (~18s execution per 1min window), not simple request counts.

5. **Record Hints work via API** but third-party apps can only show match title + confidence score. Users must be redirected to FamilySearch.org to view actual records (legal restriction).

---

### 1. FamilySearch API

**Developer Portal:** https://developers.familysearch.org/
**Old Docs (still useful):** https://www.familysearch.org/developers/docs/api/resources

#### Authentication
- OAuth 2.0 (authorization code flow)
- Register app at https://developers.familysearch.org/ to get app key
- Each app type (web, mobile, desktop) needs separate key
- Access token required for every API call

#### Environments
| Environment | Access | Data |
|-------------|--------|------|
| Integration | Automatic with app key | Test data only |
| Beta | Limited availability | Production-like |
| Production | Requires certification | Live data |

#### Key Endpoints
| Endpoint | Methods | What it does |
|----------|---------|-------------|
| Person | GET, POST, DELETE | CRUD on tree persons |
| Persons | GET, POST | Collection queries |
| Tree Person Search | GET | Search tree by name/date/place |
| Match by Tree Person Id | GET, POST | Find duplicates and hints |
| Person Matches by Example | POST | Match without auth (limited) |
| Couple Relationship | GET, POST, DELETE | Spouse links |
| Child-and-Parents | GET, POST, DELETE | Parent-child links |
| Source Description | GET, POST, DELETE | Source citations |
| Memory | GET, POST, DELETE | Photos, docs, stories |

#### Can you search historical records via API?
**Yes, but with restrictions.** The Match by Tree Person Id endpoint returns historical record matches (hints). However, actual record data (images, indexed fields) can only be displayed by FamilySearch products -- third-party apps must redirect users to familysearch.org.

#### Can you upload/sync GEDCOM via API?
**Yes -- to CET (user-owned trees).** The new CET system replaces the old Pedigree Resource File. API documentation exists for uploading trees to CET. Early adopter program: contact developers@familysearch.org.

#### Rate Limits
- **Per-user throttling** (not per-app) -- two sessions share the same limit
- Processing-time-based: example given is "18 seconds execution time per 1 minute window"
- Different endpoints have different windows
- Exceeding returns HTTP 429 with `Retry-After` header
- Monitor via `X-PROCESSING-TIME` response header
- Unauthenticated requests throttled by app key

#### SDKs
Java, C#, PHP, JavaScript (official). Community: C, Ruby, Objective-C.

---

### 2. FamilySearch MCP Server

**Name:** familysearch-mcp
**Author:** David Ulbrich (@dulbrich)
**GitHub:** https://github.com/dulbrich/familysearch-mcp
**Language:** TypeScript
**Released:** March 24, 2025

#### Tools Exposed

| Tool | Description |
|------|-------------|
| `say-hello` | Test connection |
| `configure` | Set FamilySearch API credentials |
| `authenticate` | Login with FamilySearch account |
| `get-current-user` | Get authenticated user info |
| `search-persons` | Search Family Tree by name, gender, birth/death dates, locations |
| `get-person` | Get detailed info for a person by ID |
| `get-ancestors` | Explore up to 8 generations of ancestors |
| `get-descendants` | Explore up to 3 generations of descendants |
| `search-records` | Search historical records by surname, dates, locations, collection ID |

#### Installation

```bash
git clone https://github.com/dulbrich/familysearch-mcp.git
cd familysearch-mcp
npm install
npm run build
```

#### Claude Desktop Config (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "familysearch": {
      "command": "node",
      "args": ["/path/to/familysearch-mcp/dist/index.js"]
    }
  }
}
```

#### Requirements
- Node.js 16+
- FamilySearch developer account (app key)
- FamilySearch user account
- Credentials stored in `~/.familysearch-mcp/config.json`

#### Other Genealogy MCP Servers Found
- **ancestry-mcp** (https://github.com/reeeeemo/ancestry-mcp) -- works with local .ged GEDCOM files, Python-based
- **GEDCOM Genealogy MCP** (https://www.pulsemcp.com/servers/genealogy-mcp-gedcom) -- GEDCOM file interaction
- **Gramps Web MCP** (https://www.pulsemcp.com/servers/gramps-web) -- Gramps genealogy software integration

---

### 3. GEDCOM Upload to FamilySearch

#### Old Way: Pedigree Resource File (being deprecated)
1. Go to https://www.familysearch.org/search/genealogies
2. Click "Upload Your Individual Tree" > "Upload GEDCOM file"
3. Choose file, name it, describe it, submit
4. Wait up to 30 min for processing
5. System categorizes records: Potential Matches / Add to Family Tree / Already Exists / Invalid+Living
6. Manually review each category (side-by-side comparison)
7. **Does NOT auto-merge** -- you choose for each person

**Limits:** Max 100 MB for preservation. Recommended max 100 persons if copying to Family Tree.

#### New Way: CET (Controlled Edit Trees) -- RECOMMENDED
- **URL:** Same upload flow, but now creates a live tree instead of read-only file
- Your GEDCOM becomes an **editable, collaborative family tree**
- Up to **2 co-owners** can edit
- Full access to **Record Hints, historical records, memories**
- Privacy: viewable by others but only you/co-owners can edit (can make private)
- **Future:** third-party software sync coming
- Feedback: https://community.familysearch.org/en/group/338-cet-feedback-early-access

#### What happens when you upload?
1. GEDCOM parsed into a user-owned tree
2. System generates Record Hints (matches to historical records)
3. You can manually compare and copy into the shared FamilySearch Family Tree
4. Duplicates are flagged but **never auto-merged**
5. You control what goes into the shared tree

#### Via API (for developers)
- POST a GEDCOM X document to the Persons endpoint to create persons in CET
- Early adopter program: developers@familysearch.org
- Docs: https://developers.familysearch.org/main/docs/uploading-a-tree-to-cet

---

### 4. Hoffmann Records on FamilySearch

#### Direct Search URLs (require login)
- **Rtyne area, 1800-1900:** https://www.familysearch.org/search/record/results?q.surname=Hoffmann&q.birthLikePlace=Rtyne%2C+Czech&q.birthLikeDate.from=1800&q.birthLikeDate.to=1900
- **Dvur Kralove area, 1750-1850:** https://www.familysearch.org/search/record/results?q.surname=Hoffmann&q.birthLikePlace=Dvur+Kralove&q.birthLikeDate.from=1750&q.birthLikeDate.to=1850

Note: These pages require JavaScript/login -- WebFetch could not scrape the results. You need to search manually or use the MCP server.

#### Czech Church Books Available

**Main collection:** Czech Republic, Church Books, 1552-1981
- **Collection ID:** 1804263
- **URL:** https://www.familysearch.org/search/collection/1804263
- **Images:** 4,668,489+
- **Archives included:** Litomerice, Trebon, Opava, **Zamrsk**
- **Languages:** Czech, German, Latin

**Zamrsk Archive (covers Rtyne + Dvur Kralove):**
- Covers NE Bohemia including **Trutnov district** (where Rtyne and Dvur Kralove are)
- Roman Catholic, Evangelical, Czechoslovak Church, and civil records
- Direct access: https://aron.vychodoceskearchivy.cz/
- FamilySearch has digitized images from Zamrsk in the main collection
- Specific Rtyne matriky confirmed: https://aron.vychodoceskearchivy.cz/apu/d37a812d-3602-49ad-ad62-ab22fbee635f

**FamilySearch Catalog for Dvur Kralove:**
- https://www.familysearch.org/en/search/catalog/1968417
- Census records, church records from Dvur Kralove nad Labem area

**Other collections:**
- Czech Republic, Censuses and Inhabitant Registers, 1800s: https://www.familysearch.org/en/search/collection/1930345

#### Are Hoffmann family trees already on FamilySearch?
Could not confirm via web scraping (JS-heavy pages). Use the MCP server `search-persons` tool or log in manually to search the shared Family Tree for Hoffmann in Rtyne/Dvur Kralove.

---

### 5. FamilySearch Partner Access & Matching

#### Record Hints (automatic matching)
- FamilySearch automatically generates hints by matching tree persons to historical records
- Available in both shared Family Tree and CET (user-owned trees)
- API endpoint: `Match by Tree Person Id` (GET)
- Returns: persona name, collection title, record ID, match score/confidence, status (Pending/Accepted/Rejected)

#### API Matching Endpoints
| Endpoint | What it matches against |
|----------|----------------------|
| `collection=tree` | FamilySearch shared Family Tree (default) |
| `collection=cet` | User-owned trees (add `treeId` for specific tree) |
| `collection=records` | Historical Records archive |

#### Limitations
- **Historical record data cannot be shown in third-party apps** (legal restriction)
- Third-party can show: match title + confidence score only
- Must redirect user to FamilySearch.org for full record view
- Hinting apps must pass **API compatibility certification**

#### Bulk Import
- GEDCOM upload handles bulk import (up to 100 MB)
- For Family Tree copying: recommended max 100 persons per batch
- No true "bulk API import" -- use GEDCOM upload to CET

#### Compared to MyHeritage Record Matching
FamilySearch Record Hints is the equivalent. It automatically matches your tree persons against:
- 11M+ indexed Czech names
- 4.6M+ church book images
- Census records, civil registrations
- Other users' trees

Key difference: FamilySearch is **free** and the tree is **shared/collaborative** (or private via CET).

---

### Actionable Next Steps

#### Immediate (today)

1. **Install the FamilySearch MCP server:**
   ```bash
   cd ~/projects
   git clone https://github.com/dulbrich/familysearch-mcp.git
   cd familysearch-mcp
   npm install && npm run build
   ```
   Add to Claude Desktop config. Use `search-records` and `search-persons` to query Hoffmann records programmatically.

2. **Create FamilySearch developer account:**
   Go to https://developers.familysearch.org/ and register. Get an app key for the MCP server.

3. **Upload your GEDCOM to CET:**
   Go to https://www.familysearch.org/search/genealogies > Upload. Use the new CET experience. This gives you Record Hints automatically.

#### Short-term (this week)

4. **Search Hoffmann records manually:**
   Log into familysearch.org and search collection 1804263 (Czech Church Books) for Hoffmann in Trutnov district.

5. **Check Zamrsk archive directly:**
   Browse https://aron.vychodoceskearchivy.cz/ for Rtyne v Podkrkonosi church books. These are the original digitized matriky.

6. **Search for existing Hoffmann trees:**
   Use MCP `search-persons` tool: surname=Hoffmann, birthPlace=Rtyne or Dvur Kralove, date range 1750-1900.

#### Medium-term

7. **Apply for CET early adopter program:**
   Email developers@familysearch.org to get API access for programmatic tree management.

8. **Build automated matching pipeline:**
   Use the Match by Tree Person Id API to get Record Hints for each person in your tree. Auto-flag matches for manual review.

9. **Cross-reference with Zamrsk digital archive:**
   The direct archive at aron.vychodoceskearchivy.cz has records that may not be indexed on FamilySearch yet. Browse by parish for Rtyne.

---

### Sources

- [FamilySearch Developer Portal](https://developers.familysearch.org/) -- main dev docs, getting started, API keys
- [FamilySearch API Resources](https://www.familysearch.org/developers/docs/api/resources) -- full endpoint list
- [FamilySearch MCP Server (Glama)](https://glama.ai/mcp/servers/@dulbrich/familysearch-mcp) -- MCP server listing
- [FamilySearch MCP Server (PulseMCP)](https://www.pulsemcp.com/servers/dulbrich-familysearch) -- MCP details by David Ulbrich
- [FamilySearch MCP Server (AIBase)](https://mcp.aibase.com/server/1916341237915033601) -- tools and features
- [GitHub: dulbrich/familysearch-mcp](https://github.com/dulbrich/familysearch-mcp) -- source code
- [GEDCOM Upload to PRF](https://www.familysearch.org/en/help/helpcenter/article/how-do-i-upload-my-gedcom-file) -- upload instructions
- [Copy GEDCOM to Family Tree](https://www.familysearch.org/en/help/helpcenter/article/how-do-i-copy-information-from-my-gedcom-file-into-family-tree) -- merge/copy process
- [New GEDCOM Upload (CETs)](https://www.familysearch.org/en/help/helpcenter/article/the-new-gedcom-upload-experience) -- CET transition
- [CET Feedback Community](https://community.familysearch.org/en/group/338-cet-feedback-early-access) -- early access group
- [Family Tree Matching & Hinting](https://developers.familysearch.org/main/docs/family-tree-matching-and-hinting) -- hints API
- [Integrating Hints](https://developers.familysearch.org/main/docs/integrating-hints) -- hint integration guide
- [API Throttling](https://developers.familysearch.org/main/docs/throttling) -- rate limits
- [Czech Church Records Wiki](https://www.familysearch.org/en/wiki/Czechia_Church_Records) -- overview of Czech records
- [Czech Church Books Collection](https://www.familysearch.org/en/search/collection/1804263) -- 4.6M images, 1552-1981
- [Zamrsk Archive Wiki](https://www.familysearch.org/en/wiki/Z%C3%A1mrsk_Regional_Archives,_Czechia_Church_Records) -- NE Bohemia coverage
- [Zamrsk Digital Archive (ARON)](https://aron.vychodoceskearchivy.cz/) -- direct access to digitized matriky
- [2025 Q2 Developer Newsletter](https://developers.familysearch.org/main/changelog/2025-q2-newsletter) -- CET docs, migration updates
