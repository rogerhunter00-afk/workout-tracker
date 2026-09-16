from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Use one definition everywhere: a set is logged only when it contains a real,
# positive numeric rep count. This deliberately excludes null, undefined,
# blank strings, zero and malformed placeholder values.
anchor = 'function filledSets(wk){'
assert s.count(anchor) == 1, f'filledSets anchor count {s.count(anchor)}'
s = s.replace(anchor, 'function isLoggedRep(v){ return typeof v==="number" && Number.isFinite(v) && v>0; }\n' + anchor, 1)

# Normalise every completion/history predicate to the same rule. This covers
# session progress, report generation, history filtering and calendar markers.
filter_old = 'filter(v=>v!==null)'
some_old = 'some(v=>v!==null)'
assert s.count(filter_old) >= 1, 'No old filter predicates found'
assert s.count(some_old) >= 1, 'No old some predicates found'
s = s.replace(filter_old, 'filter(isLoggedRep)')
s = s.replace(some_old, 'some(isLoggedRep)')

# An empty/undefined slot must render as a dash in copied day summaries too.
old = 'ex.sets.map(v=>v===null?"–":v)'
new = 'ex.sets.map(v=>isLoggedRep(v)?v:"–")'
assert s.count(old) == 1, f'set display anchor count {s.count(old)}'
s = s.replace(old, new, 1)

p.write_text(s)
print('Unified logged-set detection for UI, reports and calendar')
