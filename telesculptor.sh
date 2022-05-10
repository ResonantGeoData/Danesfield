#!/bin/bash

shopt -s extglob

# Assume the only other file in this directory besides this shell
# script is the FMV file we want to run the pipeline on
fmv_file=$(find . -type f ! -name "*.sh")

kwiver track-features "$fmv_file"
kwiver init-cameras-landmarks -v "$fmv_file" -t results/tracks.txt
kwiver estimate-depth "$fmv_file"
kwiver fuse-depth results/krtd results/depth --output-mesh-file results/mesh.vtp
kwiver color-mesh --input-geo-origin-file results/geo_origin.txt results/mesh.vtp "$fmv_file" results/krtd output/pc.las
