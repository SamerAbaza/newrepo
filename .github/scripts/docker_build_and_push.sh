#!/usr/bin/env bash

set -e

export IMAGE_NAME="${REGISTRY}/${REPOSITORY}/${BRANCH_REF}"

# Build and push
docker build $(./ci_helpers/get_docker_build_args.sh ${IMAGE_FOLDER}) -f ${DOCKERFILE:="./Dockerfile"} -t ${IMAGE_NAME}:${IMAGE_TAG} .
docker push ${IMAGE_NAME}:${IMAGE_TAG}

# Push with alternative tag if present
if [ -n "${ALTERNATIVE_TAG}" ]; then
  docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:${ALTERNATIVE_TAG}
  docker push ${IMAGE_NAME}:${ALTERNATIVE_TAG}
fi

docker logout https://${REGISTRY}