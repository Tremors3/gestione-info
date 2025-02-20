@echo off
IF "%~1" == "" GOTO end
IF "%~1" == "-w" GOTO webapp
IF "%~1" == "-p" GOTO parser
IF "%~1" == "-h" GOTO help
GOTO end

:webapp
echo [32mStarting Web App[0m
cd project\webapp
venv\Scripts\activate.bat & python run.py && venv\Scripts\deactivate.bat & cd .. & cd .. & GOTO end

:parser
echo [32mStarting Parser[0m
cd workspace\experiments
venv\Scripts\activate.bat & python download-parsing\parser.py & venv\Scripts\deactivate & cd .. & cd .. & GOTO end

:help
echo:
echo HELP PAGE
echo:
echo syntax: graboid.bat -[h,p,w]
echo:
echo    -h Show help
echo    -w Start Web App
echo    -p Start Parser
echo:

:end
echo fine