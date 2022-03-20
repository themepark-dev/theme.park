FROM ghcr.io/linuxserver/baseimage-alpine-nginx:3.14

# set version label
ARG BUILD_DATE
ARG TP_RELEASE
LABEL build_version="Version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="gilbn"

RUN \
echo " ## Installing packages ## " && \
apk add --no-cache --virtual=build-dependencies \
    curl && \
  echo "**** install theme.park ****" && \
    mkdir -p /app/themepark && \
  if [ -z ${TP_RELEASE+x} ]; then \
    TP_RELEASE=$(curl -sX GET "https://api.github.com/repos/gilbn/theme.park/releases/latest" \
    | awk '/tag_name/{print $4;exit}' FS='[""]'); \
  fi && \
  curl -o \
    /tmp/themepark.tar.gz -L \
    "https://github.com/GilbN/theme.park/archive/refs/tags/${TP_RELEASE}.tar.gz" && \
    tar xf \
    /tmp/themepark.tar.gz -C \
      /app/themepark/ --strip-components=1 && \
  cd /app/themepark && \
  echo "**** cleanup ****" && \
  apk del --purge \
    build-dependencies && \
  rm -rf \
    /root/.cache \
    /tmp/* \
    /app/themepark/docker-mods \
    /app/themepark/resources/organizr

# copy local files
COPY root/ /
