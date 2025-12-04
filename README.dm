Для того, чтобы запустить сервер, введите в терминале:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
