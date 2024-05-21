document.addEventListener('DOMContentLoaded', function () {
    const audio = document.getElementById('background-music');
    const playPauseButton = document.getElementById('play-pause');
    const volumeControl = document.getElementById('volume-control');

    playPauseButton.addEventListener('click', function () {
        if (audio.paused) {
            audio.play();
            playPauseButton.textContent = '暂停';
        } else {
            audio.pause();
            playPauseButton.textContent = '播放';
        }
    });

    volumeControl.addEventListener('input', function () {
        audio.volume = volumeControl.value;
    });

    // Auto-play on page load
    audio.play();
});
