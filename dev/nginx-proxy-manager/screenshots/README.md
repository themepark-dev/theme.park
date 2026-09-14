# PR 734 screenshots

Both captures show NPM 2.15.1, Aquamarine, native light mode, Chromium
151.0.7922.34, and a 1440x1000 viewport with synthetic hosts.

`before.png` uses the base CSS from `968f7bed` in an isolated browser request
override. `after.png` loads the rewritten CSS through the mounted startup script.
The Add Proxy Host dialog is empty in both captures. The running review
instance remains on the rewritten stylesheet.

These two images are embedded in the PR. Full test results and intermediate
screenshots remain under ignored `dev/artifacts/nginx-proxy-manager/707/`.
