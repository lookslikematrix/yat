#!/bin/bash
set -e

echo "🔥 YaT - Yet another Template"
echo "🔬 Software Composition Analysis"

SOURCE_DIRECTORY=${SOURCE_DIRECTORY:-$PWD}
cd $SOURCE_DIRECTORY
echo "[ $SOURCE_DIRECTORY ] We are here."

if [ -f "pyproject.toml" ]; then
    /.yat/venv/bin/cyclonedx-py poetry --output-file cyclonedx.json
fi
