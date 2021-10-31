from os import listdir
from os.path import isdir, isfile, join
from json import dump, dumps, loads
import subprocess
import shutil

def get_shas(output):
    """Returns a dict of CSS files and SHAs"""
    output_lines = output.splitlines()
    sha_dict = {}
    for line in output_lines:
        line = line.decode('utf-8').replace("0\t", "").split(" ")
        sha = line[1]
        css_file = [file for file in line[2].split("/") if "css" in file][-1]
        sha_dict.update({css_file: sha})
    return(sha_dict)


def create_addons_json():
    addon_shas = subprocess.check_output(
        ["git", "ls-files", "-s", "./css/addons/*.css"])
    SHAS = get_shas(addon_shas)
    ADDONS = {"addons": {}}
    addon_root = './css/addons'
    addon_folders = [name for name in listdir(
        addon_root) if isdir(join(addon_root, name))]
    for app in addon_folders:
        app_addons = [addon for addon in listdir(f"{addon_root}/{app}")]
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
                    "css":  [f"https://{DOMAIN}/css/addons/{app}/{addon}/{file}?sha={SHAS.get(file)}" for file in files if file.split(".")[1] == "css"]
                }
                )
            else:
                ADDONS["addons"][app].update({
                    addon:  f"https://{DOMAIN}/css/addons/{app}/{addon}/{file}?sha={SHAS.get(file)}" for file in files if file.split(".")[1] == "css"
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
                            "css": [f"https://{DOMAIN}/css/addons/{app}/{addon}/{dir}/{extra_file}?sha={SHAS.get(extra_file)}" for extra_file in extra_dir_files if extra_file.split(".")[1] == "css"]
                        }
                    }
                    )
    return dumps(ADDONS, sort_keys=True)


def create_json(app_folders: list = None, themes: list = None, community_themes: list = None, no_sub_folders=False):
    if no_sub_folders:
        THEMES_DICT = {}
        theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/theme-options/*.css"])
        community_theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/community-theme-options/*.css"])
        THEME_SHAS = get_shas(theme_shas)
        COMMUNITY_THEME_SHAS = get_shas(community_theme_shas)
        THEMES = {
                theme.split(".")[0].capitalize(): {
                    "url": f"https://{DOMAIN}/css/theme-options/{theme}?sha={THEME_SHAS.get(theme)}"
                }for theme in themes
            }
        COMMUNITY_THEMES = {
                theme.split(".")[0].capitalize(): {
                    "url": f"https://{DOMAIN}/css/community-theme-options/{theme}?sha={COMMUNITY_THEME_SHAS.get(theme)}"
                }for theme in community_themes
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
        APPS = {"applications": {}}
        app_shas = subprocess.check_output(["git", "ls-files", "-s", "./css/base/*base.css"])
        SHAS = get_shas(app_shas)
        APPS.update(dict(sorted({
            "applications": {
                app: {
                    "base_css": f"https://{DOMAIN}/css/base/{app}/{app}-base.css?sha={SHAS.get(f'{app}-base.css')}",
                    "addons": ADDONS["addons"][app] if app in ADDONS["addons"] else {}
                } for app in app_folders if not isfile(f'./css/base/{app}/.deprecated')
            }
        }.items())))
        THEMES = loads(create_json(themes=themes, community_themes=community_themes, no_sub_folders=True))
        APPS.update(ADDONS)
        APPS.update(THEMES)
        return dumps(APPS)

def temporary_copy_files():
    shutil.rmtree("./CSS", ignore_errors=True)
    shutil.rmtree("./Resources", ignore_errors=True)
    src_dst = {
        "./css/base/": "./CSS/themes",
        "./css/theme-options": "./CSS/variables",
        "./css/community-theme-options": "./CSS/variables",
        "./resources/": "./Resources/",
        "./css/addons/": "./CSS/addons",
        "./css/defaults/": "./CSS/defaults",
        "./css/theme-options/organizr.css": "./CSS/variables/organizr-dark.css"
    }
    for src in src_dst:
        if ".css" in src:
            shutil.copy(src,src_dst[src])
            continue
        shutil.copytree(src,src_dst[src],dirs_exist_ok=True)

if __name__ == "__main__":
    app_folders = [name for name in listdir('./css/base') if isdir(join('./css/base', name))]
    themes = [name for name in listdir('./css/theme-options') if isfile(join('./css/theme-options', name))]
    community_themes = [name for name in listdir('./css/community-theme-options') if isfile(join('./css/community-theme-options', name))]
    with open("CNAME", "rt", closefd=True) as cname:
        DOMAIN= cname.readline()
    apps = loads(create_json(app_folders=app_folders, themes=themes, community_themes=community_themes))
    with open("themes.json", "w") as outfile:
        dump(apps, outfile, indent=2, sort_keys=True)
    temporary_copy_files()