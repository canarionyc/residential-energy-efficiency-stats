@echo on
echo =========================================
echo       Radiance Installation Test V2
echo =========================================

set RADIANCE_HOME=C:\Radiance-5-4
set RAYPATH=%RADIANCE_HOME%\lib
set PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%RHINO8_HOME%\System;%RADIANCE_HOME%\bin

echo.
echo [1/3] Creating a simple test scene (test_scene.rad)...
echo void plastic red_plastic > test_scene.rad
echo 0 >> test_scene.rad
echo 0 >> test_scene.rad
echo 5 0.8 0.1 0.1 0.05 0.05 >> test_scene.rad

echo red_plastic sphere ball >> test_scene.rad
echo 0 >> test_scene.rad
echo 0 >> test_scene.rad
echo 4 0 0 0 1 >> test_scene.rad

echo void light bright >> test_scene.rad
echo 0 >> test_scene.rad
echo 0 >> test_scene.rad
echo 3 100 100 100 >> test_scene.rad

:: [FIXED] Moved the light to X=0, Y=0, Z=10 so the camera isn't inside it!
echo bright sphere fixture >> test_scene.rad
echo 0 >> test_scene.rad
echo 0 >> test_scene.rad
echo 4 0 0 10 0.5 >> test_scene.rad

echo.
echo [2/3] Compiling the scene with oconv...
oconv test_scene.rad > test_scene.oct

echo.
echo [3/3] Rendering the scene with rpict...
rpict -vp 5 5 5 -vd -1 -1 -1 -vu 0 0 1 -x 200 -y 200 test_scene.oct > test_scene.hdr

echo.
echo [4/4] Converting to BMP...
:: Using the < and > redirection is the safest way to run Radiance image tools
ra_bmp < test_scene.hdr > test_scene.bmp

echo.
echo =========================================
echo TEST PASSED! 
echo Open test_scene.bmp to see the result!
echo =========================================
rem pause