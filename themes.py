from os import listdir
from os.path import isdir, isfile, join
from json import dump,dumps, loads
import argparse

def create_addons_json(sha):
    ADDONS = {"addons":{}}
    addon_root = './CSS/addons'
    addon_folders = [name for name in listdir(addon_root) if isdir(join(addon_root, name))]
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
            ADDONS["addons"].update({
                    app: {
                        addon: {
                            "css": [f"https://{DOMAIN}/CSS/addons/{app}/{addon}/{file}?sha={sha}" for file in files if file.split(".")[1] == "css"]
                        }
                }
            })
            extra_dirs = [dir for dir in listdir(
                f"{addon_root}/{app}/{addon}") if isdir(join(f"{addon_root}/{app}/{addon}", dir))]
            if extra_dirs:
                for dir in extra_dirs:
                    extra_dir_files = [file for file in listdir(
                        f"{addon_root}/{app}/{addon}/{dir}") if isfile(join(f"{addon_root}/{app}/{addon}/{dir}", file))]
                    ADDONS["addons"][app].update({
                                addon: {
                                    dir: {
                                        "css": [f"https://{DOMAIN}/CSS/addons/{app}/{addon}/{dir}/{extra_file}?sha={sha}" for extra_file in extra_dir_files if extra_file.split(".")[1] == "css"]
                                    } for dir in extra_dirs
                                }
                            })
    return dumps(ADDONS)

def create_json(sha,app_folders:list=None,themes:list=None,no_sub_folders=False):
    if no_sub_folders:
        THEMES = {}
        for theme in themes:
            THEMES.update({
                "themes": {
                    theme.split(".")[0].capitalize(): {
                        "url": f"https://{DOMAIN}/CSS/variables/{theme}?sha={sha}" 
                    }for theme in themes
                }
            })
        return dumps(THEMES)
    else:
        ADDONS = loads(create_addons_json(sha))
        APPS = {"applications":{}}
        for app in app_folders:
            APPS.update({
                "applications":{
                    app: {
                        "base_css": f"https://{DOMAIN}/CSS/themes/{app}/{app}-base.css?sha={sha}",
                        "addons": ADDONS["addons"][app] if app in ADDONS["addons"] else {}
                        } for app in app_folders
                    }
                }
            )
        THEMES = loads(create_json(sha,themes=themes,no_sub_folders=True))
        APPS.update(ADDONS)
        APPS.update(THEMES)
        return dumps(APPS)

if __name__== "__main__":

    parser = argparse.ArgumentParser("Creates a JSON file with some information on all applications and themes")
    parser.add_argument("--sha", required=True, help="This is the commit SHA we use for 'versioning' on CSS files")
    args = parser.parse_args()

    sha = args.sha
    app_folders = [name for name in listdir('./CSS/themes') if isdir(join('./CSS/themes', name))]
    themes = [name for name in listdir('./CSS/variables') if isfile(join('./CSS/variables', name))]
    DOMAIN = open("CNAME","rt",closefd=True).readline()
    apps = loads(create_json(sha,app_folders,themes))

    with open("themes.json", "w") as outfile:
        dump(apps, outfile,indent=2)
