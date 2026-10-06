from datetime import datetime, timezone

from repositories import user_repository
from services.activity_service import calculate_engagement
from services.sector_service import OrganizationManagementError


ENGAGEMENT_LABELS = {"active": "Ativo", "attention": "Atenção", "inactive": "Inativo"}


def get_corporate_dashboard(manager, now=None):
    if manager.role != "manager" or manager.organization_id is None:
        raise OrganizationManagementError("Gestor sem organização associada")
    now = now or datetime.now(timezone.utc)
    collaborators = user_repository.list_collaborators_for_organization(manager.organization_id)
    metrics = {"total": len(collaborators), "active": 0, "attention": 0, "inactive": 0}
    for collaborator in collaborators:
        status = calculate_engagement(collaborator["last_activity_at"], now)
        metrics[status] += 1
        collaborator["engagement_status"] = status
        collaborator["engagement_label"] = ENGAGEMENT_LABELS[status]
        activity = collaborator["last_activity_at"]
        collaborator["activity_label"] = (
            datetime.fromisoformat(activity).strftime("%d/%m/%Y %H:%M:%S UTC")
            if activity else "Sem atividade registrada"
        )
    return {"metrics": metrics, "collaborators": collaborators}
