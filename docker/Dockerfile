FROM ghcr.io/linuxserver/baseimage-alpine-nginx:3.14

LABEL maintainer="Roxedus"

COPY / /themepark

RUN \
echo " ## Installing packages ## " && \
apk add --no-cache --virtual=build-dependencies \
    python3 


# RUN mkdir -p /usr/share/nginx/html/css/ 
# RUN mkdir -p /usr/share/nginx/html/resources/ 
# RUN cp -R css/  /usr/share/nginx/html/css/ 
# RUN cp -R resources/ /usr/share/nginx/html/resources/ 
# RUN cp index.html /usr/share/nginx/html/index.html 
#rm -rf /themepark