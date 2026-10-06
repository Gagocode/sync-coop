const professionalForm = document.querySelector("#dashboard-professional-form");

if (professionalForm) {
  professionalForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const status = document.querySelector("#dashboard-professional-status");
    const button = professionalForm.querySelector('[type="submit"]');
    button.disabled = true;
    status.hidden = true;

    try {
      const response = await fetch(professionalForm.action, {
        method: "POST",
        body: new FormData(professionalForm),
        headers: { Accept: "application/json" },
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Não foi possível salvar as informações.");

      status.textContent = "Informações profissionais salvas.";
      status.className = "professional-message professional-success";
      document.querySelector("#dashboard-resume-link").hidden = !result.professional_profile.curriculo_path;
      professionalForm.elements.curriculo.value = "";
    } catch (error) {
      status.textContent = error.message || "Não foi possível salvar as informações.";
      status.className = "professional-message professional-error";
    } finally {
      status.hidden = false;
      button.disabled = false;
    }
  });
}
