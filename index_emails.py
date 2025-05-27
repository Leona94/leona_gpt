import os
from typing import List

from mail_parser import parse_eml, extract_thread_id

try:
    from llama_index import Document, VectorStoreIndex
except ImportError:  # pragma: no cover - llama_index may not be installed
    Document = None
    VectorStoreIndex = None


def load_emails(directory: str) -> List[dict]:
    infos = []
    for fname in os.listdir(directory):
        if fname.lower().endswith(".eml"):
            path = os.path.join(directory, fname)
            info = parse_eml(path)
            info["thread_id"] = info.get("thread_id") or info.get("message_id")
            infos.append(info)
    return infos


def build_index(infos: List[dict]):
    if Document is None or VectorStoreIndex is None:
        raise RuntimeError("llama_index is not installed")

    docs = []
    for info in infos:
        text_content = info["body"]
        for att in info["attachments"]:
            if att["text"]:
                text_content += f"\n\nAttachment {att['filename']}\n{att['text']}"
        docs.append(
            Document(
                text_content,
                metadata={
                    "subject": info["subject"],
                    "from": info["from"],
                    "to": info["to"],
                    "cc": info["cc"],
                    "date": info["date"],
                    "thread_id": info.get("thread_id"),
                },
            )
        )

    index = VectorStoreIndex.from_documents(docs)
    return index


def interactive_query(index):
    qe = index.as_query_engine()
    while True:
        try:
            question = input("Frage: ")
        except EOFError:
            break
        if not question:
            break
        result = qe.query(question)
        print(result)


def main(directory: str):
    infos = load_emails(directory)
    index = build_index(infos)
    interactive_query(index)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python index_emails.py <directory_with_eml_files>")
        raise SystemExit(1)
    main(sys.argv[1])
