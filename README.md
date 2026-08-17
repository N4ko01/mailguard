# MailGuard AI

Aplicación web para clasificar correos como HAM o SPAM usando TF-IDF y Regresión Logística.

## Ejecución local

```powershell
python -m pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000`.

Coloca `tfidf_vectorizer.pkl` y `spam_classifier.pkl` dentro de `models/`.
