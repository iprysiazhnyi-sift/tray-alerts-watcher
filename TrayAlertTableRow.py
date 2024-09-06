from dataclasses import dataclass


@dataclass
class TrayAlertTableRow:
    workflow: str
    message: str
    reason: str
    solution_instance_id: str
    customer: str
    action_item: str
