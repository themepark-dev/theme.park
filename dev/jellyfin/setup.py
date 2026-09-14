"""Configure the disposable Compose instance and its synthetic movie library."""
import json
import os
from urllib.request import Request, urlopen

USERNAME = os.environ.get('JELLYFIN_DEV_USER', 'admin')
PASSWORD = os.environ.get('JELLYFIN_DEV_PASSWORD', 'admin')

BASE = 'http://localhost:18086'
AUTHORIZATION = 'MediaBrowser Client="themepark-dev", Device="Local fixture", DeviceId="themepark-jellyfin-dev", Version="1.0"'


def request(path, data=None, method=None):
    headers = {'Content-Type': 'application/json', 'Authorization': AUTHORIZATION}
    payload = json.dumps(data).encode() if data is not None else None
    with urlopen(Request(BASE + path, data=payload, headers=headers, method=method)) as response:
        content = response.read()
        return json.loads(content) if content else None


if not request('/System/Info/Public')['StartupWizardCompleted']:
    request('/Startup/Configuration', {
        'ServerName': 'theme.park preview', 'UICulture': 'en-US',
        'MetadataCountryCode': 'US', 'PreferredMetadataLanguage': 'en',
    })
    request('/Startup/User', {'Name': USERNAME, 'Password': PASSWORD})
    request('/Startup/RemoteAccess', {'EnableRemoteAccess': True, 'EnableAutomaticPortMapping': False})
    request('/Startup/Complete', {}, 'POST')

session = request('/Users/AuthenticateByName', {'Username': USERNAME, 'Pw': PASSWORD})
AUTHORIZATION = 'MediaBrowser Token="' + session['AccessToken'] + '"'
if not any(library['Name'] == 'Sample Movies' for library in request('/Library/VirtualFolders')):
    request('/Library/VirtualFolders?name=Sample%20Movies&collectionType=movies&refreshLibrary=true', {
        'LibraryOptions': {
            'PathInfos': [{'Path': '/media/Movies'}], 'EnableRealtimeMonitor': False,
            'EnableInternetProviders': False,
            'TypeOptions': [{'Type': 'Movie', 'MetadataFetchers': [], 'ImageFetchers': []}],
        },
    }, 'POST')

branding = request('/System/Configuration/branding')
if not branding.get('CustomCss'):
    branding['CustomCss'] = (
        '@import url("http://localhost:18869/css/base/jellyfin/jellyfin-base.css");\n'
        '@import url("http://localhost:18869/css/theme-options/aquamarine.css");'
    )
    branding['SplashscreenEnabled'] = False
    request('/System/Configuration/branding', branding, 'POST')
print('Local fixture ready at ' + BASE + '/web/. User: ' + USERNAME)
