from repositories import disc_repository
from services.achievement_service import evaluate_user_achievements
from services.evolution_service import record_disc_completed
from services.mission_service import complete_user_mission_by_key
from services.observed_disc_service import update_observed_disc


DISC_DIMENSIONS = ("D", "I", "S", "C")

QUESTIONS = [
    {
        "id": "q1",
        "text": "Voce recebe um trabalho em grupo com prazo curto. O que faz primeiro?",
        "options": [
            {"dimension": "D", "text": "Assumo a lideranca e defino as prioridades."},
            {"dimension": "I", "text": "Converso com o grupo para engajar todos."},
            {"dimension": "S", "text": "Organizo uma divisao equilibrada das tarefas."},
            {"dimension": "C", "text": "Analiso o enunciado e crio um plano detalhado."},
        ],
    },
    {
        "id": "q2",
        "text": "Durante uma apresentacao, surge uma pergunta dificil.",
        "options": [
            {"dimension": "D", "text": "Respondo com firmeza e direciono a discussao."},
            {"dimension": "I", "text": "Uso a pergunta para criar conexao com a turma."},
            {"dimension": "S", "text": "Mantenho a calma e respondo de forma colaborativa."},
            {"dimension": "C", "text": "Peço um momento para estruturar uma resposta precisa."},
        ],
    },
    {
        "id": "q3",
        "text": "Um colega esta atrasando uma entrega importante.",
        "options": [
            {"dimension": "D", "text": "Cobro uma decisao objetiva para resolver o atraso."},
            {"dimension": "I", "text": "Converso para motivar e entender o que aconteceu."},
            {"dimension": "S", "text": "Ofereco ajuda para manter o grupo em ritmo."},
            {"dimension": "C", "text": "Reviso o cronograma e redistribuo com criterios claros."},
        ],
    },
    {
        "id": "q4",
        "text": "Voce precisa escolher uma atividade extracurricular.",
        "options": [
            {"dimension": "D", "text": "Escolho algo com desafios e responsabilidade."},
            {"dimension": "I", "text": "Escolho algo com networking e interacao."},
            {"dimension": "S", "text": "Escolho algo consistente e de longo prazo."},
            {"dimension": "C", "text": "Escolho algo que fortalece conhecimento tecnico."},
        ],
    },
    {
        "id": "q5",
        "text": "Um projeto muda de direcao no meio do semestre.",
        "options": [
            {"dimension": "D", "text": "Tomo decisoes rapidas para adaptar a execucao."},
            {"dimension": "I", "text": "Alinho expectativas e mantenho o grupo animado."},
            {"dimension": "S", "text": "Busco preservar o que ja estava funcionando."},
            {"dimension": "C", "text": "Reavalio requisitos, riscos e impactos da mudanca."},
        ],
    },
    {
        "id": "q6",
        "text": "Em uma reuniao, ninguem quer iniciar a conversa.",
        "options": [
            {"dimension": "D", "text": "Inicio propondo um caminho de decisao."},
            {"dimension": "I", "text": "Quebro o gelo e puxo a participacao."},
            {"dimension": "S", "text": "Crio um ambiente tranquilo para todos falarem."},
            {"dimension": "C", "text": "Apresento os pontos da pauta de forma ordenada."},
        ],
    },
    {
        "id": "q7",
        "text": "Voce recebe feedback critico sobre um trabalho.",
        "options": [
            {"dimension": "D", "text": "Uso o feedback para corrigir rapidamente."},
            {"dimension": "I", "text": "Peço exemplos e mantenho o dialogo aberto."},
            {"dimension": "S", "text": "Escuto com calma e incorporo aos poucos."},
            {"dimension": "C", "text": "Registro os pontos e reviso criterios tecnicos."},
        ],
    },
    {
        "id": "q8",
        "text": "Uma oportunidade de estagio exige aprender algo novo.",
        "options": [
            {"dimension": "D", "text": "Aceito o desafio e aprendo durante a execucao."},
            {"dimension": "I", "text": "Procuro pessoas que possam trocar experiencias."},
            {"dimension": "S", "text": "Monto uma rotina constante de estudo."},
            {"dimension": "C", "text": "Busco materiais confiaveis e estudo fundamentos."},
        ],
    },
    {
        "id": "q9",
        "text": "O grupo discorda sobre a melhor solucao.",
        "options": [
            {"dimension": "D", "text": "Defendo uma escolha e levo o grupo a decidir."},
            {"dimension": "I", "text": "Facilito a conversa para aproximar opinioes."},
            {"dimension": "S", "text": "Procuro uma solucao que preserve o equilibrio."},
            {"dimension": "C", "text": "Comparo alternativas com base em dados e criterios."},
        ],
    },
    {
        "id": "q10",
        "text": "Voce precisa entregar uma tarefa individual complexa.",
        "options": [
            {"dimension": "D", "text": "Comeco pelo ponto mais dificil para destravar."},
            {"dimension": "I", "text": "Discuto ideias com colegas antes de finalizar."},
            {"dimension": "S", "text": "Avanco de forma constante ate concluir."},
            {"dimension": "C", "text": "Planejo etapas e valido cada detalhe."},
        ],
    },
    {
        "id": "q11",
        "text": "Um evento da faculdade precisa de voluntarios.",
        "options": [
            {"dimension": "D", "text": "Assumo uma frente com metas claras."},
            {"dimension": "I", "text": "Ajudo na divulgacao e recepcao das pessoas."},
            {"dimension": "S", "text": "Dou suporte onde o time mais precisar."},
            {"dimension": "C", "text": "Cuido de lista, recursos e organizacao."},
        ],
    },
    {
        "id": "q12",
        "text": "Voce concluiu uma atividade importante.",
        "options": [
            {"dimension": "D", "text": "Penso no proximo desafio a conquistar."},
            {"dimension": "I", "text": "Compartilho o resultado com outras pessoas."},
            {"dimension": "S", "text": "Reconheco o esforco coletivo e mantenho o ritmo."},
            {"dimension": "C", "text": "Registro aprendizados e pontos de melhoria."},
        ],
    },
]


class DiscError(Exception):
    pass


def get_questions():
    return QUESTIONS


def submit_initial_disc(user_id, answers):
    existing_result = get_initial_disc_result(user_id)
    if existing_result:
        raise DiscError("DISC inicial ja realizado")

    scores = calculate_scores(answers)
    result = disc_repository.save_initial_result(user_id, scores)
    record_disc_completed(user_id, result.created_at)
    complete_user_mission_by_key(user_id, "complete_disc_quiz")
    evaluate_user_achievements(user_id)
    update_observed_disc(user_id)
    return build_result_summary(result)


def get_initial_disc_result(user_id):
    result = disc_repository.find_initial_result_by_user_id(user_id)
    return build_result_summary(result) if result else None


def calculate_scores(answers):
    if not answers:
        raise DiscError("Responda todas as perguntas do quiz")

    questions_by_id = {question["id"]: question for question in QUESTIONS}
    scores = {dimension: 0 for dimension in DISC_DIMENSIONS}

    for question_id, question in questions_by_id.items():
        selected_dimension = answers.get(question_id)
        valid_dimensions = {option["dimension"] for option in question["options"]}
        if selected_dimension not in valid_dimensions:
            raise DiscError("Responda todas as perguntas do quiz")
        scores[selected_dimension] += 1

    return scores


def build_result_summary(result):
    total = result.d_score + result.i_score + result.s_score + result.c_score
    scores = {
        "D": result.d_score,
        "I": result.i_score,
        "S": result.s_score,
        "C": result.c_score,
    }
    percentages = {
        dimension: round((score / total) * 100) if total else 0
        for dimension, score in scores.items()
    }
    predominant_dimension = max(scores, key=scores.get)

    return {
        "user_id": result.user_id,
        "scores": scores,
        "total": total,
        "percentages": percentages,
        "predominant_dimension": predominant_dimension,
        "created_at": result.created_at,
    }
