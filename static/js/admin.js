const adminDict = {
    es: { btn: "Panel de Administraci\u00f3n", modalTitle: "Usuarios", consultTitle: "Historial", noData: "Sin datos", loading: "Cargando...", patient: "Paciente", diagnosis: "Diagn\u00f3sticos R\u00e1pidos", lab: "Entrenamientos", deleteBtn: "Eliminar", renameBtn: "Renombrar", status: "Estado", progress: "Progreso", model: "Modelo", date: "Fecha", save: "Guardar", cancel: "Cancelar", confirmDelete: "\u00bfEliminar esta consulta?", deleted: "Eliminado", renamed: "Renombrado", renamePrompt: "Nuevo nombre del paciente:", labsTitle: "Sesiones de Laboratorio", sessionId: "Sesi\u00f3n", deleteLabConfirm: "\u00bfEliminar esta sesi\u00f3n de laboratorio?", labDeleted: "Sesi\u00f3n eliminada", open: "Abrir" },
    en: { btn: "Administration Panel", modalTitle: "Users", consultTitle: "History", noData: "No data", loading: "Loading...", patient: "Patient", diagnosis: "Quick Diagnoses", lab: "Training Sessions", deleteBtn: "Delete", renameBtn: "Rename", status: "Status", progress: "Progress", model: "Model", date: "Date", save: "Save", cancel: "Cancel", confirmDelete: "Delete this consultation?", deleted: "Deleted", renamed: "Renamed", renamePrompt: "New patient name:", labsTitle: "Lab Sessions", sessionId: "Session", deleteLabConfirm: "Delete this lab session?", labDeleted: "Session deleted", open: "Open" },
    zh: { btn: "\u7ba1\u7406\u9762\u677f", modalTitle: "\u7528\u6237", consultTitle: "\u5386\u53f2", noData: "\u65e0\u6570\u636e", loading: "\u52a0\u8f7d\u4e2d...", patient: "\u60a3\u8005", diagnosis: "\u5feb\u901f\u8bca\u65ad", lab: "\u8bad\u7ec3\u4f1a\u8bdd", deleteBtn: "\u5220\u9664", renameBtn: "\u91cd\u547d\u540d", status: "\u72b6\u6001", progress: "\u8fdb\u5ea6", model: "\u6a21\u578b", date: "\u65e5\u671f", save: "\u4fdd\u5b58", cancel: "\u53d6\u6d88", confirmDelete: "\u5220\u9664\u6b64\u54a8\u8be2\uff1f", deleted: "\u5df2\u5220\u9664", renamed: "\u5df2\u91cd\u547d\u540d", renamePrompt: "\u60a3\u8005\u65b0\u540d\u79f0:", labsTitle: "\u5b9e\u9a8c\u5ba4\u4f1a\u8bdd", sessionId: "\u4f1a\u8bdd", deleteLabConfirm: "\u5220\u9664\u6b64\u5b9e\u9a8c\u5ba4\u4f1a\u8bdd\uff1f", labDeleted: "\u4f1a\u8bdd\u5df2\u5220\u9664", open: "\u6253\u5f00" },
    hi: { btn: "\u092a\u094d\u0930\u0936\u093e\u0938\u0928 \u092a\u0948\u0928\u0932", modalTitle: "\u0909\u092a\u092f\u094b\u0917\u0915\u0930\u094d\u0924\u093e", consultTitle: "\u0907\u0924\u093f\u0939\u093e\u0938", noData: "\u0915\u094b\u0908 \u0921\u0947\u091f\u093e \u0928\u0939\u0940\u0902", loading: "\u0932\u094b\u0921 \u0939\u094b \u0930\u0939\u093e \u0939\u0948...", patient: "\u0930\u094b\u0917\u0940", diagnosis: "\u0924\u094d\u0935\u0930\u093f\u0924 \u0928\u093f\u0926\u093e\u0928", lab: "\u092a\u094d\u0930\u0936\u093f\u0915\u094d\u0937\u0923 \u0938\u0924\u094d\u0930", deleteBtn: "\u0939\u091f\u093e\u090f\u0902", renameBtn: "\u0928\u092e \u092c\u0926\u0932\u0947\u0902", status: "\u0938\u094d\u0925\u093f\u0924\u093f", progress: "\u092a\u094d\u0930\u0917\u0924\u093f", model: "\u092e\u0949\u0921\u0932", date: "\u0924\u093e\u0930\u0940\u0916", save: "\u0938\u0939\u0947\u091c\u0947\u0902", cancel: "\u0930\u0926\u094d\u0926 \u0915\u0930\u0947\u0902", confirmDelete: "\u0915\u094d\u092f\u093e \u0907\u0938 \u092a\u0930\u093e\u092e\u0930\u094d\u0936 \u0915\u094b \u0939\u091f\u093e\u090f\u0902?", deleted: "\u0939\u091f\u093e \u0926\u093f\u092f\u093e", renamed: "\u0928\u092e \u092c\u0926\u0932 \u0926\u093f\u092f\u093e", renamePrompt: "\u0930\u094b\u0917\u0940 \u0915\u093e \u0928\u092f\u093e \u0928\u093e\u092e:", labsTitle: "\u092a\u094d\u0930\u092f\u094b\u0917\u0936\u093e\u0932\u093e \u0938\u0924\u094d\u0930", sessionId: "\u0938\u0924\u094d\u0930", deleteLabConfirm: "\u0915\u094d\u092f\u093e \u0907\u0938 \u092a\u094d\u0930\u092f\u094b\u0917\u0936\u093e\u0932\u093e \u0938\u0924\u094d\u0930 \u0915\u094b \u0939\u091f\u093e\u090f\u0902?", labDeleted: "\u0938\u0924\u094d\u0930 \u0939\u091f\u093e \u0926\u093f\u092f\u093e", open: "\u0916\u094b\u0932\u0947\u0902" }
};

var _currentAdminUserId = null;
var _currentAdminUserName = null;
var _renameConsultationId = null;

function getAdminLang() {
    var lang = localStorage.getItem('appLang') || 'es';
    return adminDict[lang] || adminDict.es;
}

function isOnDashboard() {
    return document.getElementById('chat-box') !== null;
}

function isOnTraining() {
    return typeof viewSessionResults === 'function';
}

window.openAdminUsersModal = async function () {
    const t = getAdminLang();
    var titleEl = document.getElementById('ui-admin-modal-title');
    var listEl = document.getElementById('admin-users-list');
    var modalEl = document.getElementById('admin-users-modal');
    if (!modalEl) return;
    if (titleEl) titleEl.innerText = t.modalTitle;
    listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t.loading + '</p>';
    modalEl.classList.remove('hidden');
    try {
        var resp = await fetch('/api/admin/users?t=' + Date.now());
        var result = await resp.json();
        if (result.status === "success" && result.users.length > 0) {
            var html = '';
            result.users.forEach(function (u) {
                var name = (u.first_name + ' ' + u.last_name).replace(/'/g, "\\'");
                html += '<div onclick="window.openAdminUserConsultationsModal(' + u.id + ',\'' + name + '\')" class="flex items-center justify-between p-3 rounded-xl cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"><div><p class="text-sm font-bold text-gray-800 dark:text-white">' + u.first_name + ' ' + u.last_name + '</p><p class="text-xs text-gray-500">@' + u.username + ' &middot; ' + u.role + '</p></div><div class="flex gap-3 text-right"><div><p class="text-lg font-black text-blue-600 dark:text-blue-400">' + u.diagnosis_count + '</p><p class="text-[10px] text-gray-400">diag.</p></div><div><p class="text-lg font-black text-purple-600 dark:text-purple-400">' + u.lab_count + '</p><p class="text-[10px] text-gray-400">lab.</p></div></div></div>';
            });
            listEl.innerHTML = html;
        } else {
            listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t.noData + '</p>';
        }
    } catch (e) {
        listEl.innerHTML = '<p class="text-sm text-red-500">Error</p>';
    }
};

window.closeAdminUsersModal = function () {
    var el = document.getElementById('admin-users-modal');
    if (el) el.classList.add('hidden');
};

function buildConsultationCard(item, t) {
    var lbl = item.prediction_label;
    var p = (item.original_image_path || '').replace(/\\/g, '/');
    var isPneu = item.prediction_label === "Neumon\u00eda";
    var colorClass = isPneu ? 'text-red-500' : 'text-green-500';
    var closeModals = 'window.closeAdminUsersModal();window.closeAdminUserConsultationsModal();';
    var onclickAttr;
    if (isOnDashboard()) {
        onclickAttr = closeModals + 'window.adminReviewConsultation(' + item.id + ',\'' + p.replace(/'/g, "\\'") + '\',\'' + (item.xai_image_path || '').replace(/\\/g, '/').replace(/'/g, "\\'") + '\',\'' + item.prediction_label + '\',' + item.confidence_score + ',\'' + (item.model_name || '').replace(/'/g, "\\'") + '\',\'' + (item.patient_name || '').replace(/'/g, "\\'") + '\')';
    } else {
        onclickAttr = closeModals + 'window.location.href=\'/dashboard?cid=' + item.id + '\'';
    }
    return '<div onclick="' + onclickAttr + '" class="bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer">'
        + '<div class="flex gap-3">'
        + '<img src="/' + p + '" class="w-14 h-14 object-cover rounded-lg cursor-pointer" onclick="event.stopPropagation();window.openImageModal(\'/' + p + '\')">'
        + '<div class="flex-1 min-w-0">'
        + '<p class="text-xs text-gray-500">' + item.timestamp + '</p>'
        + '<p class="text-sm font-black ' + colorClass + '">' + lbl + ' (' + item.confidence_score + '%)</p>'
        + '<p class="text-xs text-gray-400 truncate">' + t.patient + ': <span id="ptname-' + item.id + '">' + (item.patient_name || '\u2014') + '</span></p>'
        + '<p class="text-xs text-gray-500">' + item.model_name + '</p>'
        + '</div>'
        + '<div class="flex flex-col gap-1 flex-shrink-0">'
        + '<button onclick="event.stopPropagation();window.adminShowRenamePrompt(' + item.id + ',\'' + (item.patient_name || '').replace(/'/g, "\\'") + '\')" class="text-blue-400 hover:text-blue-600 text-xs" title="' + t.renameBtn + '"><i class="fa-solid fa-pen"></i></button>'
        + '<button onclick="event.stopPropagation();window.adminDeleteConsultation(' + item.id + ')" class="text-red-400 hover:text-red-600 text-xs" title="' + t.deleteBtn + '"><i class="fa-solid fa-trash-can"></i></button>'
        + '</div>'
        + '</div>'
        + '</div>';
}

window.adminReviewConsultation = function (id, imgPath, xaiPath, label, confidence, model, patient) {
    if (typeof window.openConsultationDetail === 'function') {
        window.openConsultationDetail(id, imgPath, xaiPath, label, confidence, model, patient, '');
    }
};

window.adminShowRenamePrompt = function (consultationId, currentName) {
    _renameConsultationId = consultationId;
    const t = getAdminLang();
    var modal = document.getElementById('rename-prompt-modal');
    if (!modal) {
        var div = document.createElement('div');
        div.id = 'rename-prompt-modal';
        div.setAttribute('style', 'position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center');
        div.innerHTML = '<div id="rename-prompt-inner"></div>';
        document.body.appendChild(div);
        div.addEventListener('click', function (e) { if (e.target === div) window.adminCancelRename(); });
    }
    var inner = document.getElementById('rename-prompt-inner');
    if (inner) {
        var isDark = document.documentElement.classList.contains('dark');
        var bgColor = isDark ? '#1f2937' : 'white';
        var textColor = isDark ? '#e5e7eb' : '#374151';
        var borderColor = isDark ? '#374151' : '#e5e7eb';
        var inputBg = isDark ? '#374151' : 'white';
        var inputText = isDark ? '#e5e7eb' : '#111827';
        var inputBorder = isDark ? '#4b5563' : '#d1d5db';
        var btnCancelBg = isDark ? '#374151' : '#f3f4f6';
        var btnCancelText = isDark ? '#d1d5db' : '#374151';
        inner.innerHTML = '<div style="background:' + bgColor + ';border-radius:16px;padding:24px;margin:16px;max-width:400px;width:100%;border:1px solid ' + borderColor + ';box-shadow:0 25px 50px rgba(0,0,0,0.25)">'
            + '<p style="font-size:14px;font-weight:700;color:' + textColor + ';margin-bottom:12px">' + t.renamePrompt + '</p>'
            + '<input id="rename-prompt-input" type="text" style="width:100%;border:1px solid ' + inputBorder + ';border-radius:8px;padding:8px 12px;font-size:14px;margin-bottom:16px;box-sizing:border-box;background:' + inputBg + ';color:' + inputText + '" value="' + (currentName || '').replace(/"/g, '&quot;') + '">'
            + '<div style="display:flex;justify-content:flex-end;gap:8px"><button onclick="window.adminCancelRename()" style="padding:8px 16px;font-size:14px;border-radius:8px;border:none;cursor:pointer;background:' + btnCancelBg + ';color:' + btnCancelText + '">' + t.cancel + '</button><button onclick="window.adminConfirmRename()" style="padding:8px 16px;font-size:14px;border-radius:8px;border:none;cursor:pointer;background:#2563eb;color:white;font-weight:600">' + t.save + '</button></div>'
            + '</div>';
    }
    var input = document.getElementById('rename-prompt-input');
    if (input) { input.value = currentName || ''; }
    document.getElementById('rename-prompt-modal').classList.remove('hidden');
    document.getElementById('rename-prompt-modal').style.display = 'flex';
    if (input) { setTimeout(function () { input.focus(); input.select(); }, 100); }
};

window.adminCancelRename = function () {
    var el = document.getElementById('rename-prompt-modal');
    if (el) { el.classList.add('hidden'); el.style.display = 'none'; }
    _renameConsultationId = null;
};

window.adminConfirmRename = function () {
    var input = document.getElementById('rename-prompt-input');
    var newName = input ? input.value.trim() : '';
    if (!newName || _renameConsultationId === null) return;
    window.adminDoRename(_renameConsultationId, newName);
    window.adminCancelRename();
};

window.adminDoRename = async function (consultationId, newName) {
    const t = getAdminLang();
    try {
        var formData = new FormData();
        formData.append('consultation_id', consultationId);
        formData.append('new_name', newName);
        var resp = await fetch('/api/history/update_name', { method: 'POST', body: formData });
        if (resp.ok) {
            var el = document.getElementById('ptname-' + consultationId);
            if (el) el.innerText = newName;
            var cdPatient = document.getElementById('cd-patient');
            if (cdPatient && consultationId === window._cdId) cdPatient.innerText = newName;
            if (typeof loadHistory === 'function') loadHistory();
        }
    } catch (e) {}
};

async function refreshCurrentAdminConsultations() {
    if (_currentAdminUserId === null) return;
    await window.openAdminUserConsultationsModal(_currentAdminUserId, _currentAdminUserName);
}

window.openAdminUserConsultationsModal = async function (userId, userName) {
    _currentAdminUserId = userId;
    _currentAdminUserName = userName;
    const t = getAdminLang();
    var titleEl = document.getElementById('ui-admin-consult-modal-title');
    var listEl = document.getElementById('admin-user-consultations-list');
    var modalEl = document.getElementById('admin-user-consultations-modal');
    if (!modalEl) return;
    if (titleEl) titleEl.innerHTML = t.consultTitle + ': ' + userName;
    listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t.loading + '</p>';
    modalEl.classList.remove('hidden');
    try {
        var resp = await fetch('/api/admin/users/' + userId + '/consultations?t=' + Date.now());
        var result = await resp.json();
        if (resp.status === 404) {
            listEl.innerHTML = '<p class="text-sm text-red-500 italic">Usuario no encontrado</p>';
            return;
        }
        var html = '';

        html += '<div class="mb-4"><h3 class="text-sm font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-2"><i class="fa-solid fa-stethoscope mr-1"></i> ' + t.diagnosis + '</h3>';
        if (result.consultations && result.consultations.length > 0) {
            result.consultations.forEach(function (item) {
                html += buildConsultationCard(item, t);
            });
        } else {
            html += '<p class="text-sm text-gray-400 italic">' + t.noData + '</p>';
        }
        html += '</div>';

        html += '<div><h3 class="text-sm font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider mb-2"><i class="fa-solid fa-flask mr-1"></i> ' + t.lab + '</h3>';
        if (result.training_sessions && result.training_sessions.length > 0) {
            result.training_sessions.forEach(function (sess) {
                var onclickSession = isOnTraining()
                    ? 'window.closeAdminUsersModal();window.closeAdminUserConsultationsModal();viewSessionResults(\'' + sess.session_id + '\')'
                    : 'window.closeAdminUsersModal();window.closeAdminUserConsultationsModal();window.location.href=\'/training?session=' + sess.session_id + '\'';
                html += '<div onclick="' + onclickSession + '" class="bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 mb-2 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer"><div class="flex justify-between items-center"><div><p class="text-sm font-bold text-gray-800 dark:text-white">' + t.sessionId + ': ' + sess.session_id + '</p><p class="text-xs text-gray-500">' + t.model + ': ' + sess.models.join(', ') + '</p><p class="text-xs text-gray-400">' + sess.models.length + ' ' + t.model.toLowerCase() + '(s)</p></div><div class="flex gap-2"><span class="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-2 py-1 rounded-full font-semibold">' + t.open + '</span></div></div></div>';
            });
        } else {
            html += '<p class="text-sm text-gray-400 italic">' + t.noData + '</p>';
        }
        html += '</div>';

        listEl.innerHTML = html;
    } catch (e) {
        listEl.innerHTML = '<p class="text-sm text-red-500">Error</p>';
    }
};

window.closeAdminUserConsultationsModal = function () {
    _currentAdminUserId = null;
    _currentAdminUserName = null;
    var el = document.getElementById('admin-user-consultations-modal');
    if (el) el.classList.add('hidden');
};

async function pollQueue() {
    try {
        var resp = await fetch('/api/queue/status?t=' + Date.now());
        var data = await resp.json();
        var panel = document.getElementById('queue-panel');
        var items = document.getElementById('queue-items');
        if (!panel || !items) return;
        if (data.status === "success" && data.has_pending) {
            panel.classList.remove('hidden');
            var html = '';
            data.jobs.forEach(function (j) {
                if (j.status === 'queued' || j.status === 'running') {
                    var icon = j.job_type === 'diagnosis' ? 'fa-stethoscope' : 'fa-flask';
                    var label = j.job_type === 'diagnosis' ? 'Diagn\u00f3stico' : 'Entrenamiento';
                    var statusText = j.status === 'running' ? 'Procesando...' : ('Posici\u00f3n #' + (j.position || '?'));
                    var statusColor = j.status === 'running' ? 'text-green-500' : 'text-blue-500';
                    var tooltip = j.job_type === 'diagnosis' ? 'Modelo: ' + (j.model_name || '?') : 'Sesi\u00f3n: ' + (j.session_id || '?');
                    var delBtn = j.status === 'queued' ? '<button onclick="window.cancelQueueJob(' + j.id + ')" class="text-red-400 hover:text-red-600 text-xs ml-1" title="Cancelar"><i class="fa-solid fa-trash-can"></i></button>' : '';
                    html += '<div class="flex items-center gap-2 text-xs group relative" title="' + tooltip + '"><i class="fa-solid ' + icon + ' text-gray-400"></i><span class="text-gray-700 dark:text-gray-300 truncate max-w-[100px]">' + label + '</span><span class="ml-auto ' + statusColor + ' font-semibold">' + statusText + '</span>' + delBtn + '</div>';
                }
            });
            items.innerHTML = html || '<p class="text-xs text-gray-400 italic">Sin trabajos pendientes</p>';
        } else {
            panel.classList.add('hidden');
        }
    } catch (e) {}
}

window.cancelQueueJob = async function (jobId) {
    if (!confirm('\u00bfCancelar este trabajo?')) return;
    try {
        await fetch('/api/queue/cancel/' + jobId, { method: 'DELETE' });
    } catch (e) {}
};

setInterval(pollQueue, 5000);
setTimeout(pollQueue, 500);

window.adminDeleteConsultation = async function (consultationId) {
    const t = getAdminLang();
    if (!confirm(t.confirmDelete)) return;
    try {
        var formData = new FormData();
        formData.append('consultation_id', consultationId);
        var resp = await fetch('/api/history/delete', { method: 'POST', body: formData });
        if (resp.ok) {
            var detailPanel = document.getElementById('consultation-detail-panel');
            if (detailPanel && !detailPanel.classList.contains('hidden')) {
                if (typeof window.closeConsultationDetail === 'function') window.closeConsultationDetail();
                if (typeof loadHistory === 'function') loadHistory();
            }
            await refreshCurrentAdminConsultations();
        }
    } catch (e) {}
};
