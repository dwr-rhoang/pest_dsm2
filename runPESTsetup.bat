set CONDAPATH=C:\Miniconda3
set ENVNAME=pydelmod
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python pestsetup.py
addreg1 dsm2_820.pst dsm2_820_reg.pst
pause