let selectedFile = null;

function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');
    if (html.classList.contains('dark')) {
        html.classList.remove('dark'); icon.className = 'fa-solid fa-moon text-lg'; localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark'); icon.className = 'fa-solid fa-sun text-lg'; localStorage.setItem('theme', 'dark');
    }
}

const _origChangeLang = window.changeLanguage || function(){};
window.changeLanguage = function() {
    _origChangeLang();
    const t_ = window.t || (k=>k);

    const ids = ['ui-nav-diag', 'ui-nav-lab', 'ui-history-title', 'ui-no-history', 'ui-logout', 'ui-subtitle', 'ui-model-label', 'ui-welcome', 'ui-back', 'ui-cd-rename', 'ui-cd-delete', 'ui-cd-original-label', 'ui-cd-xai-label', 'ui-cd-diagnosis-label', 'ui-cd-confidence-label', 'ui-cd-model-label', 'ui-cd-patient-label', 'ui-queue-title', 'ui-queue-empty'];
    const keys = ['navDiag', 'navLab', 'historyTitle', 'noHistory', 'logout', 'subtitle', 'modelLabel', 'welcome', 'back', 'cdRename', 'cdDelete', 'cdOrigLabel', 'cdXaiLabel', 'cdDiagLabel', 'cdConfLabel', 'cdModelLabel', 'cdPatient', 'queueTitle', 'queueEmpty'];
    ids.forEach((id, i) => { if (document.getElementById(id)) document.getElementById(id).innerText = t_(keys[i]); });
    if (!selectedFile && document.getElementById('ui-drop-text')) document.getElementById('ui-drop-text').innerText = t_('dropText');

    document.querySelectorAll('.ui-recovered-txt').forEach(el => el.innerText = t_('recovered'));
    document.querySelectorAll('.ui-diagnosis-txt').forEach(el => el.innerText = t_('diagnosis'));
    document.querySelectorAll('.ui-confidence-txt').forEach(el => el.innerText = t_('confidence'));
    document.querySelectorAll('.ui-infmodel-txt').forEach(el => el.innerText = t_('infModel'));
    document.querySelectorAll('.ui-heatmap-txt').forEach(el => el.innerText = t_('heatmap'));
    document.querySelectorAll('.ui-download-txt').forEach(el => el.innerText = t_('downloadPdf'));
    if (typeof loadHistory === 'function') loadHistory();
};

const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', function (e) {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        document.getElementById('ui-drop-text').classList.add('hidden');
        document.getElementById('file-name-display').innerText = selectedFile.name;
        document.getElementById('file-name-display').classList.remove('hidden');
        document.getElementById('send-btn').disabled = false;
        document.getElementById('drop-zone').classList.add('border-blue-500', 'bg-blue-50', 'dark:bg-blue-900/20');
    }
});

function addMessage(type, content) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    if (type === 'user') {
        msgDiv.className = 'flex items-start gap-4 justify-end';
        msgDiv.innerHTML = `<div class="bg-blue-600 dark:bg-blue-500 border border-blue-700 dark:border-blue-600 rounded-2xl rounded-tr-none p-2 shadow-sm max-w-sm">${content}</div><div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-user-md text-gray-500 dark:text-gray-400"></i></div>`;
    } else {
        msgDiv.className = 'flex items-start gap-4';
        msgDiv.innerHTML = `<div class="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center flex-shrink-0"><i class="fa-solid fa-robot text-blue-600 dark:text-blue-400"></i></div><div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl rounded-tl-none p-5 shadow-sm max-w-3xl w-full text-gray-700 dark:text-gray-200">${content}</div>`;
    }
    chatBox.appendChild(msgDiv); chatBox.scrollTop = chatBox.scrollHeight; return msgDiv;
}

async function sendImage() {
    if (!selectedFile) return;
    const modelName = document.getElementById('model-selector').value;
    const t_ = window.t || (k=>k);
    const imageUrl = URL.createObjectURL(selectedFile);

    addMessage('user', `<img src="${imageUrl}" class="rounded-lg w-48 h-auto shadow-sm cursor-pointer border border-blue-300 dark:border-blue-700" onclick="openImageModal(this.src)">`);
    const loadingMsg = addMessage('ai', `<div class="flex items-center gap-3"><i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i> <span>${t_('analyzing')}</span></div>`);

    const formData = new FormData();
    formData.append('file', selectedFile); formData.append('model_name', modelName);

    selectedFile = null; fileInput.value = "";
    document.getElementById('ui-drop-text').classList.remove('hidden');
    document.getElementById('file-name-display').classList.add('hidden');
    document.getElementById('send-btn').disabled = true;

    try {
        const response = await fetch('/predict', { method: 'POST', body: formData });
        const result = await response.json();
        if (response.ok && result.status === "queued") {
            var jobId = result.job_id;
            var pos = result.position || '?';
            const tNow = window.t || (k=>k);
            loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-clock text-yellow-500"></i> <span>' + tNow('queueEnqueued').replace('{pos}', pos).replace('{id}', jobId) + '</span></div>';

            var pollCount = 0;
            var pollInterval = setInterval(async function () {
                pollCount++;
                try {
                    var r = await fetch('/api/queue/status?t=' + Date.now());
                    var d = await r.json();
                    if (d.status === "success" && d.jobs) {
                        var job = d.jobs.find(function (j) { return j.id === jobId; });
                        if (job) {
                            if (job.status === "running") {
                                loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i> <span>' + t_('queueRunning') + '</span></div>';
                            } else if (job.status === "completed") {
                                clearInterval(pollInterval);
                                loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-check-circle text-green-500"></i> <span>' + t_('queueCompleted') + '</span></div>';
                                loadHistory();
                                pollQueue();
                            } else if (job.status === "failed") {
                                clearInterval(pollInterval);
                                loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<p class="text-red-500">' + t_('queueError').replace('{msg}', job.error_message || '') + '</p>';
                            }
                        }
                        if (pollCount > 600) { clearInterval(pollInterval); }
                    }
                } catch (e) {}
            }, 2000);
        } else if (!response.ok) {
            loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<p class="text-red-500">' + t_('queueEnqueueError') + '</p>';
        }
    } catch (error) { loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<p class="text-red-500">Error</p>'; }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history?t=' + new Date().getTime());
        const result = await response.json();
        const historyList = document.getElementById('history-list');
        if (result.status === "success" && result.data.length > 0) {
            historyList.innerHTML = '';
            const grouped = {};
            result.data.forEach(i => { if (!grouped[i.model_name]) grouped[i.model_name] = []; grouped[i.model_name].push(i); });

            for (const [model, items] of Object.entries(grouped)) {
                let html = `<div class="mb-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden"><button onclick="this.nextElementSibling.classList.toggle('hidden')" class="w-full flex justify-between p-3 bg-gray-50 dark:bg-gray-800/80"><span class="text-xs font-bold text-gray-700 dark:text-gray-300">${model} (${items.length})</span></button><div class="hidden flex-col gap-2 p-2">`;

                items.forEach(item => {
                    let lbl = item.prediction_label;
                    if (currentLang === 'en') lbl = lbl === "Neumonía" ? "Pneumonia" : "Normal";
                    const p = item.original_image_path.replace(/\\/g, '/');
                    const x = item.xai_image_path.replace(/\\/g, '/');
                    html += `<div class="bg-white dark:bg-gray-800 p-2 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer" onclick="window.openConsultationDetail(${item.id},'${p}','${x}','${item.prediction_label}',${item.confidence_score},'${model}','${(item.patient_name || '').replace(/'/g, "\\'")}','${item.timestamp}')"><div class="flex gap-3"><img src="/${p}" class="w-10 h-10 object-cover rounded"><div class="flex-1"><p class="text-[10px] text-gray-500">${item.timestamp}</p><p class="text-[11px] font-black ${item.prediction_label === "Neumonía" ? 'text-red-500' : 'text-green-500'}">${lbl}</p><p class="text-[10px] text-gray-400">${item.patient_name || ''}</p></div></div></div>`;
                });
                historyList.innerHTML += html + `</div></div>`;
            }
        }
    } catch (e) { }
}

function reviewConsultation(o, x, l, c, m, p) {
    const t_ = window.t || (k=>k);
    let lbl = l; if (currentLang === 'en') lbl = l === "Neumonía" ? "Pneumonia" : "Normal";
    addMessage('user', `<img src="/${o}" class="rounded-lg w-48 shadow-sm cursor-pointer" onclick="openImageModal(this.src)">`);
    addMessage('ai', `<div class="grid grid-cols-1 md:grid-cols-5 gap-6"><div class="md:col-span-2"><h3 class="text-xs font-bold text-gray-500 mb-2"><span class="ui-diagnosis-txt">${t_('diagnosis')}</span></h3><p class="font-black text-xl ${l === 'Neumonía' ? 'text-red-500' : 'text-green-500'}">${lbl} (${c}%)</p><p class="text-sm text-gray-400 mt-2">${m}</p></div><div class="md:col-span-3"><img src="/${x}" class="rounded-xl w-full cursor-pointer" onclick="openImageModal(this.src)"></div></div>`);
}

window._cdId = null;
window._cdPatient = '';

window.openConsultationDetail = function(id, imgPath, xaiPath, label, confidence, model, patient, timestamp) {
    window._cdId = id;
    window._cdPatient = patient;
    const t_ = window.t || (k=>k);
    const isPneu = label === "Neumonía";
    const lbl = currentLang === 'en' ? (isPneu ? "Pneumonia" : "Normal") : label;

    document.getElementById('chat-box').classList.add('hidden');
    document.getElementById('consultation-detail-panel').classList.remove('hidden');
    document.getElementById('cd-original').src = '/' + imgPath;
    document.getElementById('cd-xai').src = '/' + xaiPath;
    document.getElementById('cd-label').innerText = lbl;
    document.getElementById('cd-label').className = 'text-sm font-black ' + (isPneu ? 'text-red-500' : 'text-green-500');
    document.getElementById('cd-confidence').innerText = confidence + '%';
    document.getElementById('cd-model').innerText = model;
    document.getElementById('cd-patient').innerText = patient || '\u2014';
    document.getElementById('cd-timestamp').innerText = timestamp || '';
    document.getElementById('cd-title').innerText = t_('cdTitle');
};

window.closeConsultationDetail = function() {
    window._cdId = null;
    window._cdPatient = '';
    document.getElementById('consultation-detail-panel').classList.add('hidden');
    document.getElementById('chat-box').classList.remove('hidden');
};

function openImageModal(src) { document.getElementById('modal-image-content').src = src; document.getElementById('image-modal').classList.remove('hidden'); }
function closeImageModal() { document.getElementById('image-modal').classList.add('hidden'); }

window.addEventListener('DOMContentLoaded', () => {
    restoreTheme();
    restoreLang();
    changeLanguage();
    var params = new URLSearchParams(window.location.search);
    var cid = params.get('cid');
    if (cid) {
        fetch('/api/admin/consultations/' + cid + '?t=' + Date.now()).then(function(r){return r.json();}).then(function(result){
            if (result.status === "success" && result.consultation) {
                var c = result.consultation;
                var p = (c.original_image_path || '').replace(/\\/g, '/');
                var x = (c.xai_image_path || '').replace(/\\/g, '/');
                setTimeout(function(){ window.openConsultationDetail(c.id, p, x, c.prediction_label, c.confidence_score, c.model_name, c.patient_name, c.timestamp); }, 300);
            }
        }).catch(function(){});
    }
});
