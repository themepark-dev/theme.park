FROM scratch

RUN \
echo "::theme.park:: Installing svn package" && \
apt-get update \
apt-get install subversion

# copy local files
COPY root/ /