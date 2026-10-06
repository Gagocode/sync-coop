const escapeHtml = (value) => String(value ?? "").replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
const symbol = (name, className = "") => `<svg class="sd-icon ${className}" aria-hidden="true" focusable="false"><use href="/assets/images/symbols.svg#${name}"></use></svg>`;
const achievementSymbols = { primeiro_passo: "disc", construtor: "project", desenvolvendo_habilidades: "certificate", explorador: "mission", curriculo_vivo: "resume" };

const appShell = document.querySelector(".app-shell");
if (appShell) {
  const pathname = window.location.pathname;
  const items = [
    ["/dashboard", "Jornada"], ["/perfil/", "Perfil"], ["/missoes/", "Missões"],
    ["/projetos/", "Projetos"], ["/certificados/", "Certificados"]
  ];
  const navigation = document.createElement("header");
  navigation.className = "app-header";
  navigation.innerHTML = `<a class="app-brand" href="/dashboard"><img class="brand-mark" src="/assets/images/logo.png" alt="" width="40" height="40"><span>Sync Disc</span></a><nav aria-label="Navegação principal">${items.map(([url, label]) => `<a href="${url}" ${pathname === url || (url !== "/dashboard" && pathname.startsWith(url)) ? 'aria-current="page"' : ""}>${label}</a>`).join("")}</nav>`;
  appShell.prepend(navigation);
}

const setTab = (name) => {
  document.querySelectorAll(".workspace-tab").forEach((tab) => {
    const selected = tab.dataset.tab === name;
    tab.classList.toggle("is-active", selected);
    tab.setAttribute("aria-selected", String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });
  document.querySelectorAll(".workspace-panel").forEach((panel) => {
    const selected = panel.dataset.panel === name;
    panel.classList.toggle("is-active", selected);
    panel.hidden = !selected;
  });
};

const showFeedback = (message, isError = false) => {
  const feedback = document.querySelector("#dashboard-feedback");
  feedback.textContent = message;
  feedback.classList.toggle("is-error", isError);
  feedback.classList.toggle("is-visible", Boolean(message));
};

const formatDate = (value) => {
  if (!value) return "-";
  const date = /^\d{4}-\d{2}-\d{2}$/.test(value) ? new Date(`${value}T12:00:00`) : new Date(value);
  return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("pt-BR", { dateStyle: "medium" }).format(date);
};

const initJourneyQuiz = () => {
  const form = document.querySelector("[data-journey-quiz]");
  if (!form) return;
  const narrative = [
    ["Você entrou em uma equipe para desenvolver um projeto importante.", ["Defino prioridades e proponho um caminho para começar.", "Junto as pessoas para trocar ideias e encontrar possibilidades.", "Entendo como cada pessoa pode contribuir melhor.", "Organizo as informações e estruturo um plano de trabalho."]],
    ["Na apresentação do projeto, surge uma pergunta que o grupo não esperava.", ["Respondo com o que sabemos e encaminho uma decisão.", "Abro a conversa para entender o interesse de quem perguntou.", "Escuto a pergunta até o fim e construo uma resposta em conjunto.", "Peço um instante para conferir os dados antes de responder."]],
    ["Uma parte importante do trabalho está atrasada e o prazo se aproxima.", ["Reorganizo o plano e combino uma nova divisão de tarefas.", "Converso com o grupo para entender o que está travando.", "Ofereço apoio para que a equipe retome o ritmo.", "Reviso as etapas e identifico onde o cronograma mudou."]],
    ["Você pode escolher uma atividade para complementar sua formação.", ["Uma atividade com responsabilidade por uma entrega concreta.", "Uma atividade com troca de ideias e novas conexões.", "Uma atividade contínua em que possa desenvolver uma prática.", "Uma atividade para aprofundar um tema técnico."]],
    ["No meio do projeto, chegam novas informações que mudam o plano.", ["Ajusto a execução e ajudo o grupo a seguir em frente.", "Alinho as expectativas para que todos entendam a mudança.", "Preservo o que está funcionando e adapto o restante com calma.", "Reavalio os requisitos e verifico os impactos antes de alterar."]],
    ["Você participa de uma reunião com pessoas que ainda não conhece.", ["Apresento uma proposta para dar direção à conversa.", "Inicio uma conversa para aproximar as pessoas.", "Crio espaço para que cada pessoa se sinta à vontade para falar.", "Organizo os pontos da pauta para manter a conversa clara."]],
    ["Uma pessoa revisa seu trabalho e sugere mudanças importantes.", ["Uso os comentários para ajustar o trabalho e avançar.", "Peço exemplos e converso sobre as sugestões.", "Escuto com atenção e incorporo as mudanças gradualmente.", "Registro os pontos e verifico cada critério do trabalho."]],
    ["Você recebe a oportunidade de aprender algo que ainda não conhece.", ["Aceito o desafio e descubro o caminho durante a prática.", "Procuro pessoas para trocar experiências sobre o tema.", "Monto uma rotina para aprender com regularidade.", "Busco materiais confiáveis e estudo os fundamentos."]],
    ["Duas propostas diferentes dividem a opinião da equipe.", ["Apresento os motivos da minha proposta e ajudo o grupo a decidir.", "Facilito a conversa para aproximar os pontos de vista.", "Busco uma alternativa que preserve o equilíbrio do grupo.", "Comparo as propostas usando critérios e informações disponíveis."]],
    ["Uma tarefa complexa precisa ser concluída até o fim da semana.", ["Começo pela parte que pode destravar o restante.", "Troco ideias com colegas antes de definir a entrega.", "Avanço em etapas, mantendo um ritmo constante.", "Planejo as etapas e verifico cada requisito ao concluir."]],
    ["Sua turma está organizando uma atividade aberta à comunidade.", ["Assumo uma frente com uma entrega e um prazo definidos.", "Ajudo a divulgar a atividade e receber participantes.", "Ofereço apoio nas tarefas que o grupo precisar.", "Organizo a lista de materiais e as necessidades da atividade."]],
    ["Um projeto em equipe chega ao fim depois de várias semanas.", ["Identifico qual pode ser o próximo desafio do grupo.", "Compartilho o resultado e converso sobre o que aprendemos.", "Reconheço a contribuição de todos e o trabalho realizado.", "Registro os aprendizados e os pontos que podem melhorar."]]
  ];
  const questions = [...form.querySelectorAll(".journey-question")];
  const controls = { label: form.querySelector("[data-step-label]"), percent: form.querySelector("[data-step-percent]"), fill: form.querySelector("[data-progress-fill]"), track: form.querySelector("[role=progressbar]"), back: form.querySelector("[data-quiz-back]"), next: form.querySelector("[data-quiz-next]"), submit: form.querySelector("[data-quiz-submit]") };
  if (!questions.length) return;
  questions.forEach((question, index) => {
    const scenario = narrative[index];
    if (scenario) {
      question.querySelector("legend").textContent = scenario[0];
      question.querySelectorAll(".scenario-option > span:first-of-type").forEach((label, optionIndex) => { label.textContent = scenario[1][optionIndex]; });
    }
  });
  let current = 0;
  const render = () => {
    questions.forEach((question, index) => {
      question.hidden = index !== current;
      question.classList.toggle("is-entering", index === current);
      question.querySelectorAll("input").forEach((input) => { input.required = index === current; });
    });
    const progress = Math.round(((current + 1) / questions.length) * 100);
    controls.label.textContent = `Etapa ${current + 1} de ${questions.length}`;
    controls.percent.textContent = `${progress}%`;
    controls.fill.style.width = `${progress}%`;
    controls.track.setAttribute("aria-valuenow", String(current + 1));
    controls.back.hidden = current === 0;
    controls.next.hidden = current === questions.length - 1;
    controls.submit.hidden = current !== questions.length - 1;
  };
  controls.next.addEventListener("click", () => {
    const selected = questions[current].querySelector("input:checked");
    if (!selected) { questions[current].querySelector("input").reportValidity(); return; }
    current += 1;
    render();
  });
  controls.back.addEventListener("click", () => { current = Math.max(0, current - 1); render(); });
  form.addEventListener("submit", (event) => {
    const unanswered = questions.find((question) => !question.querySelector("input:checked"));
    if (unanswered) { event.preventDefault(); current = questions.indexOf(unanswered); render(); unanswered.querySelector("input").reportValidity(); }
  });
  render();
};

initJourneyQuiz();

const renderDisc = (disc) => {
  const element = document.querySelector("#disc-content");
  const profileElement = document.querySelector("#profile-disc");
  if (!disc) {
    element.innerHTML = `<div class="disc-empty"><span class="disc-empty-icon">${symbol("disc")}</span><div><h3>DISC Inicial pendente</h3><p>Seu resultado aparecera aqui quando estiver disponivel.</p></div></div>`;
    profileElement.innerHTML = '<p class="muted">Resultado DISC Inicial ainda nao realizado.</p>';
    return;
  }
  const dimensions = Object.entries(disc.percentages || {});
  const bars = dimensions.map(([dimension, percentage]) => `<div class="disc-bar-row"><span>${escapeHtml(dimension)}</span><div class="mini-track"><i class="disc-${escapeHtml(dimension.toLowerCase())}" style="width:${Number(percentage) || 0}%"></i></div><strong>${Number(percentage) || 0}%</strong></div>`).join("");
  element.innerHTML = `<div class="disc-result"><div class="disc-dominant"><span class="disc-letter">${escapeHtml(disc.predominant_dimension)}</span><div><strong>${escapeHtml(disc.predominant_dimension)} em destaque</strong><p>Sua dimensao predominante</p></div></div><div class="disc-bars">${bars}</div></div>`;
  profileElement.innerHTML = `<div class="disc-comparison-grid"><div><h4>Inicial</h4><p class="muted">Resultado do quiz narrativo.</p>${renderDiscScores(disc.scores)}</div><div><h4>Observado</h4><p class="muted">Calculado pelas atividades realizadas.</p>${renderDiscScores(window.dashboardProfile?.observed_disc_result?.scores)}</div></div>`;
};

const renderDiscScores = (scores) => {
  if (!scores) return '<p class="muted">Aguardando atividades.</p>';
  return `<div class="disc-score-grid">${Object.entries(scores).map(([key, value]) => `<div><strong>${escapeHtml(key)}</strong><span>${escapeHtml(value)} pts</span></div>`).join("")}</div>`;
};

const renderMissions = (missions) => {
  const active = missions.find((mission) => mission.status !== "Concluida") || missions[missions.length - 1];
  const activeElement = document.querySelector("#active-mission");
  if (!active) activeElement.innerHTML = '<p class="mission-empty">Suas proximas conquistas aparecerao aqui.</p>';
  else activeElement.innerHTML = `<span class="mission-status">${symbol("mission", "sd-record-icon")}${escapeHtml(active.status === "Pendente" ? "Disponivel agora" : active.status)}</span><h3>${escapeHtml(active.nome)}</h3><p>${escapeHtml(active.descricao)}</p><div class="mission-reward"><span>Recompensa</span><strong>${symbol("xp")}${escapeHtml(active.xp_recompensa)} XP</strong></div>`;

  const next = missions.filter((mission) => mission !== active && mission.status !== "Concluida").slice(0, 3);
  document.querySelector("#next-missions").innerHTML = next.length ? next.map((mission, index) => `<article class="mission-small card"><span class="mission-number" aria-label="Missão ${index + 2}">${symbol("mission")}</span><div><h3>${escapeHtml(mission.nome)}</h3><p>${escapeHtml(mission.descricao)}</p></div><strong>${symbol("xp", "sd-record-icon")}+${escapeHtml(mission.xp_recompensa)} XP</strong></article>`).join("") : '<p class="muted">Voce esta em dia. Continue registrando suas evidencias no Curriculo Vivo.</p>';
  document.querySelector("#mission-list").innerHTML = missions.length ? missions.map((mission) => `<article class="workspace-record-card mission-record ${mission.status === "Concluida" ? "is-complete" : ""}"><div class="record-main"><span class="mission-status">${symbol(mission.status === "Concluida" ? "achievement" : "mission", "sd-record-icon")}${escapeHtml(mission.status)}</span><h3>${escapeHtml(mission.nome)}</h3><p>${escapeHtml(mission.descricao)}</p>${mission.data_conclusao ? `<small>Concluida em ${escapeHtml(formatDate(mission.data_conclusao))}</small>` : ""}</div><strong class="record-reward">${symbol("xp")}${escapeHtml(mission.xp_recompensa)} XP</strong></article>`).join("") : '<p class="empty-state">Nenhuma missao disponivel no momento.</p>';
};

const renderCollections = (projects, certificates) => {
  document.querySelector("#project-count").textContent = `${projects.length} ${projects.length === 1 ? "projeto registrado" : "projetos registrados"}`;
  document.querySelector("#certificate-count").textContent = `${certificates.length} ${certificates.length === 1 ? "certificado registrado" : "certificados registrados"}`;
  document.querySelector("#project-preview").innerHTML = projects.slice(0, 2).map((project) => `<span>${escapeHtml(project.titulo)}</span>`).join("");
  document.querySelector("#certificate-preview").innerHTML = certificates.slice(0, 2).map((certificate) => `<span>${escapeHtml(certificate.nome)}</span>`).join("");
  document.querySelector("#project-list").innerHTML = projects.length ? projects.map(renderProject).join("") : '<div class="empty-state"><p>Seu Curriculo Vivo ainda nao tem projetos.</p><button class="button button-soft" type="button" data-open-dialog="project-dialog">Adicionar primeiro projeto</button></div>';
  document.querySelector("#certificate-list").innerHTML = certificates.length ? certificates.map(renderCertificate).join("") : '<div class="empty-state"><p>Seus certificados aparecerao aqui.</p><button class="button button-soft" type="button" data-open-dialog="certificate-dialog">Adicionar primeiro certificado</button></div>';
};

const renderProject = (project) => `<article class="workspace-record-card"><div class="record-main"><p class="eyebrow">${symbol("project", "sd-record-icon")}PROJETO</p><h3>${escapeHtml(project.titulo)}</h3><p>${escapeHtml(project.descricao)}</p><p class="record-meta"><strong>Tecnologias</strong> ${escapeHtml(project.tecnologias)}</p>${project.link ? `<a class="record-link" href="${escapeHtml(project.link)}" target="_blank" rel="noopener">Abrir projeto <span aria-hidden="true">↗</span></a>` : ""}<small>Adicionado em ${escapeHtml(formatDate(project.created_at))}</small></div><div class="record-actions"><button class="button button-ghost" type="button" data-edit="project" data-id="${project.id}">Editar</button><button class="button button-danger-ghost" type="button" data-delete="project" data-id="${project.id}">Excluir</button></div></article>`;

const renderCertificate = (certificate) => `<article class="workspace-record-card"><div class="record-main"><p class="eyebrow">${symbol("certificate", "sd-record-icon")}CERTIFICADO</p><h3>${escapeHtml(certificate.nome)}</h3><p>${escapeHtml(certificate.instituicao)}</p><p class="record-meta"><strong>${escapeHtml(certificate.carga_horaria)}h</strong> · Concluido em ${escapeHtml(formatDate(certificate.data_conclusao))}</p>${certificate.arquivo_path ? `<a class="record-link" href="/certificados/${certificate.id}/arquivo" target="_blank" rel="noopener">Abrir arquivo <span aria-hidden="true">↗</span></a>` : ""}<small>Adicionado em ${escapeHtml(formatDate(certificate.created_at))}</small></div><div class="record-actions"><button class="button button-ghost" type="button" data-edit="certificate" data-id="${certificate.id}">Editar</button><button class="button button-danger-ghost" type="button" data-delete="certificate" data-id="${certificate.id}">Excluir</button></div></article>`;

const renderAchievements = (achievements) => {
  const unlocked = achievements?.unlocked || [];
  const count = `${unlocked.length} de ${achievements?.total_count || 0} desbloqueadas`;
  document.querySelector("#achievement-count").textContent = count;
  const content = unlocked.length ? unlocked.map((achievement) => `<article class="achievement-dashboard-card card"><span class="achievement-icon">${symbol("achievement")}</span><div><h3>${symbol(achievementSymbols[achievement.achievement_key] || "achievement", "sd-record-icon")}${escapeHtml(achievement.nome)}</h3><p>${escapeHtml(achievement.descricao)}</p><small>${escapeHtml(formatDate(achievement.data_desbloqueio))}</small></div></article>`).join("") : '<p class="empty-state">Suas conquistas aparecem aqui conforme voce evolui.</p>';
  document.querySelector("#achievement-list").innerHTML = content;
  document.querySelector("#dashboard-achievement-list").innerHTML = unlocked.length ? unlocked.slice(0, 3).map((achievement) => `<article class="achievement-dashboard-card card"><span class="achievement-icon">${symbol("achievement")}</span><div><h3>${symbol(achievementSymbols[achievement.achievement_key] || "achievement", "sd-record-icon")}${escapeHtml(achievement.nome)}</h3><p>${escapeHtml(achievement.descricao)}</p></div></article>`).join("") : '<p class="muted">Suas conquistas aparecem automaticamente conforme voce evolui.</p>';
};

const renderEvolutionHistory = (history) => history?.length
  ? history.map((event) => `<article class="activity-dashboard-card card"><span>${symbol("evolution", "sd-record-icon")}${escapeHtml(event.titulo)}</span><strong>${escapeHtml(event.descricao)}</strong><small>${escapeHtml(formatDate(event.created_at))}</small></article>`).join("")
  : '<p class="muted">Nenhuma atividade registrada ainda.</p>';

const renderEvolution = (evolution) => {
  if (!evolution) return;
  const { level, indicators, history } = evolution;
  const nextText = level.next ? `${level.xp_to_next} XP para o Nivel ${level.next}` : "Nivel maximo alcancado";
  document.querySelector("#dashboard-xp").textContent = indicators.xp_current;
  document.querySelector("#dashboard-level").innerHTML = `${symbol("level")}Nivel ${escapeHtml(level.current)}`;
  document.querySelector("#dashboard-progress").style.width = `${level.progress_percent}%`;
  document.querySelector("#dashboard-progress-caption").innerHTML = `<strong>${symbol("xp", "sd-record-icon")}${escapeHtml(indicators.xp_current)} XP</strong> acumulados - ${escapeHtml(nextText)}`;
  document.querySelector("#evolution-projects").textContent = indicators.projects_created;
  document.querySelector("#evolution-certificates").textContent = indicators.certificates_added;
  document.querySelector("#evolution-missions").textContent = indicators.missions_completed;
  document.querySelector("#evolution-achievements").textContent = indicators.achievements_unlocked;
  document.querySelector("#evolution-xp").textContent = indicators.xp_current;
  document.querySelector("#profile-xp").textContent = indicators.xp_current;
  document.querySelector("#evolution-level-title").innerHTML = `${symbol("level", "sd-heading-icon")}Nivel ${escapeHtml(level.current)}`;
  document.querySelector("#evolution-level-copy").textContent = nextText;
  document.querySelector("#evolution-progress").style.width = `${level.progress_percent}%`;
  document.querySelector("#evolution-progress-caption").textContent = `${level.progress_percent}% de progresso`;
  document.querySelector("#detail-projects").textContent = indicators.projects_created;
  document.querySelector("#detail-certificates").textContent = indicators.certificates_added;
  document.querySelector("#detail-missions").textContent = indicators.missions_completed;
  document.querySelector("#detail-achievements").textContent = indicators.achievements_unlocked;
  document.querySelector("#detail-xp").textContent = indicators.xp_current;
  const renderedHistory = renderEvolutionHistory(history);
  document.querySelector("#history-list").innerHTML = renderedHistory;
  document.querySelector("#evolution-history").innerHTML = renderedHistory;
};

const loadDashboard = async () => {
  const [profileResponse, missionsResponse] = await Promise.all([fetch("/perfil/json"), fetch("/missoes/json")]);
  if (!profileResponse.ok || !missionsResponse.ok) throw new Error("Nao foi possivel carregar o painel.");
  const profile = await profileResponse.json();
  const missions = (await missionsResponse.json()).missions || [];
  window.dashboardProfile = profile;
  const { user, disc_result: disc, projects = [], certificates = [], achievements, evolution } = profile;
  document.querySelector("#profile-email").textContent = user.email || "-";
  document.querySelector("#profile-created").textContent = formatDate(user.created_at);
  renderDisc(disc);
  renderMissions(missions);
  renderCollections(projects, certificates);
  renderAchievements(achievements);
  renderEvolution(evolution);
};

const openDialog = (type, record = null) => {
  const dialog = document.querySelector(`#${type}-dialog`);
  const form = document.querySelector(`#${type}-form`);
  form.reset();
  form.dataset.recordId = record?.id || "";
  form.querySelector(".dialog-error").textContent = "";
  const title = document.querySelector(`#${type}-dialog-title`);
  title.textContent = `${record ? "Editar" : "Adicionar"} ${type === "project" ? "projeto" : "certificado"}`;
  if (record) Object.entries(record).forEach(([key, value]) => {
    const input = form.elements.namedItem(key);
    if (input && input.type !== "file" && value != null) input.value = value;
  });
  dialog.showModal();
};

const submitRecord = async (event, type) => {
  event.preventDefault();
  const form = event.currentTarget;
  const recordId = form.dataset.recordId;
  const endpoint = type === "project" ? "/projetos/" : "/certificados/";
  const url = recordId ? `${endpoint}${recordId}/editar` : endpoint;
  const isCertificate = type === "certificate";
  const options = isCertificate
    ? { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } }
    : { method: "POST", body: JSON.stringify(Object.fromEntries(new FormData(form))), headers: { "Content-Type": "application/json", Accept: "application/json" } };
  const submitButton = form.querySelector('[type="submit"]');
  submitButton.disabled = true;
  try {
    const response = await fetch(url, options);
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Nao foi possivel salvar este registro.");
    document.querySelector(`#${type}-dialog`).close();
    await loadDashboard();
    showFeedback(`${type === "project" ? "Projeto" : "Certificado"} ${recordId ? "atualizado" : "adicionado"} com sucesso.`);
  } catch (error) {
    form.querySelector(".dialog-error").textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
};

const removeRecord = async (type, recordId) => {
  const label = type === "project" ? "projeto" : "certificado";
  if (!window.confirm(`Excluir este ${label}?`)) return;
  try {
    const endpoint = type === "project" ? "/projetos/" : "/certificados/";
    const response = await fetch(`${endpoint}${recordId}/excluir`, { method: "POST", headers: { Accept: "application/json" } });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || `Nao foi possivel excluir o ${label}.`);
    await loadDashboard();
    showFeedback(`${label[0].toUpperCase()}${label.slice(1)} excluido com sucesso.`);
  } catch (error) {
    showFeedback(error.message, true);
  }
};

if (document.body.classList.contains("dashboard-page")) {
  document.querySelectorAll(".workspace-tab").forEach((tab) => tab.addEventListener("click", () => setTab(tab.dataset.tab)));
  document.querySelectorAll("[data-open-tab]").forEach((button) => button.addEventListener("click", () => {
    setTab(button.dataset.openTab);
    document.querySelector(`#tab-${button.dataset.openTab}`).focus();
  }));
  document.querySelectorAll(".workspace-tab").forEach((tab) => tab.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
    event.preventDefault();
    const tabs = [...document.querySelectorAll(".workspace-tab")];
    const current = tabs.indexOf(tab);
    const next = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (current + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
    setTab(tabs[next].dataset.tab);
    tabs[next].focus();
  }));
  document.addEventListener("click", (event) => {
    const openButton = event.target.closest("[data-open-dialog]");
    if (openButton) openDialog(openButton.dataset.openDialog.replace("-dialog", ""));
    const closeButton = event.target.closest("[data-close-dialog]");
    if (closeButton) closeButton.closest("dialog").close();
    const editButton = event.target.closest("[data-edit]");
    if (editButton) {
      const type = editButton.dataset.edit;
      const records = type === "project" ? window.dashboardProfile.projects : window.dashboardProfile.certificates;
      openDialog(type, records.find((record) => String(record.id) === editButton.dataset.id));
    }
    const deleteButton = event.target.closest("[data-delete]");
    if (deleteButton) removeRecord(deleteButton.dataset.delete, deleteButton.dataset.id);
  });
  document.querySelector("#project-form").addEventListener("submit", (event) => submitRecord(event, "project"));
  document.querySelector("#certificate-form").addEventListener("submit", (event) => submitRecord(event, "certificate"));
  loadDashboard().catch(() => document.querySelectorAll(".loading-state").forEach((element) => { element.textContent = "Nao foi possivel carregar os dados agora."; }));
}
