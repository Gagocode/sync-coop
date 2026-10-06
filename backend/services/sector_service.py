from repositories import sector_repository, user_repository


class OrganizationManagementError(Exception):
    pass


def list_sectors(manager):
    organization_id = _manager_organization_id(manager)
    return sector_repository.list_by_organization(organization_id)


def create_sector(manager, data):
    organization_id = _manager_organization_id(manager)
    name = _require_name(data.get("name"))
    return sector_repository.create(organization_id, name)


def update_sector(manager, sector_id, data):
    organization_id = _manager_organization_id(manager)
    if not sector_repository.find_by_id_for_organization(sector_id, organization_id):
        raise OrganizationManagementError("Setor não encontrado")
    name = _require_name(data.get("name"))
    sector = sector_repository.update_name(sector_id, organization_id, name)
    if not sector:
        raise OrganizationManagementError("Setor não encontrado")
    return sector


def delete_sector(manager, sector_id):
    organization_id = _manager_organization_id(manager)
    if not sector_repository.find_by_id_for_organization(sector_id, organization_id):
        raise OrganizationManagementError("Setor não encontrado")
    if not sector_repository.delete_if_empty(sector_id, organization_id):
        raise OrganizationManagementError(
            "Não é possível excluir um setor que possui colaboradores associados"
        )


def list_manageable_users(manager):
    organization_id = _manager_organization_id(manager)
    return user_repository.list_for_organization_or_unassigned(organization_id)


def assign_user_to_sector(manager, user_id, sector_id):
    organization_id = _manager_organization_id(manager)
    if not sector_repository.find_by_id_for_organization(sector_id, organization_id):
        raise OrganizationManagementError("Setor não encontrado nesta organização")
    if not user_repository.assign_sector(user_id, organization_id, sector_id):
        raise OrganizationManagementError(
            "Usuário não encontrado, pertence a outra organização ou é gestor"
        )


def _manager_organization_id(manager):
    if manager.role != "manager" or manager.organization_id is None:
        raise OrganizationManagementError("Gestor sem organização associada")
    return manager.organization_id


def _require_name(value):
    value = value.strip() if value else ""
    if not value:
        raise OrganizationManagementError("Nome do setor obrigatório")
    return value
