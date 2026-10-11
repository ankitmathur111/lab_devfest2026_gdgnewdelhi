import uuid
from .models import ReviewItem
from .audit import audit_log

class ReviewQueue:
    def __init__(self):
        self.items = {}

    def add(self, user_id, action, arguments, reason):
        item_id = str(uuid.uuid4())[:8]
        item = ReviewItem(item_id, user_id, action, arguments, reason)
        self.items[item_id] = item
        audit_log.record(
            "HUMAN_REVIEW_CREATED",
            review_id=item_id,
            user_id=user_id,
            action=action,
            reason=reason,
        )
        return item

    def pending(self):
        return [
            {
                "id": x.id,
                "user_id": x.user_id,
                "action": x.action,
                "arguments": x.arguments,
                "reason": x.reason,
                "status": x.status,
            }
            for x in self.items.values()
            if x.status == "PENDING"
        ]

    def decide(self, review_id, approve):
        item = self.items.get(review_id)
        if not item:
            return {"error": "Review item not found"}

        item.status = "APPROVED" if approve else "REJECTED"
        audit_log.record(
            "HUMAN_REVIEW_DECISION",
            review_id=review_id,
            decision=item.status,
            action=item.action,
        )
        return {"review_id": review_id, "status": item.status}

review_queue = ReviewQueue()
