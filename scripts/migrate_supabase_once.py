from pathlib import Path

p = Path("index.html")
s = p.read_text()


def replace_once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {n}")
    s = s.replace(old, new, 1)


def replace_between(start, end, new, label):
    global s
    a = s.find(start)
    if a < 0:
        raise SystemExit(f"{label}: start marker not found")
    b = s.find(end, a)
    if b < 0:
        raise SystemExit(f"{label}: end marker not found")
    s = s[:a] + new + s[b:]


replace_once(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>',
    'Supabase SDK include'
)

backup_start = '    <p class="seclabel">Backup</p>\n'
backup_end = '    <div class="divider"></div>\n    <div class="btn-row">\n      <button class="btn btn-ghost" id="closeSettings">Close</button>'
backup_new = '''    <p class="seclabel">Cloud sync</p>

    <div id="cloudConnected" style="display:none">
      <p class="muted" id="cloudStatus" style="margin-bottom:14px"></p>
      <div class="btn-row">
        <button class="btn btn-sage" id="cloudSyncNow">Sync now</button>
        <button class="btn btn-ghost" id="cloudSignOut">Sign out</button>
      </div>
    </div>

    <div id="cloudSetup">
      <p class="muted">Your workout log stays on this device and syncs privately through Strongroom Cloud. Sign in once; no GitHub token is needed.</p>
      <div class="field"><label>Email</label><input id="cloudEmail" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" /></div>
      <div class="field"><label>Password</label><input id="cloudPassword" type="password" autocomplete="current-password" placeholder="At least 6 characters" /></div>
      <div class="btn-row">
        <button class="btn btn-primary" id="cloudSignIn">Sign in</button>
        <button class="btn btn-ghost" id="cloudCreate">Create account</button>
      </div>
      <p class="bk-error" id="cloudError" style="display:none"></p>
    </div>

'''
replace_between(backup_start, backup_end, backup_new, 'backup UI')

replace_once(
'''   Strongroom — personal workout tracker
   Storage: local-first (localStorage is the source of truth);
   optional GitHub backup mirrors it to data.json in this repo,
   debounced so a session is one commit, not one per tap.
   Falls back to in-memory if browser storage is unavailable.''',
'''   Strongroom — personal workout tracker
   Storage: local-first (localStorage is the immediate source of truth);
   optional Strongroom Cloud sync mirrors it privately to Supabase.
   The app remains usable offline and syncs again when connectivity returns.
   Falls back to in-memory if browser storage is unavailable.''',
'storage comment'
)

state_old = '''let DATA = store.get("wt_data") || seed();
let CFG  = store.get("wt_cfg")  || {owner:"",repo:"",branch:"main",token:""};
let SHA  = store.get("wt_sha")  || null;       // github file sha for updates
let dirty = !!store.get("wt_dirty");           // local changes not yet backed up
let lastSync = store.get("wt_lastsync") || null;
let lastSyncError = null;
let lastSyncStatus = null;
let syncRetryTimer = null;
let syncRetryAttempt = 0;
let cur  = todayKey();                          // current day key
let calMonth = new Date();                       // calendar view month
let editingIdx = null;                           // exercise being edited
'''
state_new = '''let DATA = store.get("wt_data") || seed();
let dirty = !!store.get("wt_dirty");           // local changes not yet in Strongroom Cloud
let lastSync = store.get("wt_lastsync") || null;
let lastSyncError = null;
let cur  = todayKey();                          // current day key
let calMonth = new Date();                       // calendar view month
let editingIdx = null;                           // exercise being edited

const SB_URL = "https://hkxgkbdrazktzmuujeqq.supabase.co";
const SB_KEY = "sb_publishable_0Su_8qOrteBTkEdLxCWDbA_9Ez-N-IT";
const SB = (window.supabase && window.supabase.createClient)
  ? window.supabase.createClient(SB_URL, SB_KEY, {auth:{persistSession:true, autoRefreshToken:true, detectSessionInUrl:true}})
  : null;
let CLOUD_USER = null;
let cloudTimer = null;
let cloudRetryTimer = null;
let cloudBusy = false;
'''
replace_once(state_old, state_new, 'app state')

persist_start = '// ---- persistence: local-first; the GitHub backup is async and debounced ----\n'
persist_end = '// ---- rep cycling: null -> targetReps -> targetReps-1 -> … -> 1 -> null ----\n'
persist_new = r'''// ---- persistence: local-first; Supabase sync is asynchronous ----
function persistLocal(){ store.set("wt_data", DATA); }

function save(reason){
  persistLocal();
  dirty = true; store.set("wt_dirty", true);
  if(CLOUD_USER) scheduleCloudSync(1800);
}

function filledSets(wk){ return wk.exercises.reduce((a,ex)=>a+ex.sets.filter(v=>v!==null).length,0); }
function hasLocalLog(){ return Object.keys(DATA.workouts).some(k=>filledSets(DATA.workouts[k])>0); }

// Merge is intentionally conservative: routines are unioned and, when two
// copies contain the same day, the copy with more logged sets wins. Ties stay
// local so a tap made on this device is never silently discarded.
function mergeData(local, remote){
  if(!remote) return local;
  const out = JSON.parse(JSON.stringify(remote));
  out.settings = local.settings || remote.settings;
  const byId = {};
  (remote.routines||[]).forEach(r=>byId[r.id]=r);
  (local.routines||[]).forEach(r=>byId[r.id]=r);
  const merged = Object.values(byId);
  if(merged.length) out.routines = merged;
  out.lastRoutineId = local.lastRoutineId || remote.lastRoutineId;
  delete out.templates;
  out.workouts ||= {};
  Object.keys(local.workouts||{}).forEach(k=>{
    const r = out.workouts[k];
    if(!r || filledSets(local.workouts[k]) >= filledSets(r)) out.workouts[k] = local.workouts[k];
  });
  return out;
}

function ensureMayLeanRoutine(){
  ensureRoutines();
  if(DATA.routines.some(r=>r.id==="maylean2027" || r.name==="May Lean — Full Body")) return false;
  DATA.routines.push({
    id:"maylean2027", name:"May Lean — Full Body", exercises:[
      {name:"Barbell Chest Press", weight:16, sets:3, targetReps:8, bodyweight:false},
      {name:"Lat Pulldown", weight:45, sets:3, targetReps:8, bodyweight:false},
      {name:"Leg Press (feet slightly higher)", weight:0, sets:3, targetReps:10, bodyweight:false},
      {name:"Seated Hip Abduction", weight:0, sets:3, targetReps:12, bodyweight:false},
      {name:"Lateral Raises", weight:10, sets:3, targetReps:12, bodyweight:false},
      {name:"Seated Dumbbell Curls", weight:16, sets:2, targetReps:6, bodyweight:false},
      {name:"Overhead Dumbbell Tricep Extensions", weight:10, sets:2, targetReps:8, bodyweight:false}
    ]
  });
  persistLocal();
  dirty = true; store.set("wt_dirty", true);
  return true;
}

function relTime(ts){
  const sec = Math.floor((Date.now()-ts)/1000);
  if(sec<60) return "just now";
  if(sec<3600) return Math.floor(sec/60)+" min ago";
  if(sec<86400) return Math.floor(sec/3600)+" h ago";
  return shortDate(keyOf(new Date(ts)));
}
function cloudError(msg){
  const e = el("cloudError");
  if(!e) return;
  if(msg){ e.textContent=msg; e.style.display=""; }
  else { e.textContent=""; e.style.display="none"; }
}
function renderCloud(){
  const connected=el("cloudConnected"), setup=el("cloudSetup"), status=el("cloudStatus");
  if(!connected || !setup) return;
  if(!SB){
    connected.style.display="none"; setup.style.display="";
    cloudError("Cloud sync library could not load. Your workout log is still safe on this device.");
    return;
  }
  if(CLOUD_USER){
    connected.style.display=""; setup.style.display="none";
    cloudError(null);
    const who = CLOUD_USER.email ? " · "+escapeHtml(CLOUD_USER.email) : "";
    if(cloudBusy) status.innerHTML=`<span class="sync-dot"></span> Syncing${who}…`;
    else if(lastSyncError) status.innerHTML=`<span class="sync-dot off"></span> Cloud sync issue — your log is safe on this device and will retry${who}.`;
    else if(dirty) status.innerHTML=`<span class="sync-dot"></span> Waiting to sync${who}…`;
    else status.innerHTML=`<span class="sync-dot on"></span> Synced to Strongroom Cloud${who}${lastSync?" · "+relTime(lastSync):""}`;
  } else {
    connected.style.display="none"; setup.style.display="";
  }
}

function scheduleCloudSync(delay){
  clearTimeout(cloudTimer);
  cloudTimer=setTimeout(()=>{ cloudTimer=null; cloudSync(true); }, delay||1800);
}
function scheduleCloudRetry(){
  if(!CLOUD_USER || !dirty) return;
  clearTimeout(cloudRetryTimer);
  cloudRetryTimer=setTimeout(()=>{
    cloudRetryTimer=null;
    if(navigator.onLine!==false) cloudSync(true);
  }, 30000);
}

async function cloudPush(){
  if(!SB || !CLOUD_USER) return false;
  const {error} = await SB.from("strongroom_state").upsert(
    {user_id:CLOUD_USER.id, data:DATA},
    {onConflict:"user_id"}
  );
  if(error) throw error;
  dirty=false; store.set("wt_dirty", false);
  lastSync=Date.now(); store.set("wt_lastsync", lastSync);
  lastSyncError=null;
  // Supabase is now the backup. Remove the old GitHub PAT from this browser
  // only after the first cloud write succeeds.
  store.set("wt_cfg", {owner:"",repo:"",branch:"main",token:""});
  store.set("wt_sha", null);
  return true;
}

async function cloudSync(silent){
  if(!SB || !CLOUD_USER || cloudBusy) return false;
  cloudBusy=true; renderCloud();
  try{
    const localWasDirty=dirty;
    const {data:row,error} = await SB.from("strongroom_state")
      .select("data,updated_at")
      .eq("user_id", CLOUD_USER.id)
      .maybeSingle();
    if(error) throw error;

    if(row && row.data){
      DATA = localWasDirty ? mergeData(DATA, row.data) : row.data;
      ensureRoutines(); ensureMayLeanRoutine();
      persistLocal(); render();
    }

    if(!row || localWasDirty || dirty) await cloudPush();
    else {
      lastSync=Date.now(); store.set("wt_lastsync", lastSync);
      lastSyncError=null;
    }
    clearTimeout(cloudRetryTimer); cloudRetryTimer=null;
    if(!silent) toast("Up to date");
    return true;
  }catch(e){
    lastSyncError=e.message || String(e);
    scheduleCloudRetry();
    if(!silent) toast("Cloud sync failed — saved on this device");
    return false;
  }finally{
    cloudBusy=false; renderCloud();
  }
}

async function cloudAuth(mode){
  cloudError(null);
  if(!SB){ cloudError("Cloud sync is unavailable right now."); return; }
  const email=(el("cloudEmail").value||"").trim();
  const password=el("cloudPassword").value||"";
  if(!email){ cloudError("Enter your email address."); return; }
  if(password.length<6){ cloudError("Use a password of at least 6 characters."); return; }
  const btn = mode==="create" ? el("cloudCreate") : el("cloudSignIn");
  const old=btn.textContent; btn.disabled=true; btn.textContent=mode==="create"?"Creating…":"Signing in…";
  try{
    const res = mode==="create"
      ? await SB.auth.signUp({email,password})
      : await SB.auth.signInWithPassword({email,password});
    if(res.error) throw res.error;
    if(mode==="create" && !res.data.session){
      cloudError("Account created. Check your email to confirm it, then return here and sign in.");
      return;
    }
    CLOUD_USER=res.data.user || (res.data.session&&res.data.session.user) || null;
    renderCloud();
    if(CLOUD_USER) await cloudSync(false);
  }catch(e){
    cloudError(e.message || "Could not sign in.");
  }finally{
    btn.disabled=false; btn.textContent=old;
  }
}

async function initCloud(){
  if(!SB){ renderCloud(); return; }
  try{
    const {data,error}=await SB.auth.getSession();
    if(error) throw error;
    CLOUD_USER=data.session ? data.session.user : null;
  }catch(e){ lastSyncError=e.message || String(e); }
  renderCloud();
  if(CLOUD_USER) await cloudSync(true);
  SB.auth.onAuthStateChange((_event,session)=>{
    CLOUD_USER=session ? session.user : null;
    renderCloud();
    if(CLOUD_USER) setTimeout(()=>cloudSync(true),0);
  });
}

addEventListener("online", ()=>{ if(CLOUD_USER) cloudSync(true); });
document.addEventListener("visibilitychange", ()=>{
  if(document.visibilityState==="visible" && CLOUD_USER) cloudSync(true);
});

'''
replace_between(persist_start, persist_end, persist_new, 'persistence backend')

replace_once(
'el("btnSettings").onclick = ()=>{ renderUnits(); renderBackup(); bkError(null); open("ovSettings"); };',
'el("btnSettings").onclick = ()=>{ renderUnits(); renderCloud(); cloudError(null); open("ovSettings"); };',
'settings open handler'
)

settings_start = 'el("connectBtn").onclick=connectGitHub;\n'
settings_end = 'el("closeSettings").onclick=closeAll;\n'
settings_new = '''el("cloudSignIn").onclick=()=>cloudAuth("signin");
el("cloudCreate").onclick=()=>cloudAuth("create");
el("cloudSyncNow").onclick=async function(){
  this.textContent="Syncing…"; this.disabled=true;
  await cloudSync(false);
  this.textContent="Sync now"; this.disabled=false;
};
el("cloudSignOut").onclick=async()=>{
  if(SB) await SB.auth.signOut();
  CLOUD_USER=null;
  renderCloud();
  toast("Signed out — your log stays on this device");
};
el("closeSettings").onclick=closeAll;
'''
replace_between(settings_start, settings_end, settings_new, 'settings cloud handlers')

boot_old = '''// ---- boot ----
ensureRoutines();   // migrate v1 (flat templates) data into a routine set
render();
renderBackup();
// quietly reconcile and retry any pending local backup on launch
if(isConfigured()){ syncCycle(true); }
'''
boot_new = '''// ---- boot ----
ensureRoutines();   // migrate v1 (flat templates) data into a routine set
ensureMayLeanRoutine();
render();
renderCloud();
initCloud();
'''
replace_once(boot_old, boot_new, 'boot')

p.write_text(s)
print("Strongroom migrated to Supabase cloud sync")
