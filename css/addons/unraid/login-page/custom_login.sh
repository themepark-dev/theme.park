#!/bin/bash
TYPE="retro-terminal"
THEME="green.css"
DOMAIN="theme-park.dev" # If you update the domain after the script has been run, You must disable and re enable JS or the whole theme.
SCHEME="https"
ADD_JS="true"
JS="custom_text_header.js"
DISABLE_THEME="false"

echo -e "Variables set:\\n\
TYPE          = ${TYPE}\\n\
THEME         = ${THEME}\\n\
DOMAIN        = ${DOMAIN}\\n\
SCHEME        = ${SCHEME}\\n\
ADD_JS        = ${ADD_JS}\\n\
JS            = ${JS}\\n\
DISABLE_THEME = ${DISABLE_THEME}\\n"

IFS='"'
set $(cat /etc/unraid-version)
UNRAID_VERSION="$2"
IFS=$' \t\n'
LOGIN_PAGE="/usr/local/emhttp/login.php"
# Changing file path to login.php if version >= 6.10
if [[ "${UNRAID_VERSION}" =~ ^6.10.* ]]; then
echo "Unraid version: ${UNRAID_VERSION}, changing path to login page"
LOGIN_PAGE="/usr/local/emhttp/webGui/include/.login.php"
fi

# Restore login.php
if [ ${DISABLE_THEME} = "true" ]; then
  echo "Restoring backup of login.php" 
  cp -p ${LOGIN_PAGE}.backup ${LOGIN_PAGE}
  exit 0
fi

# Backup login page if needed.
if [ ! -f ${LOGIN_PAGE}.backup ]; then
  echo "Creating backup of login.php" 
  cp -p ${LOGIN_PAGE} ${LOGIN_PAGE}.backup
fi

# Use correct domain style
case ${DOMAIN} in
  *"github.io"*)
  echo "Switching to github.io URL style"
    DOMAIN="${DOMAIN}\/theme.park"
    ;;
esac

# Adding stylesheets
if ! grep -q ${DOMAIN} ${LOGIN_PAGE}; then
  echo "Adding stylesheet"
  sed -i -e "\@<style>@i\    <link data-tp='theme' rel='stylesheet' href='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/${THEME}'>" ${LOGIN_PAGE}
  sed -i -e "\@<style>@i\    <link data-tp='base' rel='stylesheet' href='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/${TYPE}-base.css'>" ${LOGIN_PAGE}
  echo 'Stylesheet set to' ${THEME}
fi

# Adding/Removing javascript
if [ ${ADD_JS} = "true" ]; then
  if ! grep -q ${JS} ${LOGIN_PAGE}; then
    if grep -q "<script type='text/javascript' src='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/" ${LOGIN_PAGE}; then
      echo "Replacing Javascript"
      sed -i "/<script type='text\/javascript' src='${SCHEME}:\/\/${DOMAIN}\/css\/addons\/unraid\/login-page/c <script type='text/javascript' src='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/js/${JS}'></script>" ${LOGIN_PAGE}
    else
      echo "Adding javascript"
      sed -i -e "\@</body>@i\    <script type='text/javascript' src='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/js/${JS}'></script>" ${LOGIN_PAGE}
    fi
  fi
else
  if grep -q ${JS} ${LOGIN_PAGE}; then
    echo "Removing javascript.."
    sed -i "/<script type='text\/javascript' src='${SCHEME}:\/\/${DOMAIN}\/css\/addons\/unraid\/login-page/d" ${LOGIN_PAGE}
  fi
fi

# Changing stylesheet
if ! grep -q ${TYPE}/${THEME} ${LOGIN_PAGE}; then
  echo "Changing existing custom stylesheet.." 
  sed -i "/<link data-tp='theme' rel='stylesheet' href='${SCHEME}:\/\/${DOMAIN}\/css\/addons\/unraid\/login-page/c <link data-tp='theme' rel='stylesheet' href='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/${THEME}'>" ${LOGIN_PAGE}
  sed -i "/<link data-tp='base' rel='stylesheet' href='${SCHEME}:\/\/${DOMAIN}\/css\/addons\/unraid\/login-page/c <link data-tp='base' rel='stylesheet' href='${SCHEME}://${DOMAIN}/css/addons/unraid/login-page/${TYPE}/${TYPE}-base.css'>" ${LOGIN_PAGE}
  echo 'Stylesheet set to' ${THEME}
fi
