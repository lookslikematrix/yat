#!/bin/bash
set -e

CHANGED_FILES=$(git diff --name-only ${TARGET_BRANCH:-origin/main}...HEAD)
echo "[ $CHANGED_FILES | main ] 🔎 Changed files:"
/.yat/venv/bin/pre-commit run --files $CHANGED_FILES
