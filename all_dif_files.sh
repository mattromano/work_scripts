#!/bin/bash

# Fetch the latest changes from the remote main branch
git fetch origin main

# List changed files between the current branch and main
# Filter for .sql files
git diff --name-only main | grep -E '\.sql$' | tr '\n' ' '| xargs
