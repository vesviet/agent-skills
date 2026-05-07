#!/usr/bin/env bash

# Optional helper for skills that need to talk to a dev cluster or remote shell.
# Customize these defaults for your own environment after installing the pack.

export DEV_USER="${DEV_USER:-developer}"
export DEV_HOST="${DEV_HOST:-dev.example.internal}"
export DEV_PORT="${DEV_PORT:-22}"
export DEV_SSH="ssh ${DEV_USER}@${DEV_HOST} -p ${DEV_PORT}"
