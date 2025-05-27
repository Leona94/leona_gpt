# leona_gpt

Dieses Projekt demonstriert, wie sich E-Mail-Dateien (`.eml`) einlesen und 
mit [LlamaIndex](https://github.com/run-llama/llama_index) durchsuchen lassen.

## Voraussetzungen

* Python 3.9+
* Die Bibliothek `llama-index` muss installiert sein:
  ```bash
  pip install llama-index
  ```

## Nutzung

1. **E-Mails vorbereiten**: Speichere alle `.eml` Dateien in einem Verzeichnis.
2. **Index erstellen und abfragen**:
   ```bash
   python index_emails.py /pfad/zum/eml-verzeichnis
   ```
   Anschließend kannst du Fragen zum Inhalt der Mails stellen.

Das Skript liest die E-Mails ein, erkennt Anhänge, gruppiert sie nach Threads
und erstellt einen Vektorindex. Textbasierte Anhänge werden automatisch
geöffnet und dem Index hinzugefügt.
