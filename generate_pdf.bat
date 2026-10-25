@echo off
cd /d C:\vnchoicedouble
echo ================================
echo  Choice Slats - Tao PDF dao tao
echo ================================
python _mkpdf.py
echo.
echo Exit code: %errorlevel%
echo (Neu thay "PDF OK -> ..." la thanh cong. File: Choice_Slats_Training_Manual.pdf)
echo.
pause
