from rag import answer

def main():
    print("RAG-ассистент. Введи вопрос или 'exit'.")
    while True:
        q = input("\n> ").strip()
        if q.lower() in {"exit", "quit"}:
            break
        if not q:
            continue
        print("\n" + answer(q))

if __name__ == "__main__":
    main()


'''
Запуск
pip install -r requirements.txt
# положи свои .md/.txt/.pdf в data/
python ingest.py
python app.py
'''