#!/bin/bash
set -e

echo "🔥 YaT - Yet another Template"
yq .name /.yat/yat.yml

SBOM_OUTPUT_PATH=""
if [ -n "$YAT_OUTPUT_DIRECTORY" ]; then
    SBOM_OUTPUT_PATH=$YAT_OUTPUT_DIRECTORY/${YAT_RELEASE_NAME}_${YAT_RELEASE_VERSION}.cyclondx.json
else
    SBOM_OUTPUT_PATH=$PWD/${YAT_RELEASE_NAME}_${YAT_RELEASE_VERSION}.cyclondx.json
fi

SOURCE_DIRECTORY=${SOURCE_DIRECTORY:-$PWD}
cd $SOURCE_DIRECTORY
echo "[ $SOURCE_DIRECTORY ] We are here."

echo "[ $SBOM_OUTPUT_PATH ] Create software bill of material (SBOM) here."

if [ -f "pyproject.toml" ]; then
    /.yat/venv/bin/cyclonedx-py poetry --output-file $SBOM_OUTPUT_PATH
fi
