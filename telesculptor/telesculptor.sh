#!/bin/bash

shopt -s extglob

source /kwiver/build/setup_KWIVER.sh
# Set up X virtual framebuffer (Xvfb) to support running VTK headless.
# The color-mesh KWIVER applet needs this to work.
Xvfb :1 -screen 0 1024x768x16 -nolisten tcp &
export DISPLAY=:1.0

# Assume the only other file in this directory besides this shell
# script and color-mesh.conf is the FMV file we want to run the pipeline on
fmv_file=$(find . -type f ! -name "*.sh" ! -name "*.conf")
echo "$fmv_file"

echo "track-features"
kwiver track-features "$fmv_file"
echo "init-cameras-landmarks"
kwiver init-cameras-landmarks --video "$fmv_file" --tracks results/tracks.txt --camera results/krtd --landmarks results/landmarks.ply
echo "estimate-depth"
kwiver estimate-depth --input-landmarks-file results/landmarks.ply "$fmv_file" results/krtd results/depth
echo "fuse-depth"
kwiver fuse-depth --input-geo-origin-file results/geo_origin.txt --output-mesh-file results/mesh.vtp results/krtd results/depth
echo "color-mesh"
kwiver color-mesh --config input/color-mesh.conf --input-geo-origin-file results/geo_origin.txt results/mesh.vtp "$fmv_file" results/krtd results/pc.las

mkdir -p output/
mv results/ output/
mv $fmv_file output/
