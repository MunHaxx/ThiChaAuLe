npm run build
xcopy /s build flask-app\
cd flask-app
start cmd /c "flask run"
ping -n 2 127.0.0.1 > nul
start http://127.0.0.1:5000
set /p dummy_var="Appuyez sur Entrée pour fermer l'application"
for /f "tokens=5" %a in ('netstat -aon ^| findstr :5000') do taskkill /f /pid %a