@echo off
setlocal enabledelayedexpansion

:: Set the folder containing your images
set "folder=F:\WorkingDirectory_AI\biometric\fingerprints"
set "count=1"

cd /d "%folder%"

:: Loop through all files in the folder
for %%F in (*) do (
    :: Rename each file with sequential numbering and change the extension to PNG
    ren "%%F" "!count!.png"
    set /a count+=1
)

echo Renaming complete.
pause
