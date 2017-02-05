rmdir /s /q dist
rmdir /s /q build
pyinstaller -D FlappyBird.py --hidden-import=lib
xcopy data dist\FlappyBird\data\ /S /E /y
pause