Для запуска сайта необходимо выполнить несколько команд в терминале:

cd firefly
python3 -m venv venv  !(если виртуальная среда не установлена)
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload 

Далее переходите по ссылке в выводе терминала