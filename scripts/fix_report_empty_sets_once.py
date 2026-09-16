from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Treat only actual positive numeric rep values as logged. Blank/undefined/null
# values can render identically in the UI, but must never count in reports.
old = '''function filledSets(wk){ return wk.exercises.reduce((a,ex)=>a+ex.sets.filter(v=>v!==null).length,0); }\nfunction hasLocalLog(){ return Object.keys(DATA.workouts).some(k=>filledSets(DATA.workouts[k])>0); }'''
new = '''function isLoggedRep(v){ return typeof v==="number" && Number.isFinite(v) && v>0; }\nfunction filledSets(wk){ return wk.exercises.reduce((a,ex)=>a+ex.sets.filter(isLoggedRep).length,0); }\nfunction hasLocalLog(){ return Object.keys(DATA.workouts).some(k=>filledSets(DATA.workouts[k])>0); }'''
assert s.count(old) == 1, f'filledSets anchor count {s.count(old)}'
s = s.replace(old, new, 1)

# Day summary: only real reps count as completed, and non-rep placeholders print as dash.
old = '''    const done = ex.sets.filter(v=>v!==null);\n    const reps = done.reduce((a,b)=>a+b,0);'''
new = '''    const done = ex.sets.filter(isLoggedRep);\n    const reps = done.reduce((a,b)=>a+b,0);'''
# Occurs in summariseDay and per-exercise report history.
assert s.count(old) == 2, f'done-filter anchor count {s.count(old)}'
s = s.replace(old, new)

old = '''    const setStr = ex.sets.length ? ex.sets.map(v=>v===null?"–":v).join(" ") : "—";'''
new = '''    const setStr = ex.sets.length ? ex.sets.map(v=>isLoggedRep(v)?v:"–").join(" ") : "—";'''
assert s.count(old) == 1, f'setStr anchor count {s.count(old)}'
s = s.replace(old, new, 1)

# Full-history session filter: untouched template days must not appear at all.
old = '''    return wk.exercises.some(ex=>ex.sets.some(v=>v!==null));'''
new = '''    return wk.exercises.some(ex=>ex.sets.some(isLoggedRep));'''
# One occurrence in buildReport and one in calendar. Both should use the same
# definition of a genuinely logged workout day.
assert s.count(old) == 2, f'logged-day anchor count {s.count(old)}'
s = s.replace(old, new)

p.write_text(s)
print('Hardened report/session logging against blank and undefined set values')
