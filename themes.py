#! /usr/bin/env python3

from os import defpath, listdir, environ as env, chdir, getcwd
from os.path import isdir, isfile, join, dirname, abspath
from json import dump, dumps, loads, load
import subprocess
from hashlib import md5

chdir(dirname(abspath(__file__))) # Set working dir

def get_shas(output) -> dict[str, str]:
    """Returns a dict of CSS files and SHAs"""
    output_lines = output.splitlines() if output else []
    sha_dict = {}
    for line in output_lines:
        line = line.decode('utf-8').replace("0\t", "").split(" ")
        sha = line[1]
        css_file = [file for file in line[2].split("/") if "css" in file][-1]
        sha_dict.update({css_file: sha})
    return(sha_dict)


def get_md5_hash(file_path) -> str:
    """Returns the MD5 hash of a file"""
    md5_hash = md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def create_addons_json() -> str:
    #addon_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/addons/*.css"]) if isdir(".git") else []
    #SHAS = get_shas(addon_shas)
    ADDONS = {"addons": {}}
    addon_root = './css/addons'
    addon_folders = [name for name in listdir(
        addon_root) if isdir(join(addon_root, name))]
    for app in addon_folders:
        app_addons = [addon for addon in listdir(f"{addon_root}/{app}") if isdir(f"{addon_root}/{app}/{addon}")]
        ADDONS["addons"].update({
            app: {
                addon: {} for addon in app_addons
            }
        })
        for addon in app_addons:
            files = [file for file in listdir(
                f"{addon_root}/{app}/{addon}") if isfile(join(f"{addon_root}/{app}/{addon}", file))]
            if len([f for f in files if f.endswith('.css')]) > 1:
                ADDONS["addons"][app][addon].update({
                    "css":  [f"{scheme}://{DOMAIN}/css/addons/{app}/{addon}/{file}?sha={get_md5_hash(join(getcwd(),'css','addons',app,addon,file))}" for file in files if file.split(".")[1] == "css"]
                }
                )
            else:
                ADDONS["addons"][app].update({
                    addon:  f"{scheme}://{DOMAIN}/css/addons/{app}/{addon}/{file}?sha={get_md5_hash(join(getcwd(),'css','addons',app,addon,file))}" for file in files if file.split(".")[1] == "css"
                }
                )
            extra_dirs = [dir for dir in listdir(
                f"{addon_root}/{app}/{addon}") if isdir(join(f"{addon_root}/{app}/{addon}", dir))]
            if extra_dirs:
                for dir in extra_dirs:
                    extra_dir_files = [file for file in listdir(
                        f"{addon_root}/{app}/{addon}/{dir}") if isfile(join(f"{addon_root}/{app}/{addon}/{dir}", file))]
                    ADDONS["addons"][app][addon].update({
                        dir: {
                            "css": [f"{scheme}://{DOMAIN}/css/addons/{app}/{addon}/{dir}/{extra_file}?sha={get_md5_hash(join(getcwd(),'css','addons',app,addon,dir,extra_file))}" for extra_file in extra_dir_files if extra_file.split(".")[1] == "css"]
                        }
                    }
                    )
    return dumps(ADDONS, sort_keys=True)


def create_json(app_folders: list = None, themes: list = None, community_themes: list = None ,docker_mods: list = None, no_sub_folders=False) -> str:
    if no_sub_folders:
        THEMES_DICT = {}
        #theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/theme-options/*.css"]) if isdir(".git") else []
        #community_theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/community-theme-options/*.css"]) if isdir(".git") else []
        #THEME_SHAS = get_shas(theme_shas)
        #COMMUNITY_THEME_SHAS = get_shas(community_theme_shas)
        THEMES = {
                theme.split(".")[0].capitalize(): {
                    "url": f"{scheme}://{DOMAIN}/css/theme-options/{theme}?sha={get_md5_hash(join(getcwd(),'css','theme-options', theme))}"
                }for theme in themes if themes
            }
        COMMUNITY_THEMES = {
                theme.split(".")[0].capitalize(): {
                    "url": f"{scheme}://{DOMAIN}/css/community-theme-options/{theme}?sha={get_md5_hash(join(getcwd(),'css','community-theme-options', theme))}"
                }for theme in community_themes if community_themes
            }
        THEMES_DICT.update(dict(sorted({
            "themes": {
                **THEMES
                },
            "community-themes": {
                **COMMUNITY_THEMES
                },
            "all-themes": {
                **THEMES, **COMMUNITY_THEMES
                }
            }.items())))
        return dumps(THEMES_DICT)
    else:
        ADDONS = loads(create_addons_json())
        APPS = {}
        #app_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/base/*base.css"]) if isdir(".git") else []
        #SHAS = get_shas(app_shas)
        APPS.update(dict(sorted({
            "applications": {
                app: {
                    "base_css": f"{scheme}://{DOMAIN}/css/base/{app}/{app}-base.css?sha={get_md5_hash(join('css','base', app, f'{app}-base.css'))}",
                    "addons": ADDONS["addons"][app] if app in ADDONS["addons"] else {}
                } for app in app_folders if not isfile(f'./css/base/{app}/.deprecated')
            }
        }.items())))
        APPS.update(dict(sorted({
            "deprecated": {
                app: {
                    "base_css": f"{scheme}://{DOMAIN}/css/base/{app}/{app}-base.css?sha={get_md5_hash(join('css','base', app, f'{app}-base.css'))}",
                    "addons": ADDONS["addons"][app] if app in ADDONS["addons"] else {}
                } for app in app_folders if isfile(f'./css/base/{app}/.deprecated')
            }
        }.items())))
        APPS.update(dict(sorted({
            "docker-mods": {
                mod: f"{scheme}://{DOMAIN}/docker-mods/{mod}/root/etc/cont-init.d/98-themepark" for mod in docker_mods if docker_mods
                 }
        }.items())))
        THEMES = loads(create_json(themes=themes, community_themes=community_themes, no_sub_folders=True))
        APPS.update(ADDONS)
        APPS.update(THEMES)
        return dumps(APPS)

def create_theme_options() -> None:
    #app_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/base/*base.css"]) if isdir(".git") else []
    #theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/theme-options/*.css"]) if isdir(".git") else []
    #community_theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/community-theme-options/*.css"]) if isdir(".git") else []
    #THEME_SHAS = get_shas(theme_shas)
    #COMMUNITY_THEME_SHAS = get_shas(community_theme_shas)
    #APP_SHAS = get_shas(app_shas)
    def create_css(theme, theme_type="standard"):
        folder = "./css/base"
        with open(f"{folder}/{app}/{theme.lower()}.css", "w") as create_app:
            content = f'@import url("/css/base/{app}/{app}-base.css?sha={get_md5_hash(join(getcwd(),"css","base",app,f"{app}-base.css"))}");\n@import url("/css/{"theme-options" if theme_type=="standard" else "community-theme-options"}/{theme.lower()}.css?sha={get_md5_hash(join(getcwd(),"css","theme-options",f"{theme.lower()}.css")) if theme_type=="standard" else get_md5_hash(join(getcwd(),"css","community-theme-options",f"{theme.lower()}.css"))}");'
            create_app.write(content)
    with open("themes.json") as themes:
        data = load(themes)
        themes = data["themes"]
        community_themes = data["community-themes"]
        applications = data["applications"]
    for app in applications:
        for theme in themes:
            create_css(theme)
        for theme in community_themes:
            create_css(theme,theme_type="community")

env_domain = env.get('TP_DOMAIN')
scheme = env.get('TP_SCHEME','https') if env.get('TP_SCHEME') else 'https'

if __name__ == "__main__":
    app_folders = [name for name in listdir('./css/base') if isdir(join('./css/base', name))]
    themes = [name for name in listdir('./css/theme-options') if isfile(join('./css/theme-options', name))]
    docker_mods = [name for name in listdir('./docker-mods')] if isdir('./docker-mods') else []
    community_themes = [name for name in listdir('./css/community-theme-options') if isfile(join('./css/community-theme-options', name))]
    develop = True if isdir(".git") and subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"]).decode('ascii').strip() == "develop" else False
    if env_domain:
        DOMAIN = env_domain
    else:
        with open("CNAME", "rt", closefd=True) as cname:
            CNAME = cname.readline()
        DOMAIN = CNAME if not develop else f"develop.{CNAME}"
    apps = loads(create_json(app_folders=app_folders, themes=themes, community_themes=community_themes, docker_mods=docker_mods))
    with open("themes.json", "w") as outfile:
        dump(apps, outfile, indent=2, sort_keys=True)
    create_theme_options()