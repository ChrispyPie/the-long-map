#!/usr/bin/env bash
# The outer world vector layer (data/world/outer.topo.json): Natural Earth 50m land, lakes and rivers inside the
# world bounds (data/world.json "bounds"). Land is clipped OUTSIDE the Near East box that data/base.topo.json
# already draws, so the two land layers meet without overlap or a straight cut. Rivers and lakes are NOT erased
# by that box — the base layer only has a hand-picked set, and erasing the box used to cut the Rhine, the upper
# Danube, the Nile south of 11°N, and others at a rectangular edge. Instead we subtract the geometries (and
# names, for lakes) already in the base layer, so those courses stay continuous and are not drawn twice.
# Also writes the unclipped outer land used as the relief coast mask.
# Needs: mapshaper (npm i mapshaper), Natural Earth 50m geojson in $NE (ne_50m_land.json, ne_50m_lakes.json,
# ne_50m_rivers_lake_centerlines.json; https://www.naturalearthdata.com, public domain).
set -euo pipefail
NE=${NE:-/workspace/tlm-world/ne}; WORK=${TLM_TERRAIN_WORK:-/workspace/tlm-terrain/work}; M=${MAPSHAPER:-mapshaper}
ROOT=$(cd "$(dirname "$0")/../.." && pwd); T=$(mktemp -d)
WORLD=-20,-2,95,66; NEAR=-12,2,88,58
cleanup(){ rm -rf "$T"; }; trap cleanup EXIT

$M -i $NE/ne_50m_land.json -clip bbox=$WORLD -erase bbox=$NEAR -filter-fields -rename-layers land -o format=geojson $T/land.json

$M -i $ROOT/data/base.topo.json -drop target=land,lakes -o format=geojson $T/base_rivers.json
$M -i $ROOT/data/base.topo.json -drop target=land,rivers -o format=geojson $T/base_lakes.json
# 8 km buffer covers the difference between the 10 m base rivers and the 50 m world set
$M -i $T/base_rivers.json -buffer 8km -o format=geojson $T/base_rivers_buf.json
$M -i $T/base_lakes.json -buffer 5km -o format=geojson $T/base_lakes_buf.json

# lakes already drawn in the base (10 m vs 50 m shapes often miss a clean erase)
python3 - "$T/base_lakes.json" "$T/lake_filter.txt" << 'PY'
import json, sys
lakes = json.load(open(sys.argv[1]))
feats = lakes.get("features") or [lakes]
names = sorted({(f.get("properties") or {}).get("name") for f in feats if (f.get("properties") or {}).get("name")})
open(sys.argv[2], "w").write(json.dumps(names) + ".indexOf(name) === -1")
PY

# rivers: whole world bounds, no canals, minus the base courses (continuations under other names remain)
$M -i $NE/ne_50m_rivers_lake_centerlines.json -clip bbox=$WORLD \
  -filter 'name === null || !/canal|csatorna/i.test(name)' \
  -erase $T/base_rivers_buf.json \
  -filter-fields name -rename-layers rivers -o format=geojson $T/rivers.json

$M -i $NE/ne_50m_lakes.json -clip bbox=$WORLD \
  -filter "$(cat $T/lake_filter.txt)" \
  -erase $T/base_lakes_buf.json \
  -filter-fields name -rename-layers lakes -o format=geojson $T/lakes.json

mkdir -p $ROOT/data/world
$M -i $T/land.json $T/lakes.json $T/rivers.json combine-files -rename-layers land,lakes,rivers \
  -o format=topojson quantization=40000 $ROOT/data/world/outer.topo.json

mkdir -p $WORK
$M -i $NE/ne_50m_land.json -clip bbox=-80,-60,170,85 -erase bbox=$NEAR -filter-fields -rename-layers land -o format=topojson $WORK/mask_outer.topo.json
