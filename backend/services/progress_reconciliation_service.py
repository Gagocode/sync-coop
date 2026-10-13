"""Explicit, idempotent reconciliation of state written by older versions."""

from database.connection import transaction
from repositories import achievement_repository, certificate_repository, disc_repository
from repositories import mission_repository, project_repository, user_repository
from services.achievement_service import evaluate_user_achievements
from services.disc_service import build_result_summary, calculate_initial_class
from services.evolution_service import backfill_history_for_current_state
from services.mission_service import create_initial_missions_for_user, complete_missions_for_event
from services.observed_disc_service import update_observed_disc


def reconcile_existing_progress():
    for user_id in user_repository.list_user_ids():
        reconcile_user_progress(user_id)


def reconcile_user_progress(user_id):
    with transaction():
        create_initial_missions_for_user(user_id)
        user = user_repository.find_by_id(user_id)
        disc = disc_repository.find_initial_result_by_user_id(user_id)
        if disc:
            expected_class = calculate_initial_class(
                build_result_summary(disc)["predominant_dimension"]
            )
            if user.classe != expected_class:
                user_repository.update_profile_class(user_id, expected_class)
            complete_missions_for_event(user_id, "DISC_COMPLETED")
            complete_missions_for_event(user_id, "PROFILE_COMPLETED")

        projects = project_repository.list_by_user_id(user_id)
        certificates = certificate_repository.list_by_user_id(user_id)
        if projects:
            complete_missions_for_event(user_id, "PROJECT_CREATED")
        if certificates:
            complete_missions_for_event(user_id, "CERTIFICATE_CREATED")

        evaluate_user_achievements(user_id)
        missions = mission_repository.list_by_user_id(user_id)
        achievements = achievement_repository.list_unlocked_by_user_id(user_id)
        backfill_history_for_current_state(
            user_id=user_id,
            projects=projects,
            certificates=certificates,
            completed_missions=[mission for mission in missions if mission.status == "Concluida"],
            unlocked_achievements=achievements,
        )
        update_observed_disc(user_id)
