Для запуска сайта необходимо выполнить несколько команд в терминале:

Для macOS:
cd firefly(Перейти в папку проекта, если еще не в ней)
python -m venv venv  !(если виртуальная среда не установлена)
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload 

Для Windows:
cd firefly(Перейти в папку проекта, если еще не в ней)
python -m venv venv  !(если виртуальная среда не установлена)
.\venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn app.main:app --reload 

Далее переходите по ссылке в выводе терминала