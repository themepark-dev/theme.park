from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1] / 'artifacts/jellyfin/724/media'
root.mkdir(parents=True, exist_ok=True)
if not (root/'sample.mp4').exists():
    import subprocess
    subprocess.run(['docker', 'run', '--rm', '--entrypoint', '/usr/lib/jellyfin-ffmpeg/ffmpeg',
                    '-v', f'{root}:/out', 'jellyfin/jellyfin:12.0',
                    '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
                    '-i', 'testsrc2=size=640x360:rate=24', '-f', 'lavfi',
                    '-i', 'sine=frequency=440:sample_rate=48000', '-t', '15',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-y', '/out/sample.mp4'], check=True)
for i,(title,color) in enumerate([('Northern Lights','#186b77'),('The Quiet Orbit','#33386b'),('Glass Coast','#9a5838'),('After the Rain','#356245'),('Signal Blue','#225f95'),('Distant Gardens','#794978')]):
 p=root/'Movies'/f'{title} (2026)';p.mkdir(parents=True,exist_ok=True);shutil.copy(root/'sample.mp4',p/(title+'.mp4'))
 (p/'movie.nfo').write_text(f'<movie><title>{title}</title><year>2026</year><plot>Synthetic sample film for checking theme.park styling. No external media or metadata.</plot><runtime>1</runtime><genre>Adventure</genre><studio>Sample Studio</studio><mpaa>PG</mpaa><lockdata>true</lockdata></movie>')
 for shape,w,h in [('poster',600,900),('backdrop',1280,720)]:
  (p/(shape+'.svg')).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="{color}"/><circle cx="{w*.7}" cy="{h*.32}" r="{w*.32}" fill="#ffffff" opacity=".14"/><path d="M0 {h*.7} L{w*.45} {h*.36} L{w} {h*.85} V{h} H0Z" fill="#071c30" opacity=".6"/><text x="40" y="{h*.76}" fill="white" font-family="sans-serif" font-size="{32 if shape=='poster' else 52}">{title}</text><text x="40" y="{h*.87}" fill="#c8d3df" font-family="sans-serif" font-size="18">THEME.PARK / SAMPLE {i+1:02}</text></svg>''')

import subprocess
subprocess.run(["node", str(Path(__file__).with_name("seed-images.cjs")), str(root/"Movies")], check=True)
