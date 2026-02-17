from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AuditEvent:
    org_id: str
    actor: str
    action: str
    details: dict

class InMemoryStore:
    def __init__(self):
        self.teams: Dict[str, dict] = {}
        self.audit_logs: Dict[str, List[AuditEvent]] = defaultdict(list)
        self.paper_positions: Dict[str, Dict[str, dict]] = defaultdict(dict)
        self.alerts: List[dict] = []

    def add_audit(self, org_id: str, actor: str, action: str, details: dict):
        self.audit_logs[org_id].append(AuditEvent(org_id, actor, action, details))

store = InMemoryStore()
