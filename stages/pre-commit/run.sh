#!/bin/bash
set -e

echo "🔥 YaT - Yet another Template"
echo "🔶 pre-commit"

echo "[ $PWD ] We are here."

CHANGED_FILES=$(git diff --name-only ${TARGET_BRANCH:-origin/main}...HEAD)
echo "[ $CHANGED_FILES | $TARGET_BRANCH ] 🔎 Changed files related to target branch:"
/.yat/venv/bin/pre-commit run --files $CHANGED_FILES
