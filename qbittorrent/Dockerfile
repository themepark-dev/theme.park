FROM scratch

RUN \
echo "THEMEPARK :: INFO :: Installing svn package" && \
apt-get update \
apt-get install subversion -y

# copy local files
COPY root/ /