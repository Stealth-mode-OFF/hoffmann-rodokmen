// MyHeritage — odmítnutí všech Tschenek Smart Matches přes GraphQL
// POUŽITÍ:
// 1. Přihlas se na https://www.myheritage.cz/ v normálním Chrome
// 2. Otevři libovolnou MyHeritage stránku (např. Hofman Web Site)
// 3. F12 → Console
// 4. Zkopíruj+vlož tento celý kód a Enter
//
// Tento script:
// - Extrahuje live bearer_token z aktuální session
// - Zavolá GraphQL bulk reject pro každou Tschenek osobu
// - VYNECHÁ 3500006 (Anna Marie Richter)

(async () => {
  const TSCHENEK_IDS = [
    '3500071','3500072','3500014','3500075','3500005','3500073',
    '3500007','3500008','3500009','3500011','3500012','3500078',
    '3500010','3500017','3500074','3500076','3500077','3500079','3500080'
  ];
  const TREE_ID = 'OYYV6ZSFD34UUMVQJZSWYFYUJYW4Y7Y';

  // Intercept fetch to grab live bearer_token from next real GraphQL call
  console.log('Triggering fetch to capture fresh bearer_token…');
  let bearerToken = null;
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    const [url, opts] = args;
    if (typeof url === 'string' && url.includes('web-family-graphql') && opts?.body) {
      const body = opts.body.toString();
      const m = body.match(/bearer_token["\]=]+([^&\s"]+)/);
      if (m) bearerToken = m[1];
    }
    return originalFetch.apply(this, args);
  };

  // Trigger a fetch by navigating to any matches page via the SPA router
  // Simpler: use existing fetch wrapper — try calling a known endpoint
  await fetch(`/FP/API/DiscoveryHub/fetch-matches-by-people.php?action=getResults&s=${TREE_ID}&lang=CS&familyTreeId=&offset=0&count=5&filtersState%5BmatchType%5D=2&filtersState%5BmatchStatus%5D=64`);
  await new Promise(r => setTimeout(r, 1500));

  // Fall back: extract from cookies
  if (!bearerToken) {
    const m = document.cookie.match(/mhc_bearer_token=([^;]+)/);
    if (m) bearerToken = decodeURIComponent(m[1]);
  }

  if (!bearerToken) {
    console.error('❌ Bearer token not found. Try navigating to /discovery-hub first.');
    return;
  }
  console.log('✓ Got bearer token');

  const results = { rejected: [], failed: [] };
  for (const pid of TSCHENEK_IDS) {
    const formData = new FormData();
    formData.append('bearer_token', bearerToken);
    formData.append('query', `mutation individual_matches_bulk_update_mutation($updateData:EditableIndividual!){individual_update(id:"individual-${TREE_ID}-${pid}",lang:"CS",update_data:$updateData){id}}`);
    formData.append('description', 'bulk_match_status_updated');
    formData.append('variables', JSON.stringify({
      bulk_action: {
        matches: {
          update: { confirmation_status: { status: "rejected" } },
          params: { match_type: "smart", match_status: "pending", is_new_match: true }
        }
      },
      updateData: {}
    }));

    try {
      const resp = await originalFetch('/web-family-graphql/bulk_match_status_updated/', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.errors) { results.failed.push({pid, errors: json.errors}); }
        else { results.rejected.push(pid); console.log(`✓ ${pid}`); }
      } else {
        results.failed.push({pid, status: resp.status});
      }
    } catch(e) {
      results.failed.push({pid, err: e.message});
    }
    await new Promise(r => setTimeout(r, 300)); // rate-limit gentle
  }

  console.log(`\n=== DONE ===`);
  console.log(`Rejected: ${results.rejected.length} / ${TSCHENEK_IDS.length}`);
  if (results.failed.length) console.log('Failed:', results.failed);
  window.fetch = originalFetch; // restore
})();
