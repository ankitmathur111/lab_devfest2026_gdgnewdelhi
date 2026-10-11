from datetime import datetime, timezone

class AuditLog:
    def __init__(self):
        self.events = []

    def record(self, event_type, **details):
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **details,
        })

audit_log = AuditLog()
