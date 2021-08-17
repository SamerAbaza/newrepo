#!/usr/bin/env bash

BUILD_ARGS="--build-arg CODE_SOURCE=$1"
if [ -f "$1/build.args" ]; then
  for line in $(cat "${1}/build.args")
    do
      BUILD_ARGS+=" --build-arg $line"
    done
fi
echo "$BUILD_ARGS"

# export DOCKER_BUILDKIT=1
# eval $(ssh-agent)
# ssh-add;
#
# docker build --ssh default $BUILD_ARGS -f ./Dockerfile -t "${1//_/-}" .