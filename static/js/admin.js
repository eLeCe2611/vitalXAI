(function() {
    const c = document.cookie.match(/csrf_token=([^;]+)/);
    if (!c) return;
    const csrfToken = c[1];
    const origFetch = window.fetch;
    let _isRefreshing = false;
    window.fetch = async function(url, options) {
        if (options && (options.method || 'GET').toUpperCase() !== 'GET') {
            options = Object.assign({}, options);
            options.headers = Object.assign({}, options.headers || {});
            options.headers['X-CSRF-Token'] = csrfToken;
        }
        let response = await origFetch(url, options);
        if (response.status === 401 && !_isRefreshing) {
            _isRefreshing = true;
            try {
                const refreshResp = await origFetch('/api/token/refresh', { method: 'POST', headers: { 'X-CSRF-Token': csrfToken } });
                if (refreshResp.ok) {
                    response = await origFetch(url, options);
                } else {
                    window.location.href = '/';
                    return response;
                }
            } catch (e) {
                window.location.href = '/';
            } finally {
                _isRefreshing = false;
            }
        }
        return response;
    };
})();

var _currentAdminUserId = null;
var _currentAdminUserName = null;
var _renameConsultationId = null;

function getAdminLang() {
    return window.t || (k=>k);
}

function isOnDashboard() {
    return document.getElementById('chat-box') !== null;
}

function isOnTraining() {
    return typeof viewSessionResults === 'function';
}

window.openAdminUsersModal = async function () {
    const t_ = getAdminLang();
    var titleEl = document.getElementById('ui-admin-modal-title');
    var listEl = document.getElementById('admin-users-list');
    var modalEl = document.getElementById('admin-users-modal');
    if (!modalEl) return;
    if (titleEl) titleEl.innerText = t_('adminModalTitle');
    listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t_('adminLoading') + '</p>';
    modalEl.classList.remove('hidden');
    try {
        var resp = await fetch('/api/admin/users?t=' + Date.now());
        var result = await resp.json();
        if (result.status === "success" && result.users.length > 0) {
            var html = '';
            result.users.forEach(function (u) {
                var name = (u.first_name + ' ' + u.last_name).replace(/'/g, "\\'");
                html += '<div onclick="window.openAdminUserConsultationsModal(' + u.id + ',\'' + name + '\')" class="flex items-center justify-between p-3 rounded-xl cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"><div><p class="text-sm font-bold text-gray-800 dark:text-white">' + u.first_name + ' ' + u.last_name + '</p><p class="text-xs text-gray-500">@' + u.username + ' &middot; ' + u.role + '</p></div><div class="flex gap-3 text-right"><div><p class="text-lg font-black text-blue-600 dark:text-blue-400">' + u.diagnosis_count + '</p><p class="text-[10px] text-gray-400">' + t_('adminDiagCount') + '</p></div><div><p class="text-lg font-black text-purple-600 dark:text-purple-400">' + u.lab_count + '</p><p class="text-[10px] text-gray-400">' + t_('adminLabCount') + '</p></div></div></div>';
            });
            listEl.innerHTML = html;
        } else {
            listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t_('adminNoData') + '</p>';
        }
    } catch (e) {
        listEl.innerHTML = '<p class="text-sm text-red-500">Error</p>';
    }
};

window.closeAdminUsersModal = function () {
    var el = document.getElementById('admin-users-modal');
    if (el) el.classList.add('hidden');
};

function buildConsultationCard(item, t_) {
    var lbl = item.prediction_label;
    var p = (item.original_image_path || '').replace(/\\/g, '/');
    var isPneu = item.prediction_label === "Neumonía";
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
        + '<p class="text-xs text-gray-400 truncate">' + t_('adminPatient') + ': <span id="ptname-' + item.id + '">' + (item.patient_name || '\u2014') + '</span></p>'
        + '<p class="text-xs text-gray-500">' + item.model_name + '</p>'
        + '</div>'
        + '<div class="flex flex-col gap-1 flex-shrink-0">'
        + '<button onclick="event.stopPropagation();window.adminShowRenamePrompt(' + item.id + ',\'' + (item.patient_name || '').replace(/'/g, "\\'") + '\')" class="text-blue-400 hover:text-blue-600 text-xs" title="' + t_('adminRenameBtn') + '"><i class="fa-solid fa-pen"></i></button>'
        + '<button onclick="event.stopPropagation();window.adminDeleteConsultation(' + item.id + ')" class="text-red-400 hover:text-red-600 text-xs" title="' + t_('adminDeleteBtn') + '"><i class="fa-solid fa-trash-can"></i></button>'
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
    const t_ = getAdminLang();
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
            + '<p style="font-size:14px;font-weight:700;color:' + textColor + ';margin-bottom:12px">' + t_('adminRenamePrompt') + '</p>'
            + '<input id="rename-prompt-input" type="text" style="width:100%;border:1px solid ' + inputBorder + ';border-radius:8px;padding:8px 12px;font-size:14px;margin-bottom:16px;box-sizing:border-box;background:' + inputBg + ';color:' + inputText + '" value="' + (currentName || '').replace(/"/g, '&quot;') + '">'
            + '<div style="display:flex;justify-content:flex-end;gap:8px"><button onclick="window.adminCancelRename()" style="padding:8px 16px;font-size:14px;border-radius:8px;border:none;cursor:pointer;background:' + btnCancelBg + ';color:' + btnCancelText + '">' + t_('adminCancel') + '</button><button onclick="window.adminConfirmRename()" style="padding:8px 16px;font-size:14px;border-radius:8px;border:none;cursor:pointer;background:#2563eb;color:white;font-weight:600">' + t_('adminSave') + '</button></div>'
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
    const t_ = getAdminLang();
    var titleEl = document.getElementById('ui-admin-consult-modal-title');
    var listEl = document.getElementById('admin-user-consultations-list');
    var modalEl = document.getElementById('admin-user-consultations-modal');
    if (!modalEl) return;
    if (titleEl) titleEl.innerHTML = t_('adminConsultTitle') + ': ' + userName;
    listEl.innerHTML = '<p class="text-sm text-gray-400 italic">' + t_('adminLoading') + '</p>';
    modalEl.classList.remove('hidden');
    try {
        var resp = await fetch('/api/admin/users/' + userId + '/consultations?t=' + Date.now());
        var result = await resp.json();
        if (resp.status === 404) {
            listEl.innerHTML = '<p class="text-sm text-red-500 italic">' + t_('adminNotFound') + '</p>';
            return;
        }
        var html = '';

        html += '<div class="mb-4"><h3 class="text-sm font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-2"><i class="fa-solid fa-stethoscope mr-1"></i> ' + t_('adminDiagnosis') + '</h3>';
        if (result.consultations && result.consultations.length > 0) {
            result.consultations.forEach(function (item) {
                html += buildConsultationCard(item, t_);
            });
        } else {
            html += '<p class="text-sm text-gray-400 italic">' + t_('adminNoData') + '</p>';
        }
        html += '</div>';

        html += '<div><h3 class="text-sm font-bold text-purple-600 dark:text-purple-400 uppercase tracking-wider mb-2"><i class="fa-solid fa-flask mr-1"></i> ' + t_('adminLab') + '</h3>';
        if (result.training_sessions && result.training_sessions.length > 0) {
            result.training_sessions.forEach(function (sess) {
                var onclickSession = isOnTraining()
                    ? 'window.closeAdminUsersModal();window.closeAdminUserConsultationsModal();viewSessionResults(\'' + sess.session_id + '\')'
                    : 'window.closeAdminUsersModal();window.closeAdminUserConsultationsModal();window.location.href=\'/training?session=' + sess.session_id + '\'';
                html += '<div onclick="' + onclickSession + '" class="bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 mb-2 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer"><div class="flex justify-between items-center"><div><p class="text-sm font-bold text-gray-800 dark:text-white">' + t_('adminSessionIdLabel') + ': ' + sess.session_id + '</p><p class="text-xs text-gray-500">' + t_('adminModelsLabel') + ': ' + sess.models.join(', ') + '</p><p class="text-xs text-gray-400">' + sess.models.length + ' ' + t_('adminModelsLabel').toLowerCase() + '</p></div><div class="flex gap-2"><span class="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-2 py-1 rounded-full font-semibold">' + t_('adminOpen') + '</span></div></div></div>';
            });
        } else {
            html += '<p class="text-sm text-gray-400 italic">' + t_('adminNoData') + '</p>';
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
        if (data.status === "success") {
            const t_ = getAdminLang();
            var hasPending = data.has_pending;
            data.jobs.forEach(function (j) {
                if (j.status === 'completed' && j.job_type === 'external_validation' && typeof currentViewingSession !== 'undefined' && currentViewingSession && j.session_id === currentViewingSession && typeof viewSessionResults === 'function') {
                    viewSessionResults(currentViewingSession);
                }
            });
            if (hasPending) {
                panel.classList.remove('hidden');
                var html = '';
                data.jobs.forEach(function (j) {
                    if (j.status === 'queued' || j.status === 'running') {
                        var icon = j.job_type === 'diagnosis' ? 'fa-stethoscope' : (j.job_type === 'external_validation' ? 'fa-hospital-user' : 'fa-flask');
                        var label = j.job_type === 'diagnosis' ? t_('queueDiagnosis') : (j.job_type === 'external_validation' ? t_('queueExtValidation') : t_('queueTraining'));
                        var statusText = j.status === 'running' ? t_('queueProcessing') : t_('queuePosition').replace('{pos}', (j.position || '?'));
                        var statusColor = j.status === 'running' ? 'text-green-500' : 'text-blue-500';
                        var tooltip = j.job_type === 'diagnosis' ? 'Modelo: ' + (j.model_name || '?') : 'Sesión: ' + (j.session_id || '?');
                        var delBtn = j.status === 'queued' ? '<button onclick="window.cancelQueueJob(' + j.id + ')" class="text-red-400 hover:text-red-600 text-xs ml-1" title="' + t_('queueCancel') + '"><i class="fa-solid fa-trash-can"></i></button>' : '';
                        html += '<div class="flex items-center gap-2 text-xs group relative" title="' + tooltip + '"><i class="fa-solid ' + icon + ' text-gray-400"></i><span class="text-gray-700 dark:text-gray-300 truncate max-w-[100px]">' + label + '</span><span class="ml-auto ' + statusColor + ' font-semibold">' + statusText + '</span>' + delBtn + '</div>';
                    }
                });
                items.innerHTML = html || '<p class="text-xs text-gray-400 italic">' + t_('queueEmpty') + '</p>';
            } else {
                panel.classList.add('hidden');
            }
        }
    } catch (e) {}
}

window.cancelQueueJob = async function (jobId) {
    const t_ = getAdminLang();
    if (!confirm(t_('queueCancelConfirm'))) return;
    try {
        await fetch('/api/queue/cancel/' + jobId, { method: 'DELETE' });
    } catch (e) {}
};

setInterval(pollQueue, 5000);
setTimeout(pollQueue, 500);

window.adminDeleteConsultation = async function (consultationId) {
    const t_ = getAdminLang();
    if (!confirm(t_('adminConfirmDelete'))) return;
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
