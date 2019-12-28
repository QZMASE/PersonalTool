for %%a in (*.ts) do ffmpeg -i "%%a" -vcodec copy -acodec copy -f mp4 "%%~na.mp4"
pause