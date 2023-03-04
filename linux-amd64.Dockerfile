FROM ghcr.io/linuxserver/baseimage-alpine-nginx:3.16

# set version label
ARG BUILD_DATE
ARG TP_RELEASE
ARG BUILD_ARCHITECTURE
LABEL build_version="Version:- ${TP_RELEASE} Build-date:- ${BUILD_DATE} Platform: ${BUILD_ARCHITECTURE}"
LABEL maintainer="gilbn"

RUN \
echo " ## Installing packages ## " && \
apk add --no-cache --virtual=runtime-dependencies \
    python3 && \
  echo "**** install theme.park ****" && \
    mkdir -p /app/themepark

# copy local files
WORKDIR /app
COPY css/ /app/themepark/css/
COPY resources/ /app/themepark/resources/
COPY docker-mods/ /app/themepark/docker-mods/
COPY themes.py index.html CNAME /app/themepark/

COPY docker/root/ /