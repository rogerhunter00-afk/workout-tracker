from pathlib import Path

p = Path('index.html')
s = p.read_text()
original = s

def replace_once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s = s.replace(old, new, 1)

def replace_between(start_marker, end_marker, replacement, label):
    global s
    a = s.find(start_marker)
    if a < 0:
        raise SystemExit(f'{label}: start marker not found')
    b = s.find(end_marker, a)
    if b < 0:
        raise SystemExit(f'{label}: end marker not found')
    s = s[:a] + replacement + s[b:]

# ---------- styles ----------
replace_once('''  .bk-error{color:var(--danger);font-size:13.5px;margin:12px 0 0;}\n''', '''  .bk-error{color:var(--danger);font-size:13.5px;margin:12px 0 0;}\n  .brand-stack{display:flex;align-items:baseline;gap:9px;min-width:0;}\n  .user-badge{display:none;font-family:"Barlow Condensed";font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--clay-soft);border:1px solid var(--line2);background:var(--surface);padding:3px 7px;border-radius:999px;max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}\n  .theme-presets{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin:8px 0 14px;}\n  .theme-chip{min-width:0;border:1px solid var(--line2);background:var(--bg2);color:var(--tan);border-radius:11px;padding:8px 3px 7px;font:600 10px/1 "Barlow",sans-serif;text-transform:uppercase;letter-spacing:.5px;display:flex;flex-direction:column;align-items:center;gap:6px;}\n  .theme-chip.on{border-color:var(--clay);color:var(--cream);background:var(--surface2);}\n  .theme-dot{width:17px;height:17px;border-radius:50%;box-shadow:0 0 0 2px rgba(255,255,255,.08) inset;}\n  .colour-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:14px;}\n  .colour-field{min-width:0;}\n  .colour-field label{display:block;color:var(--dim);font-size:10px;text-transform:uppercase;letter-spacing:.8px;margin-bottom:5px;}\n  .colour-field input[type=color]{width:100%;height:42px;border:1px solid var(--line2);border-radius:10px;background:var(--bg2);padding:4px;}\n''', 'personalisation styles')

# ---------- top bar identity ----------
replace_once('''      <div class="brand">STRONG<b>ROOM</b></div>''', '''      <div class="brand-stack"><div class="brand">STRONG<b>ROOM</b></div><div class="user-badge" id="userBadge"></div></div>''', 'topbar identity')

# ---------- cloud setup + profile UI ----------
replace_once('''    <div id="cloudSetup">\n      <p class="muted">Your workout log stays on this device and syncs privately through Strongroom Cloud. Sign in once; no GitHub token is needed.</p>\n      <div class="field"><label>Email</label><input id="cloudEmail" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" /></div>\n      <div class="field"><label>Password</label><input id="cloudPassword" type="password" autocomplete="current-password" placeholder="At least 6 characters" /></div>\n      <div class="btn-row">\n        <button class="btn btn-primary" id="cloudSignIn">Sign in</button>\n        <button class="btn btn-ghost" id="cloudCreate">Create account</button>\n      </div>\n      <p class="bk-error" id="cloudError" style="display:none"></p>\n    </div>\n\n    <div class="divider"></div>''', '''    <div id="cloudSetup">\n      <p class="muted">Your workout log stays on this device and syncs privately through Strongroom Cloud. Sign in once; no GitHub token is needed.</p>\n      <div class="field"><label>Display name <span style="color:var(--dim);font-weight:400">(new accounts)</span></label><input id="cloudName" type="text" autocomplete="name" placeholder="e.g. Cesca" /></div>\n      <div class="field"><label>Email</label><input id="cloudEmail" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" /></div>\n      <div class="field"><label>Password</label><input id="cloudPassword" type="password" autocomplete="current-password" placeholder="At least 6 characters" /></div>\n      <div class="btn-row">\n        <button class="btn btn-primary" id="cloudSignIn">Sign in</button>\n        <button class="btn btn-ghost" id="cloudCreate">Create account</button>\n      </div>\n      <p class="bk-error" id="cloudError" style="display:none"></p>\n    </div>\n\n    <div id="profilePanel" style="display:none">\n      <div class="divider"></div>\n      <p class="seclabel">Personalise</p>\n      <div class="field"><label>Name</label><input id="profileName" type="text" autocomplete="name" placeholder="Your name" /></div>\n      <label style="display:block;color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.8px">Theme</label>\n      <div class="theme-presets" id="themePresets">\n        <button type="button" class="theme-chip" data-theme="clay"><span class="theme-dot" style="background:#bd6f46"></span>Clay</button>\n        <button type="button" class="theme-chip" data-theme="berry"><span class="theme-dot" style="background:#c4778d"></span>Berry</button>\n        <button type="button" class="theme-chip" data-theme="ocean"><span class="theme-dot" style="background:#5f96a8"></span>Ocean</button>\n        <button type="button" class="theme-chip" data-theme="sage"><span class="theme-dot" style="background:#8a9a6b"></span>Sage</button>\n        <button type="button" class="theme-chip" data-theme="lavender"><span class="theme-dot" style="background:#9985b5"></span>Lavender</button>\n      </div>\n      <div class="colour-grid">\n        <div class="colour-field"><label>Accent</label><input id="profileAccent" type="color" value="#bd6f46" /></div>\n        <div class="colour-field"><label>Background</label><input id="profileBackground" type="color" value="#1c1813" /></div>\n        <div class="colour-field"><label>Completed</label><input id="profileCompletion" type="color" value="#8a9a6b" /></div>\n      </div>\n      <div class="btn-row">\n        <button class="btn btn-primary" id="profileSave">Save appearance</button>\n        <button class="btn btn-ghost" id="profileReset">Reset colours</button>\n      </div>\n      <p class="bk-error" id="profileError" style="display:none"></p>\n    </div>\n\n    <div class="divider"></div>''', 'cloud/profile settings')

# ---------- state ----------
old_state = '''// ---- app state ----\nlet DATA = store.get("wt_data") || seed();\nlet dirty = !!store.get("wt_dirty");           // local changes not yet in Strongroom Cloud\nlet lastSync = store.get("wt_lastsync") || null;\nlet lastSyncError = null;\nlet cur  = todayKey();                          // current day key\nlet calMonth = new Date();                       // calendar view month\nlet editingIdx = null;                           // exercise being edited\n\nconst SB_URL = "https://hkxgkbdrazktzmuujeqq.supabase.co";\nconst SB_KEY = "sb_publishable_0Su_8qOrteBTkEdLxCWDbA_9Ez-N-IT";\nconst SB = (window.supabase && window.supabase.createClient)\n  ? window.supabase.createClient(SB_URL, SB_KEY, {auth:{persistSession:true, autoRefreshToken:true, detectSessionInUrl:true}})\n  : null;\nlet CLOUD_USER = null;\nlet cloudTimer = null;\nlet cloudRetryTimer = null;\nlet cloudBusy = false;\n'''
new_state = '''// ---- app state ----\n// Keep the old single-user cache intact as a migration source. Once an account\n// is active, Strongroom uses user-scoped localStorage keys so two people can\n// safely use the same browser without crossing workout data.\nconst LEGACY_DATA = store.get("wt_data") || null;\nconst LEGACY_DIRTY = !!store.get("wt_dirty");\nlet DATA = LEGACY_DATA || store.get("wt_guest_data") || seed();\nlet dirty = LEGACY_DIRTY || !!store.get("wt_guest_dirty");\nlet lastSync = store.get("wt_lastsync") || null;\nlet lastSyncError = null;\nlet cur  = todayKey();                          // current day key\nlet calMonth = new Date();                       // calendar view month\nlet editingIdx = null;                           // exercise being edited\n\nconst SB_URL = "https://hkxgkbdrazktzmuujeqq.supabase.co";\nconst SB_KEY = "sb_publishable_0Su_8qOrteBTkEdLxCWDbA_9Ez-N-IT";\nconst SB = (window.supabase && window.supabase.createClient)\n  ? window.supabase.createClient(SB_URL, SB_KEY, {auth:{persistSession:true, autoRefreshToken:true, detectSessionInUrl:true}})\n  : null;\nlet CLOUD_USER = null;\nlet CLOUD_PROFILE = null;\nlet PROFILE_DRAFT = null;\nlet CLOUD_READY = false;\nlet cloudTimer = null;\nlet cloudRetryTimer = null;\nlet cloudBusy = false;\n\nconst THEME_PRESETS = {\n  clay:{accent:"#bd6f46", background:"#1c1813", completion:"#8a9a6b"},\n  berry:{accent:"#c4778d", background:"#20171c", completion:"#91a477"},\n  ocean:{accent:"#5f96a8", background:"#121c20", completion:"#82a889"},\n  sage:{accent:"#8a9a6b", background:"#171d16", completion:"#b8a06a"},\n  lavender:{accent:"#9985b5", background:"#1b1821", completion:"#7fa08a"}\n};\n'''
replace_once(old_state, new_state, 'app state')

# ---------- local persistence ----------
replace_once('''// ---- persistence: local-first; Supabase sync is asynchronous ----\nfunction persistLocal(){ store.set("wt_data", DATA); }\n\nfunction save(reason){\n  persistLocal();\n  dirty = true; store.set("wt_dirty", true);\n  if(CLOUD_USER) scheduleCloudSync(1800);\n}\n''', '''// ---- persistence: local-first; Supabase sync is asynchronous ----\nfunction scopedKey(kind, user){\n  const u = user===undefined ? CLOUD_USER : user;\n  return u ? `wt_${kind}_${u.id}` : `wt_guest_${kind}`;\n}\nfunction persistLocal(){ store.set(scopedKey("data"), DATA); }\nfunction setDirty(v){ dirty=!!v; store.set(scopedKey("dirty"), dirty); }\nfunction setLastSync(v){ lastSync=v||null; store.set(scopedKey("lastsync"), lastSync); }\n\nfunction save(reason){\n  persistLocal();\n  setDirty(true);\n  if(CLOUD_USER && CLOUD_READY) scheduleCloudSync(1800);\n}\n''', 'scoped local persistence')

# ensure helper does not write the old global dirty key
s = s.replace('dirty = true; store.set("wt_dirty", true);', 'setDirty(true);')

# ---------- cloud/profile/auth engine ----------
new_cloud = r'''async function cloudPush(){
  if(!SB || !CLOUD_USER || !CLOUD_READY) return false;
  const {error} = await SB.from("strongroom_state").upsert(
    {user_id:CLOUD_USER.id, data:DATA, updated_at:new Date().toISOString()},
    {onConflict:"user_id"}
  );
  if(error) throw error;
  setDirty(false);
  setLastSync(Date.now());
  lastSyncError=null;
  // Supabase is now the backup. Remove the old GitHub PAT from this browser
  // only after a cloud write succeeds.
  store.set("wt_cfg", {owner:"",repo:"",branch:"main",token:""});
  store.set("wt_sha", null);
  return true;
}

function hasLoggedData(data){
  if(!data || !data.workouts) return false;
  return Object.keys(data.workouts).some(k=>{
    const w=data.workouts[k];
    return w && Array.isArray(w.exercises) && w.exercises.some(ex=>Array.isArray(ex.sets)&&ex.sets.some(v=>v!==null));
  });
}
function cloneData(v){ return JSON.parse(JSON.stringify(v)); }
function accountName(){
  return (CLOUD_PROFILE&&CLOUD_PROFILE.display_name) || (CLOUD_USER&&CLOUD_USER.user_metadata&&CLOUD_USER.user_metadata.display_name) || (CLOUD_USER&&CLOUD_USER.email?CLOUD_USER.email.split("@")[0]:"this account");
}

function normalHex(v, fallback){ return /^#[0-9a-f]{6}$/i.test(String(v||"")) ? String(v).toLowerCase() : fallback; }
function mixHex(a,b,t){
  a=normalHex(a,"#000000").slice(1); b=normalHex(b,"#ffffff").slice(1); t=Math.max(0,Math.min(1,t));
  const ar=parseInt(a.slice(0,2),16), ag=parseInt(a.slice(2,4),16), ab=parseInt(a.slice(4,6),16);
  const br=parseInt(b.slice(0,2),16), bg=parseInt(b.slice(2,4),16), bb=parseInt(b.slice(4,6),16);
  const h=n=>Math.round(n).toString(16).padStart(2,"0");
  return "#"+h(ar+(br-ar)*t)+h(ag+(bg-ag)*t)+h(ab+(bb-ab)*t);
}
function hexLuma(h){
  h=normalHex(h,"#1c1813").slice(1);
  const c=[0,2,4].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4));
  return .2126*c[0]+.7152*c[1]+.0722*c[2];
}
function defaultProfile(name, requestedTheme){
  const n=(name||"Strongroom").trim()||"Strongroom";
  const chosen = requestedTheme && THEME_PRESETS[requestedTheme] ? requestedTheme : (n.toLowerCase()==="cesca" ? "berry" : "clay");
  const t=THEME_PRESETS[chosen];
  return {display_name:n, theme:chosen, accent:t.accent, background:t.background, completion:t.completion};
}
function applyTheme(profile){
  const p=profile || defaultProfile("Strongroom","clay");
  const preset=THEME_PRESETS[p.theme];
  const accent=normalHex(p.accent, preset?preset.accent:"#bd6f46");
  const background=normalHex(p.background, preset?preset.background:"#1c1813");
  const completion=normalHex(p.completion, preset?preset.completion:"#8a9a6b");
  const r=document.documentElement.style;
  r.setProperty("--bg",background);
  r.setProperty("--bg2",mixHex(background,"#ffffff",.035));
  r.setProperty("--surface",mixHex(background,"#ffffff",.085));
  r.setProperty("--surface2",mixHex(background,"#ffffff",.13));
  r.setProperty("--line",mixHex(background,"#ffffff",.18));
  r.setProperty("--line2",mixHex(background,"#ffffff",.26));
  r.setProperty("--clay",accent);
  r.setProperty("--clay-deep",mixHex(accent,"#000000",.18));
  r.setProperty("--clay-soft",mixHex(accent,"#ffffff",.22));
  r.setProperty("--sage",completion);
  r.setProperty("--olive",mixHex(completion,"#000000",.22));
  r.setProperty("--ochre",mixHex(accent,"#ffffff",.14));
  const light=hexLuma(background)>.45;
  r.setProperty("--cream",light?"#211b15":"#ece3d4");
  r.setProperty("--tan",light?"#4d453b":"#bcae97");
  r.setProperty("--dim",light?"#6d6255":"#857a69");
  const meta=document.querySelector('meta[name="theme-color"]'); if(meta) meta.content=background;
}
function profileError(msg){
  const e=el("profileError"); if(!e) return;
  e.textContent=msg||""; e.style.display=msg?"":"none";
}
function renderProfile(){
  const panel=el("profilePanel"), badge=el("userBadge");
  if(panel) panel.style.display=(CLOUD_USER&&CLOUD_PROFILE)?"":"none";
  if(badge){
    const nm=CLOUD_PROFILE&&CLOUD_PROFILE.display_name;
    badge.textContent=nm||""; badge.style.display=nm?"":"none";
  }
  if(!CLOUD_PROFILE){ return; }
  PROFILE_DRAFT ||= {...CLOUD_PROFILE};
  if(el("profileName")) el("profileName").value=PROFILE_DRAFT.display_name||"";
  if(el("profileAccent")) el("profileAccent").value=normalHex(PROFILE_DRAFT.accent,"#bd6f46");
  if(el("profileBackground")) el("profileBackground").value=normalHex(PROFILE_DRAFT.background,"#1c1813");
  if(el("profileCompletion")) el("profileCompletion").value=normalHex(PROFILE_DRAFT.completion,"#8a9a6b");
  document.querySelectorAll(".theme-chip").forEach(b=>b.classList.toggle("on",b.dataset.theme===PROFILE_DRAFT.theme));
}
function chooseTheme(name){
  if(!THEME_PRESETS[name] || !CLOUD_PROFILE) return;
  const t=THEME_PRESETS[name];
  PROFILE_DRAFT={...(PROFILE_DRAFT||CLOUD_PROFILE),theme:name,accent:t.accent,background:t.background,completion:t.completion};
  applyTheme(PROFILE_DRAFT); renderProfile();
}
async function loadProfile(){
  if(!SB || !CLOUD_USER) return false;
  const {data,error}=await SB.from("strongroom_profiles").select("display_name,theme,accent,background,completion").eq("user_id",CLOUD_USER.id).maybeSingle();
  if(error) throw error;
  if(data){ CLOUD_PROFILE=data; }
  else {
    const m=CLOUD_USER.user_metadata||{};
    const base=defaultProfile(m.display_name || (CLOUD_USER.email?CLOUD_USER.email.split("@")[0]:"Strongroom"), m.theme);
    const {data:made,error:makeErr}=await SB.from("strongroom_profiles").upsert({user_id:CLOUD_USER.id,...base,updated_at:new Date().toISOString()},{onConflict:"user_id"}).select("display_name,theme,accent,background,completion").single();
    if(makeErr) throw makeErr;
    CLOUD_PROFILE=made;
  }
  PROFILE_DRAFT={...CLOUD_PROFILE};
  applyTheme(CLOUD_PROFILE); renderProfile(); renderCloud();
  return true;
}
async function saveProfile(){
  if(!SB || !CLOUD_USER || !CLOUD_PROFILE) return;
  profileError(null);
  const name=(el("profileName").value||"").trim();
  if(!name){ profileError("Enter a name first."); return; }
  const draft={...(PROFILE_DRAFT||CLOUD_PROFILE),display_name:name};
  const btn=el("profileSave"), old=btn.textContent; btn.disabled=true; btn.textContent="Saving…";
  try{
    const {data,error}=await SB.from("strongroom_profiles").upsert({user_id:CLOUD_USER.id,display_name:draft.display_name,theme:draft.theme||"custom",accent:normalHex(draft.accent,"#bd6f46"),background:normalHex(draft.background,"#1c1813"),completion:normalHex(draft.completion,"#8a9a6b"),updated_at:new Date().toISOString()},{onConflict:"user_id"}).select("display_name,theme,accent,background,completion").single();
    if(error) throw error;
    CLOUD_PROFILE=data; PROFILE_DRAFT={...data}; applyTheme(data); renderProfile(); renderCloud(); toast("Appearance saved");
  }catch(e){ profileError(e.message||"Could not save appearance."); }
  finally{ btn.disabled=false; btn.textContent=old; }
}

async function loadUserState(silent){
  if(!SB || !CLOUD_USER) return false;
  cloudBusy=true; renderCloud();
  try{
    const scoped=store.get(scopedKey("data")) || null;
    const scopedDirty=!!store.get(scopedKey("dirty"));
    const scopedLast=store.get(scopedKey("lastsync")) || null;
    const {data:row,error}=await SB.from("strongroom_state").select("data,updated_at").eq("user_id",CLOUD_USER.id).maybeSingle();
    if(error) throw error;
    if(row&&row.data){
      DATA=(scoped&&scopedDirty)?mergeData(scoped,row.data):row.data;
      dirty=scopedDirty;
      lastSync=scopedLast || (row.updated_at?Date.parse(row.updated_at):null);
    } else if(scoped){
      DATA=scoped; dirty=true; lastSync=scopedLast;
    } else {
      let useLegacy=false;
      const claimed=store.get("wt_legacy_claimed_by");
      if(LEGACY_DATA && hasLoggedData(LEGACY_DATA) && !claimed){
        useLegacy=confirm(`This device already has a Strongroom workout history. Import it into ${accountName()}?\n\nChoose Cancel to start this account fresh.`);
      }
      DATA=useLegacy?cloneData(LEGACY_DATA):seed();
      if(useLegacy) store.set("wt_legacy_claimed_by",CLOUD_USER.id);
      dirty=true; lastSync=null;
    }
    ensureRoutines();
    persistLocal(); setDirty(dirty); if(lastSync) setLastSync(lastSync);
    CLOUD_READY=true;
    render(); renderUnits();
    if(!row || dirty) await cloudPush();
    else lastSyncError=null;
    if(!silent) toast("Up to date");
    return true;
  }catch(e){
    lastSyncError=e.message||String(e); scheduleCloudRetry();
    if(!silent) toast("Cloud sync failed — saved on this device");
    return false;
  }finally{ cloudBusy=false; renderCloud(); }
}

async function cloudSync(silent){
  if(!SB || !CLOUD_USER || cloudBusy) return false;
  if(!CLOUD_READY) return loadUserState(silent);
  cloudBusy=true; renderCloud();
  try{
    const localWasDirty=dirty;
    const {data:row,error}=await SB.from("strongroom_state").select("data,updated_at").eq("user_id",CLOUD_USER.id).maybeSingle();
    if(error) throw error;
    if(row&&row.data){
      DATA=localWasDirty?mergeData(DATA,row.data):row.data;
      ensureRoutines(); persistLocal(); render();
    }
    if(!row || localWasDirty || dirty) await cloudPush();
    else { setLastSync(Date.now()); lastSyncError=null; }
    clearTimeout(cloudRetryTimer); cloudRetryTimer=null;
    if(!silent) toast("Up to date");
    return true;
  }catch(e){
    lastSyncError=e.message||String(e); scheduleCloudRetry();
    if(!silent) toast("Cloud sync failed — saved on this device");
    return false;
  }finally{ cloudBusy=false; renderCloud(); }
}

async function activateCloudUser(user,silent){
  if(!user){
    CLOUD_USER=null; CLOUD_PROFILE=null; PROFILE_DRAFT=null; CLOUD_READY=false;
    DATA=store.get("wt_guest_data")||seed(); dirty=!!store.get("wt_guest_dirty"); lastSync=store.get("wt_guest_lastsync")||null; lastSyncError=null;
    applyTheme(defaultProfile("Strongroom","clay")); renderProfile(); renderCloud(); render(); return;
  }
  if(CLOUD_USER && CLOUD_USER.id===user.id && CLOUD_READY){ CLOUD_USER=user; renderCloud(); return; }
  CLOUD_USER=user; CLOUD_READY=false; lastSyncError=null;
  dirty=!!store.get(scopedKey("dirty")); lastSync=store.get(scopedKey("lastsync"))||null;
  await loadProfile();
  await loadUserState(silent);
}

async function cloudAuth(mode){
  cloudError(null);
  if(!SB){ cloudError("Cloud sync is unavailable right now."); return; }
  const name=(el("cloudName").value||"").trim();
  const email=(el("cloudEmail").value||"").trim();
  const password=el("cloudPassword").value||"";
  if(mode==="create" && !name){ cloudError("Enter a display name for the new account."); return; }
  if(!email){ cloudError("Enter your email address."); return; }
  if(password.length<6){ cloudError("Use a password of at least 6 characters."); return; }
  const btn=mode==="create"?el("cloudCreate"):el("cloudSignIn");
  const old=btn.textContent; btn.disabled=true; btn.textContent=mode==="create"?"Creating…":"Signing in…";
  try{
    const initialTheme=name.toLowerCase()==="cesca"?"berry":"clay";
    const res=mode==="create"
      ? await SB.auth.signUp({email,password,options:{data:{display_name:name,theme:initialTheme}}})
      : await SB.auth.signInWithPassword({email,password});
    if(res.error) throw res.error;
    if(mode==="create" && !res.data.session){
      cloudError("Account created. Check your email to confirm it, then return here and sign in.");
      return;
    }
    const u=res.data.user||(res.data.session&&res.data.session.user)||null;
    if(u) await activateCloudUser(u,false);
  }catch(e){ cloudError(e.message||"Could not sign in."); }
  finally{ btn.disabled=false; btn.textContent=old; }
}

async function initCloud(){
  applyTheme(defaultProfile("Strongroom","clay"));
  if(!SB){ renderCloud(); return; }
  try{
    const {data,error}=await SB.auth.getSession();
    if(error) throw error;
    if(data.session) await activateCloudUser(data.session.user,true);
    else { renderCloud(); renderProfile(); }
  }catch(e){ lastSyncError=e.message||String(e); renderCloud(); }
  SB.auth.onAuthStateChange((event,session)=>{
    if(event==="TOKEN_REFRESHED" && session){ CLOUD_USER=session.user; return; }
    setTimeout(()=>activateCloudUser(session?session.user:null,true),0);
  });
}

addEventListener("online",()=>{ if(CLOUD_USER) cloudSync(true); });
document.addEventListener("visibilitychange",()=>{
  if(document.visibilityState==="visible"&&CLOUD_USER) cloudSync(true);
});

'''
replace_between('async function cloudPush(){', '// ---- rep cycling:', new_cloud, 'cloud/profile engine')

# ---------- cloud display name ----------
replace_once('''    const who = CLOUD_USER.email ? " · "+escapeHtml(CLOUD_USER.email) : "";''', '''    const label=(CLOUD_PROFILE&&CLOUD_PROFILE.display_name) || CLOUD_USER.email || "";\n    const who = label ? " · "+escapeHtml(label) : "";''', 'cloud status identity')

# ---------- event wiring ----------
old_events = '''el("cloudSignIn").onclick=()=>cloudAuth("signin");\nel("cloudCreate").onclick=()=>cloudAuth("create");\nel("cloudSyncNow").onclick=async function(){\n  this.textContent="Syncing…"; this.disabled=true;\n  await cloudSync(false);\n  this.textContent="Sync now"; this.disabled=false;\n};\nel("cloudSignOut").onclick=async()=>{\n  if(SB) await SB.auth.signOut();\n  CLOUD_USER=null;\n  renderCloud();\n  toast("Signed out — your log stays on this device");\n};\nel("closeSettings").onclick=closeAll;\nel("closeSettings").onclick=closeAll;\n'''
new_events = '''el("cloudSignIn").onclick=()=>cloudAuth("signin");\nel("cloudCreate").onclick=()=>cloudAuth("create");\nel("cloudSyncNow").onclick=async function(){\n  this.textContent="Syncing…"; this.disabled=true;\n  await cloudSync(false);\n  this.textContent="Sync now"; this.disabled=false;\n};\nel("cloudSignOut").onclick=async()=>{\n  if(CLOUD_USER && dirty) await cloudSync(true);\n  if(SB) await SB.auth.signOut();\n  await activateCloudUser(null,true);\n  toast("Signed out");\n};\ndocument.querySelectorAll(".theme-chip").forEach(b=>b.addEventListener("click",()=>chooseTheme(b.dataset.theme)));\n["profileAccent","profileBackground","profileCompletion"].forEach(id=>{\n  el(id).addEventListener("input",()=>{\n    if(!CLOUD_PROFILE) return;\n    PROFILE_DRAFT={...(PROFILE_DRAFT||CLOUD_PROFILE),theme:"custom",accent:el("profileAccent").value,background:el("profileBackground").value,completion:el("profileCompletion").value};\n    applyTheme(PROFILE_DRAFT); renderProfile();\n  });\n});\nel("profileSave").onclick=saveProfile;\nel("profileReset").onclick=()=>{\n  if(!CLOUD_PROFILE) return;\n  chooseTheme((CLOUD_PROFILE.display_name||"").trim().toLowerCase()==="cesca"?"berry":"clay");\n};\nel("closeSettings").onclick=closeAll;\n'''
replace_once(old_events, new_events, 'cloud/profile events')

# Settings opening should refresh profile controls too
replace_once('''el("btnSettings").onclick = ()=>{ renderUnits(); renderCloud(); cloudError(null); open("ovSettings"); };''', '''el("btnSettings").onclick = ()=>{ renderUnits(); renderCloud(); renderProfile(); cloudError(null); profileError(null); open("ovSettings"); };''', 'settings open')

# Don't inject Roger's May Lean routine into every future account.
replace_once('''ensureRoutines();   // migrate v1 (flat templates) data into a routine set\nensureMayLeanRoutine();\nrender();''', '''ensureRoutines();   // migrate v1 (flat templates) data into a routine set\nrender();''', 'boot routine isolation')

if s == original:
    raise SystemExit('No changes made')
p.write_text(s)
print('Patched Strongroom multi-user accounts and personalisation')
