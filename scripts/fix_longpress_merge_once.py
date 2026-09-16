from pathlib import Path

p = Path('index.html')
s = p.read_text()
old = '''// Merge is intentionally conservative: routines are unioned and, when two
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
'''
new = '''// Merge keeps remote-only days/routines, but any locally edited day wins in
// full. A pending local edit may deliberately REMOVE a logged set (long-press),
// so comparing filled-set counts would incorrectly resurrect deleted reps.
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
  // `mergeData` is only used when this device has unsynced local changes.
  // Therefore every local version of a date is authoritative, including a
  // lower filled-set count caused by intentionally clearing a set.
  Object.keys(local.workouts||{}).forEach(k=>{
    out.workouts[k] = local.workouts[k];
  });
  return out;
}
'''
if s.count(old) != 1:
    raise SystemExit(f'Expected merge block once, found {s.count(old)}')
s = s.replace(old,new,1)
p.write_text(s)
print('Patched long-press/cloud merge semantics')
