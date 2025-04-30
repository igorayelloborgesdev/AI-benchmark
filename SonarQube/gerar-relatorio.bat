@echo off
setlocal enabledelayedexpansion

:: Configurações
set SONAR_URL=http://localhost:9000
set SONAR_TOKEN=squ_cdf0e39372ecce0335754a49370a9cfae9a00522
set PROJECT_KEY=meu-projeto

:: Baixar métricas do SonarQube
curl -u %SONAR_TOKEN%: "%SONAR_URL%/api/measures/component?component=%PROJECT_KEY%&metricKeys=coverage,bugs,vulnerabilities,code_smells,duplicated_lines_density" -o resultado.json

:: Inicializar variáveis com valores vazios
set COVERAGE=

:: Extrair valores de "coverage" usando findstr e for /f
for /f "tokens=2 delims=:,{}[]" %%a in ('findstr /i "\"metric\":\"coverage\"" resultado.json') do (
    set TEMP=%%a
    set COVERAGE=!TEMP:~1,-1!
)
pause

:: Exibir os valores extraídos
echo Coverage: !COVERAGE!
pause
:: Gerar HTML com as métricas extraídas
(
echo ^<html^>
echo ^<head^>
echo ^<title^>Relatório SonarQube^</title^>
echo ^<style^>
echo body { font-family: Arial, sans-serif; margin: 20px; background: #f7f9fc; }
echo h1 { color: #333; }
echo table { border-collapse: collapse; width: 80%%; margin-top: 20px; }
echo th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
echo th { background-color: #4CAF50; color: white; }
echo tr:nth-child(even) { background-color: #f2f2f2; }
echo tr:hover { background-color: #ddd; }
echo ^</style^>
echo ^</head^>
echo ^<body^>
echo ^<h1^>Relatório SonarQube - Projeto: %PROJECT_KEY%^</h1^>
echo ^<table^>
echo ^<tr^>^<th^>Métrica^</th^>^<th^>Valor^</th^>^</tr^>
echo ^<tr^>^<td^>Coverage (%%)^</td^>^<td^>!COVERAGE!^</td^>^</tr^>
echo ^</table^>
echo ^</body^>
echo ^</html^>
) > report.html

echo Relatório gerado: report.html
pause
