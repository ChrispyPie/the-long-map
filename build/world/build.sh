#!/usr/bin/env bash
# The outer world vector layer (data/world/outer.topo.json): Natural Earth 50m land, lakes and rivers inside the
# world bounds (data/world.json "bounds") but OUTSIDE the Near East box that data/base.topo.json already draws,
# so the two layers meet without overlap. Also writes the unclipped outer land used as the relief coast mask.
# Needs: mapshaper (npm i mapshaper), Natural Earth 50m geojson in $NE (ne_50m_land.json, ne_50m_lakes.json,
# ne_50m_rivers_lake_centerlines.json; https://www.naturalearthdata.com, public domain).
set -euo pipefail
NE=${NE:-/workspace/tlm-world/ne}; WORK=${TLM_TERRAIN_WORK:-/workspace/tlm-terrain/work}; M=${MAPSHAPER:-mapshaper}
ROOT=$(cd "$(dirname "$0")/../.." && pwd); T=$(mktemp -d)
WORLD=-20,-2,95,66; NEAR=-12,2,88,58
$M -i $NE/ne_50m_land.json -clip bbox=$WORLD -erase bbox=$NEAR -filter-fields -rename-layers land -o format=geojson $T/land.json
$M -i $NE/ne_50m_lakes.json -clip bbox=$WORLD -erase bbox=$NEAR -filter-fields name -rename-layers lakes -o format=geojson $T/lakes.json
$M -i $NE/ne_50m_rivers_lake_centerlines.json -clip bbox=$WORLD -erase bbox=$NEAR -filter-fields name -rename-layers rivers -o format=geojson $T/rivers.json
mkdir -p $ROOT/data/world
$M -i $T/land.json $T/lakes.json $T/rivers.json combine-files -rename-layers land,lakes,rivers -o format=topojson quantization=40000 $ROOT/data/world/outer.topo.json
mkdir -p $WORK
$M -i $NE/ne_50m_land.json -clip bbox=-80,-60,170,85 -erase bbox=$NEAR -filter-fields -rename-layers land -o format=topojson $WORK/mask_outer.topo.json
rm -rf $T
