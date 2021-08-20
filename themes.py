from os import listdir
from os.path import isdir, isfile, join
from json import dump,dumps, loads
import subprocess

def get_shas(output):
    """Returns a dict of CSS files and SHAs"""
    output_lines = output.splitlines()
    sha_dict = {}
    for line in output_lines:
        line = line.decode('utf-8').replace("\t","").split(" ")
        sha = line[1]
        css_file = [file for file in line[2].split("/") if "css" in file][0]
        sha_dict.update({css_file: sha})
    return(sha_dict)

def create_addons_json():
    addon_shas = subprocess.check_output(["git", "ls-files", "-s", "./CSS/addons/*.css"])
    SHAS = get_shas(addon_shas)
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
                            "css": [f"https://{DOMAIN}/CSS/addons/{app}/{addon}/{file}?sha={SHAS.get(file)}" for file in files if file.split(".")[1] == "css"]
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
                                        "css": [f"https://{DOMAIN}/CSS/addons/{app}/{addon}/{dir}/{extra_file}?sha={SHAS.get(extra_file)}" for extra_file in extra_dir_files if extra_file.split(".")[1] == "css"]
                                    } for dir in extra_dirs
                                }
                            })
    return dumps(ADDONS)

def create_json(app_folders:list=None,themes:list=None,no_sub_folders=False):
    if no_sub_folders:
        THEMES = {}
        theme_shas = subprocess.check_output(["git", "ls-files", "-s", "./CSS/variables/*.css"])
        SHAS = get_shas(theme_shas)
        for theme in themes:
            THEMES.update({
                "themes": {
                    theme.split(".")[0].capitalize(): {
                        "url": f"https://{DOMAIN}/CSS/variables/{theme}?sha={SHAS.get(theme)}" 
                    }for theme in themes
                }
            })
        return dumps(THEMES)
    else:
        ADDONS = loads(create_addons_json())
        APPS = {"applications":{}}
        app_shas = subprocess.check_output(["git", "ls-files", "-s", "./CSS/themes/*base.css"])
        SHAS = get_shas(app_shas)
        for app in app_folders:
            APPS.update({
                "applications":{
                    app: {
                        "base_css": f"https://{DOMAIN}/CSS/themes/{app}/{app}-base.css?sha={SHAS.get(f'{app}-base.css')}",
                        "addons": ADDONS["addons"][app] if app in ADDONS["addons"] else {}
                        } for app in app_folders
                    }
                }
            )
        THEMES = loads(create_json(themes=themes,no_sub_folders=True))
        APPS.update(ADDONS)
        APPS.update(THEMES)
        return dumps(APPS)

if __name__== "__main__":
    app_folders = [name for name in listdir('./CSS/themes') if isdir(join('./CSS/themes', name))]
    themes = [name for name in listdir('./CSS/variables') if isfile(join('./CSS/variables', name))]
    DOMAIN = open("CNAME","rt",closefd=True).readline()
    apps = loads(create_json(app_folders,themes))

    with open("themes.json", "w") as outfile:
        dump(apps, outfile,indent=2)
