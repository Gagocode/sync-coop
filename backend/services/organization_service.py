from repositories import organization_repository


class OrganizationError(Exception):
    pass


def organization_setup_available():
    return not organization_repository.has_any()


def create_first_organization(user_id, data):
    name = _require_name(data.get("name"), "Nome da organização obrigatório")
    organization = organization_repository.create_first_for_manager(user_id, name)
    if not organization:
        raise OrganizationError("A configuração inicial já foi concluída ou não está disponível")
    return organization


def _require_name(value, message):
    value = value.strip() if value else ""
    if not value:
        raise OrganizationError(message)
    return value
