#!/bin/bash

shopt -s extglob

# Assume the only other file in this directory besides this shell
# script and color-mesh.conf is the FMV file we want to run the pipeline on
fmv_file=$(find . -type f ! -name "*.sh" ! -name "*.conf")
echo "$fmv_file"

echo "track-features"
kwiver track-features "$fmv_file"
echo "init-cameras-landmarks"
kwiver init-cameras-landmarks -v "$fmv_file" -t results/tracks.txt
echo "estimate-depth"
kwiver estimate-depth "$fmv_file"
echo "fuse-depth"
kwiver fuse-depth results/krtd results/depth --input-geo-origin-file results/geo_origin.txt --output-mesh-file results/mesh.vtp
echo "color-mesh"
kwiver color-mesh --config input/color-mesh.conf --input-geo-origin-file results/geo_origin.txt results/mesh.vtp "$fmv_file" results/krtd results/pc.las

mkdir -p output/
mv results/ output/
mv $fmv_file output/
