# Task Plan

## Status
`closed`

## Task
- ID: TASK-008
- Title: Sistema de internacionalización unificado
- Backlog source: `agents/task/backlog.md`

## Summary
Implementar un sistema i18n completo y homogéneo en toda la aplicación. Actualmente el training page carece de i18n (dict vacío, `changeLanguage()` vacío, sin selector de idioma), los mensajes del backend están hardcodeados en español, y los PDFs/gráficos XAI/labels de predicción no son traducibles.

## Scope
**In:**
- Crear `static/js/i18n.js` con diccionario compartido para los 4 idiomas (es, en, zh, hi)
- Refactorizar dashboard.js, admin.js y training.js para usar el i18n.js compartido
- Implementar i18n en training.html: dict completo, changeLanguage() funcional, selector de idioma
- Traducir mensajes de error del backend (routers) vía cookie `appLang` + diccionario Python en `services/lang.py`
- Traducir labels de predicción ("Neumonía"/"Normal") según cookie `appLang` (ml_engine.py)
- Traducir títulos de gráficos XAI ("Radiografía Original", etc.) según cookie `appLang` (xai_generator.py)
- Traducir textos del PDF de diagnóstico (pdf_generator.py) según cookie `appLang`
- Añadir selector de idioma en training.html
- Traducir SYSTEM_PROMPT del chatbot a los 4 idiomas
- chatbot_service.py lee cookie `appLang` para seleccionar el prompt según idioma
- Unificar claves de traducción entre todas las páginas

**Out (explicitamente excluido):**
- Traducción del training_log.txt generado por scripts subprocess
- Traducción del PDF MLOps (pdf_generator_mlops.py) — es muy extenso y técnico
- Traducción de los scripts en `pneumoniacnn-main/` (son scripts de investigación independientes)
- Nuevos idiomas adicionales — se mantienen los 4 actuales (es, en, zh, hi)

## Current Behavior
- `training.js`: `const dict = { es: {}, en: {} };` — diccionario vacío
- `training.js`: `function changeLanguage() {}` — función vacía
- `training.html`: No tiene `<select id="lang-selector">` — no hay selector de idioma
- Todo el texto en training.html está hardcodeado en español
- `ml_engine.py:89`: `label = "Neumonía" if is_pneumonia else "Normal"` — siempre en español
- `dashboard.js:137`: Traducción manual solo para inglés mediante if ternario
- `pdf_generator.py`: "Reporte de Diagnóstico", "Fecha:", "Modelo de IA Utilizado:", "DIAGNOSTICO:", "Nivel de Confianza:", "Radiografia Original", "Mapa de Calor (XAI)" — siempre en español
- `xai_generator.py:129,134,139,145`: Títulos de matplotlib hardcodeados en español/inglés mixto
- `dashboard.js`, `admin.js`, `login.html`, `register.html`: Tienen sus propios dicts completos para 4 idiomas pero sin claves compartidas

## Target Behavior
- `static/js/i18n.js`: Diccionario único compartido con todos los textos de la aplicación para 4 idiomas
- `training.js`: Elimina su dict local, usa el i18n.js compartido. `changeLanguage()` funcional
- `dashboard.js` y `admin.js`: Eliminan sus dicts locales, usan el i18n.js compartido
- `training.html`: Selector de idioma visible, mismo estilo que en dashboard
- `services/lang.py`: Diccionario Python con textos del backend para 4 idiomas. Lee cookie `appLang` para seleccionar idioma
- `services/chatbot_service.py`: Traduce SYSTEM_PROMPT según cookie `appLang`. Lee `lang` del Request
- `routers/trainer.py`, `inference.py`, `auth.py`: Usan `lang.py` para traducir mensajes de error/respuesta
- `ml_engine.py`: Lee cookie `appLang` para devolver labels "Neumonía"/"Normal" traducidos
- `pdf_generator.py`: Lee cookie `appLang` para generar PDF en el idioma del usuario
- `xai_generator.py`: Lee cookie `appLang` para títulos de gráficos en el idioma del usuario
- Todas las páginas comparten el mismo i18n.js y el mismo patrón: función `t('clave')` + changeLanguage() + lang-selector

## Acceptance Criteria
- [ ] Training page tiene selector de idioma funcional con 4 idiomas
- [ ] Training page traduce todos sus textos visibles al cambiar idioma
- [ ] Labels de predicción ("Neumonía"/"Normal") se traducen según idioma
- [ ] Gráficos XAI muestran títulos en el idioma del usuario
- [ ] PDF de diagnóstico se genera en el idioma del usuario
- [ ] Selector de idioma persiste en localStorage (como ya hacen las demás páginas)
- [ ] Las traducciones de training page cubren: sidebar, header, chatbot, botones de acción, tabla de resultados, terminal section, modals
- [ ] Chatbot responde en el idioma seleccionado por el usuario (system prompt traducido + lenguaje natural del modelo)
- [ ] No se rompen las traducciones existentes en dashboard.js, admin.js, login.html, register.html

## Edge Cases
- Si el usuario cambia idioma mientras un proceso de diagnóstico/training está corriendo, los nuevos textos deben aparecer en el nuevo idioma
- Los PDFs ya generados no se retraducen (solo afecta a nuevos PDFs)
- Las imágenes XAI ya generadas no se retraducen (solo afecta a nuevas generaciones)
- El selector de idioma debe persistir entre páginas (mismo idioma en dashboard y training)

## Assumptions / Risks
- Los usuarios chinos (zh) e hindi (hi) prefieren español/inglés como fallback si alguna clave no está traducida
- Los 4 idiomas actuales son los definitivos para el TFG
- El diccionario de training.js tendrá ~40-50 claves nuevas; hay que mantener la consistencia con dashboard.js

## Database Impact
Not applicable.

## Open Questions
(Preguntas resueltas — ver sección Decisiones Tomadas abajo)

## Decisiones Tomadas
1. **Mensajes del backend**: Se traducen vía cookie `appLang` + diccionario Python en `services/lang.py`
2. **Mecanismo backend**: Los servicios (ml_engine, pdf_generator, xai_generator) leen la cookie `appLang` directamente, sin necesidad de parámetros extra en los routers
3. **Organización de dicts**: Archivo compartido `static/js/i18n.js` para todas las páginas. dashboard.js, admin.js y training.js lo usan
4. **PDF MLOps**: Se deja en español para mantener la tarea acotada

## Source of Truth to Read
- `agents/task/backlog.md`
- `agents/docs/DoD.md`
- `agents/docs/testing.md`
- `agents/docs/design.md`
- `agents/docs/api.md`
- `static/js/dashboard.js` (como referencia del patrón actual)
- `static/js/admin.js` (como referencia del patrón actual)
- `static/js/training.js` (objetivo principal)
- `templates/training.html` (objetivo principal)
- `services/ml_engine.py` (línea 89 — labels)
- `services/pdf_generator.py` (PDF diagnóstico)
- `services/xai_generator.py` (títulos matplotlib)
- `routers/trainer.py` (mensajes backend)
- `routers/inference.py` (mensajes backend)
- `routers/auth.py` (mensajes backend)

## Decision Records
- ADRs read from `agents/docs/decisions.md`: None directly relevant to i18n
- New decisions to record: Ninguna por ahora
