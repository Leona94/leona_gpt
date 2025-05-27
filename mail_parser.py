import base64
from email import policy
from email.parser import BytesParser
from typing import List, Dict


def parse_eml(file_path: str) -> Dict:
    """Parse an .eml file and return a dict with useful fields."""
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    info = {
        "subject": msg.get("subject"),
        "message_id": msg.get("message-id"),
        "from": msg.get("from"),
        "to": msg.get("to"),
        "cc": msg.get("cc"),
        "date": msg.get("date"),
    }

    # Extract body text
    if msg.is_multipart():
        parts = []
        for part in msg.walk():
            cdisp = part.get_content_disposition()
            if cdisp == "attachment":
                continue
            if part.get_content_type() == "text/plain":
                parts.append(part.get_content())
        body = "\n".join(parts)
    else:
        body = msg.get_content()
    info["body"] = body.strip() if body else ""

    # Extract attachments
    attachments = []
    for part in msg.iter_attachments():
        payload = part.get_payload(decode=True) or b""
        content_type = part.get_content_type()
        text = None
        if content_type.startswith("text/"):
            charset = part.get_content_charset() or "utf-8"
            try:
                text = payload.decode(charset, errors="replace")
            except Exception:
                text = None
        attachments.append(
            {
                "filename": part.get_filename(),
                "content_type": content_type,
                "size": len(payload),
                "text": text,
            }
        )
    info["attachments"] = attachments
    return info


def extract_thread_id(msg) -> str:
    """Return a thread identifier for the given message."""
    refs = msg.get("References")
    if refs:
        return refs.split()[-1]
    irt = msg.get("In-Reply-To")
    if irt:
        return irt.strip()
    return msg.get("Message-ID")


def group_emails_by_thread(infos: List[Dict]) -> Dict[str, List[Dict]]:
    """Group parsed email info dicts by thread id."""
    threads: Dict[str, List[Dict]] = {}
    for info in infos:
        tid = info.get("thread_id") or info.get("message_id")
        threads.setdefault(tid, []).append(info)
    for msgs in threads.values():
        msgs.sort(key=lambda x: x.get("date"))
    return threads
