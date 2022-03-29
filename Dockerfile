FROM ghcr.io/linuxserver/baseimage-alpine-nginx:3.14

# set version label
ARG BUILD_DATE
ARG TP_RELEASE
LABEL build_version="Version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="gilbn"

RUN \
echo " ## Installing packages ## " && \
apk add --no-cache --virtual=build-dependencies \
    python3 && \
  echo "**** install theme.park ****" && \
    mkdir -p /app/themepark

# copy local files
WORKDIR /app
COPY css/ /app/themepark/css/
COPY resources/ /app/themepark/resources/
COPY themes.py index.html CNAME /app/themepark/

COPY docker/root/ /