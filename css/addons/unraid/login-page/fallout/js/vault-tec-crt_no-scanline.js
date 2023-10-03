// Adds a video background
// Source: https://www.youtube.com/watch?v=ehvduomE0AU

let video = `
<div class="background-wrap"><video id="video-bg-elem" preload="auto" autoplay="true" loop="loop" muted="muted"> <source src="https:\/\/gilbn.github.io\/theme.park\/css\/addons\/unraid\/login-page\/fallout\/video\/VaultTecCRTLoopNoScanline.mp4" type="video\/mp4">Video not supported</video></div>
`
document.body.innerHTML += video
