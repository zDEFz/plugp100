#!/bin/bash

PYTHON_VERSION=$1

# TODO: add ARCHITECTURE check as second arguments ARCHITECTURE=$2
if [ "$PYTHON_VERSION" = "py3.9" ]; then
    IMAGE_NAME=arm32v7/python:3.9
    DOCKER_PLATFORM=linux/arm
elif [ "$PYTHON_VERSION" = "py3.10" ]; then
    IMAGE_NAME=arm32v7/python:3.10
    DOCKER_PLATFORM=linux/arm
fi

docker run -d \
    --platform="${DOCKER_PLATFORM}" \
    --workdir "${GITHUB_WORKSPACE}" \
    -e DEBIAN_FRONTEND=noninteractive \
    -e CI \
    -e GITHUB_ACTION \
    -e GITHUB_ACTION_PATH \
    -e GITHUB_ACTIONS \
    -e GITHUB_ACTOR \
    -e GITHUB_API_URL \
    -e GITHUB_BASE_REF \
    -e GITHUB_ENV \
    -e GITHUB_EVENT_NAME \
    -e GITHUB_EVENT_PATH \
    -e GITHUB_GRAPHQL_URL \
    -e GITHUB_HEAD_REF \
    -e GITHUB_JOB \
    -e GITHUB_REF \
    -e GITHUB_REPOSITORY \
    -e GITHUB_RUN_ID \
    -e GITHUB_RUN_NUMBER \
    -e GITHUB_SERVER_URL \
    -e GITHUB_SHA \
    -e GITHUB_WORKFLOW \
    -e GITHUB_WORKSPACE \
    -e RUNNER_OS \
    -e RUNNER_TEMP \
    -e RUNNER_TOOL_CACHE \
    -e RUNNER_WORKSPACE \
    -v "/var/run/docker.sock:/var/run/docker.sock" \
    -v "${EVENT_DIR}:${EVENT_DIR}" \
    -v "${GITHUB_WORKSPACE}:${GITHUB_WORKSPACE}" \
    -v "${ACTION_DIR}:${ACTION_DIR}" \
    $IMAGE_NAME \
    tail -f /etc/passwd >> /dev/null

export PYTHON_CONTAINER=$(docker ps --filter "ancestor=${IMAGE_NAME}" --format {{.Names}})

