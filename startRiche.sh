npm run build; 
cp -r build flask-app/; 
cd flask-app;
source venv/Scripts/activate

python3 -m flask run &

sleep 2
open "http://127.0.0.1:5000"
read -p "********************************************"$'\n'"Appuyez sur Entrée pour fermer l'application"$'\n'"********************************************"$'\n'
kill -9 $(lsof -t -i:5000)
