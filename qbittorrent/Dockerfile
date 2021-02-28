FROM scratch

RUN \
 echo "THEMEPARK :: INFO :: Installing svn package" && \
 apt-get update && \
 apt-get install -y \
	subversion

# copy local files
COPY root/ /