const dict = { es: {}, en: {} }; 
        let logInterval = null;
        let currentViewingSession = ""; 
        let currentViewingModel = "";
        let currentSessionConfig = null; 
        
        const chatSessionId = "CHAT_" + Math.random().toString(36).substring(7);

        function openImageModal(src) { document.getElementById('modal-image').src = src; document.getElementById('image-modal').classList.remove('hidden'); }
        function closeImageModal() { document.getElementById('image-modal').classList.add('hidden'); document.getElementById('modal-image').src = ''; }
        window.addEventListener('keydown', function(event) { if (event.key === 'Escape') closeImageModal(); });
        function toggleTheme() {
            const html = document.documentElement;
            if (html.classList.contains('dark')) { html.classList.remove('dark'); localStorage.setItem('theme', 'light'); document.getElementById('theme-icon').className='fa-solid fa-moon text-lg'; }
            else { html.classList.add('dark'); localStorage.setItem('theme', 'dark'); document.getElementById('theme-icon').className='fa-solid fa-sun text-lg'; }
        }
        function changeLanguage() {}

        async function loadSidebarModels() {
            const list = document.getElementById('experiments-list');
            try {
                const res = await fetch('/api/train/models');
                const data = await res.json();
                
                if (data.sessions && data.sessions.length > 0) {
                    list.innerHTML = '';
                    data.sessions.forEach(session => {
                        let title = session.session_id; 
                        let subtitle = "Sesión Guardada";
                        if (title.startsWith('RUN_') && title.length === 19) {
                            const rawDate = title.replace('RUN_', '');
                            subtitle = `${rawDate.substring(6,8)}/${rawDate.substring(4,6)} ${rawDate.substring(9,11)}:${rawDate.substring(11,13)}`;
                        }

                        let sessionHTML = `
                        <div class="mb-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-sm relative group/session cursor-pointer" onclick="viewSessionResults('${session.session_id}')">
                            <div class="flex items-center w-full">
                                <div class="flex-1 text-left flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors rounded-tl-xl overflow-hidden">
                                    <div class="flex items-center gap-3 overflow-hidden">
                                        <div class="min-w-[32px] w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center text-purple-600 dark:text-purple-400"><i class="fa-solid fa-layer-group text-sm"></i></div>
                                        <div class="overflow-hidden pr-2">
                                            <span class="font-bold text-xs text-gray-800 dark:text-gray-200 block truncate" title="${title}">${title}</span>
                                            <span class="text-[10px] text-gray-500 dark:text-gray-400 font-mono block truncate">${subtitle}</span>
                                        </div>
                                    </div>
                                </div>
                                <button onclick="toggleSession(event, '${session.session_id}')" class="px-4 py-4 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors rounded-tr-xl border-l border-transparent dark:border-gray-700 focus:outline-none">
                                    <i id="session-icon-${session.session_id}" class="fa-solid fa-chevron-down text-gray-400 text-xs transition-transform duration-200 shrink-0"></i>
                                </button>
                            </div>
                            <div class="absolute right-12 top-3.5 opacity-0 group-hover/session:opacity-100 transition-opacity flex items-center gap-1 bg-white dark:bg-gray-800 shadow-sm rounded-md p-1 border border-gray-200 dark:border-gray-600 z-10" onclick="event.stopPropagation()">
                                <button onclick="renameSession(event, '${session.session_id}')" class="w-6 h-6 flex items-center justify-center rounded bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors" title="Renombrar sesión"><i class="fa-solid fa-pencil text-[10px]"></i></button>
                                <button onclick="deleteSession(event, '${session.session_id}')" class="w-6 h-6 flex items-center justify-center rounded bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors" title="Eliminar sesión"><i class="fa-solid fa-trash text-[10px]"></i></button>
                            </div>
                            <div id="session-content-${session.session_id}" class="hidden flex-col gap-1 p-2 bg-gray-50/50 dark:bg-gray-900/30 border-t border-gray-100 dark:border-gray-700" onclick="event.stopPropagation()">`;
                        
                        session.models.forEach(model => {
                            sessionHTML += `<button onclick="viewResults('${session.session_id}', '${model}')" class="w-full text-left px-4 py-2 text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors flex items-center gap-2 focus:outline-none"><i class="fa-solid fa-microchip text-xs opacity-50"></i> ${model}</button>`;
                        });
                        sessionHTML += `</div></div>`; list.innerHTML += sessionHTML;
                    });
                } else {
                    list.innerHTML = `<div class="text-center mt-10"><i class="fa-solid fa-box-open text-3xl text-gray-300 dark:text-gray-600 mb-3"></i><p class="text-sm text-gray-400 dark:text-gray-500 font-medium">No hay sesiones guardadas</p></div>`;
                }
            } catch (e) {}
        }

        function appendChatMessage(sender, text) {
            const chatHistory = document.getElementById('chat-history');
            const bubbleDiv = document.createElement('div');
            
            if (sender === 'user') {
                bubbleDiv.className = "flex flex-col gap-1 items-end ml-auto max-w-[85%] sm:max-w-[75%]";
                bubbleDiv.innerHTML = `<div class="chat-bubble-user px-4 py-3 rounded-2xl text-sm shadow-sm leading-relaxed">${text.replace(/\n/g, '<br>')}</div>`;
            } else {
                bubbleDiv.className = "flex flex-col gap-1 items-start max-w-[85%] sm:max-w-[75%]";
                bubbleDiv.innerHTML = `<div class="chat-bubble-ai px-4 py-3 rounded-2xl text-sm shadow-sm leading-relaxed">${text.replace(/\n/g, '<br>')}</div>`;
            }
            
            chatHistory.appendChild(bubbleDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        async function handleChatSubmit(event) {
            event.preventDefault();
            const inputField = document.getElementById('chat-input');
            const message = inputField.value.trim();
            if (!message) return;

            appendChatMessage('user', message);
            inputField.value = '';
            inputField.disabled = true;

            const chatHistory = document.getElementById('chat-history');
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'chat-loading';
            loadingDiv.className = "flex flex-col gap-1 items-start max-w-[80%]";
            loadingDiv.innerHTML = `<div class="chat-bubble-ai px-4 py-3 rounded-2xl text-sm shadow-sm flex items-center gap-2"><i class="fa-solid fa-circle-notch fa-spin"></i> Pensando...</div>`;
            chatHistory.appendChild(loadingDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;

            const formData = new FormData();
            formData.append('session_id', chatSessionId);
            formData.append('message', message);

            try {
                const response = await fetch('/api/chat', { method: 'POST', body: formData });
                const data = await response.json();
                
                document.getElementById('chat-loading').remove();

                if (data.response.includes('"ready": true') || data.response.includes("'ready': true")) {
                    try {
                        const jsonMatch = data.response.match(/\{[\s\S]*\}/);
                        if (jsonMatch) {
                            const config = JSON.parse(jsonMatch[0]);
                            appendChatMessage('ai', `¡Todo listo! He configurado las máquinas con esos parámetros. Iniciando el entrenamiento de: <b>${config.models}</b>.`);
                            startTrainingFromChat(config);
                        }
                    } catch (e) {
                        appendChatMessage('ai', "¡Ups! Entendí los parámetros pero hubo un fallo interno leyendo los datos. ¿Puedes repetírmelos?");
                    }
                } else {
                    appendChatMessage('ai', data.response);
                }
            } catch (error) {
                document.getElementById('chat-loading').remove();
                appendChatMessage('ai', "Error de conexión con el servidor. Revisa tu consola.");
            }
            
            inputField.disabled = false;
            inputField.focus();
        }

        async function browseFolderAndInsert() {
            try {
                const response = await fetch('/api/train/browse');
                const data = await response.json();
                if(data.path) { 
                    const inputField = document.getElementById('chat-input');
                    inputField.value = `La ruta de mi dataset es: ${data.path}`;
                    inputField.focus();
                }
            } catch (error) { alert("No se pudo abrir el explorador de Windows."); }
        }

        async function startTrainingFromChat(config) {
            document.getElementById('loading-spinner').classList.remove('hidden');
            const formData = new FormData(); 
            formData.append('dataset_path', config.dataset_path); 
            formData.append('model_names', config.models); 
            formData.append('epochs', config.epochs); 
            formData.append('batch_size', config.batch_size); 
            formData.append('learning_rate', config.learning_rate);

            try {
                const response = await fetch('/api/train/start', { method: 'POST', body: formData }); 
                const result = await response.json();
                if (response.ok) {
                    currentViewingSession = result.message.split('sesión ')[1].replace('.',''); 
                    document.getElementById('training-console').classList.remove('hidden'); 
                    document.getElementById('console-logs').innerHTML = `<p class="text-blue-400">> ${result.message}</p>`;
                    if(logInterval) clearInterval(logInterval); 
                    logInterval = setInterval(fetchLogs, 2000);
                } else { 
                    alert("❌ Error: " + result.message); 
                    document.getElementById('loading-spinner').classList.add('hidden'); 
                }
            } catch (error) { 
                document.getElementById('loading-spinner').classList.add('hidden'); 
            }
        }

        function toggleSession(event, sessionId) {
            event.stopPropagation();
            const content = document.getElementById(`session-content-${sessionId}`);
            const icon = document.getElementById(`session-icon-${sessionId}`);
            if (content.classList.contains('hidden')) { content.classList.remove('hidden'); icon.classList.replace('fa-chevron-down', 'fa-chevron-up'); } 
            else { content.classList.add('hidden'); icon.classList.replace('fa-chevron-up', 'fa-chevron-down'); }
        }

        function customPrompt(msg, def) {
            return new Promise(resolve => {
                const wrap = document.createElement('div');
                wrap.style.cssText = 'position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center';
                const box = document.createElement('div');
                box.style.cssText = 'background:white;padding:24px;border-radius:12px;min-width:320px;box-shadow:0 4px 24px rgba(0,0,0,0.2)';
                box.innerHTML = `<p style="margin:0 0 12px;font-weight:700;font-size:14px">${msg}</p><input id="cp-input" value="${def}" style="width:100%;padding:8px 12px;border:1px solid #ccc;border-radius:8px;font-size:14px;box-sizing:border-box"><div style="display:flex;gap:8px;justify-content:flex-end;margin-top:16px"><button id="cp-cancel" style="padding:8px 16px;border-radius:8px;border:1px solid #ccc;background:white;cursor:pointer">Cancelar</button><button id="cp-ok" style="padding:8px 16px;border-radius:8px;border:none;background:#2563eb;color:white;cursor:pointer">Renombrar</button></div>`;
                wrap.appendChild(box); document.body.appendChild(wrap);
                document.getElementById('cp-input').focus();
                document.getElementById('cp-input').select();
                document.getElementById('cp-ok').onclick = () => { const v = document.getElementById('cp-input').value; document.body.removeChild(wrap); resolve(v); };
                document.getElementById('cp-cancel').onclick = () => { document.body.removeChild(wrap); resolve(null); };
                document.getElementById('cp-input').onkeydown = e => { if(e.key==='Enter') document.getElementById('cp-ok').click(); if(e.key==='Escape') document.getElementById('cp-cancel').click(); };
            });
        }

        async function renameSession(event, oldId) {
            if(event) event.stopPropagation();
            const newName = await customPrompt("Nuevo nombre para esta sesión:", oldId);
            if (!newName || newName === oldId) return;
            const formData = new FormData(); formData.append('old_name', oldId); formData.append('new_name', newName);
            try {
                const res = await fetch('/api/train/session/rename', { method: 'POST', body: formData });
                const data = await res.json();
                if (res.ok) { if (currentViewingSession === oldId) { currentViewingSession = data.new_name; if(document.getElementById('session-title-name')) document.getElementById('session-title-name').innerText = data.new_name; } loadSidebarModels(); } 
                else { alert("❌ Error: " + data.message); }
            } catch(e) {}
        }

        async function deleteSession(event, sessionId) {
            if(event) event.stopPropagation();
            if(!confirm(`⚠️ ¿Eliminar DEFINITIVAMENTE la sesión '${sessionId}'?`)) return;
            try {
                const res = await fetch(`/api/train/session/${sessionId}`, { method: 'DELETE' });
                if (res.ok) { if (currentViewingSession === sessionId) { document.getElementById('session-results-panel').classList.add('hidden'); document.getElementById('results-panel').classList.add('hidden'); document.getElementById('config-panel').classList.remove('hidden'); } loadSidebarModels(); } 
                else { const data = await res.json(); alert("❌ Error: " + data.message); }
            } catch(e) {}
        }

        async function recalculateComparison(sessionId) {
            document.getElementById('session-results-panel').classList.add('hidden'); document.getElementById('config-panel').classList.remove('hidden'); document.getElementById('training-console').classList.remove('hidden'); document.getElementById('loading-spinner').classList.remove('hidden');
            const formData = new FormData(); formData.append('session_id', sessionId);
            try { await fetch('/api/train/session/compare', { method: 'POST', body: formData }); currentViewingSession = sessionId; if(logInterval) clearInterval(logInterval); logInterval = setInterval(fetchLogs, 2000); } catch(e) {}
        }

        function cloneSessionConfig() {
            if (!currentSessionConfig || Object.keys(currentSessionConfig).length === 0) { 
                alert("No hay configuración guardada para esta sesión."); 
                return; 
            }
            
            document.getElementById('session-results-panel').classList.add('hidden'); 
            document.getElementById('results-panel').classList.add('hidden'); 
            document.getElementById('config-panel').classList.remove('hidden');
            
            const modelsStr = Array.isArray(currentSessionConfig.models) 
                ? currentSessionConfig.models.join(", ") 
                : currentSessionConfig.models;
                
            const autoMessage = `Hola, quiero reutilizar los parámetros de un experimento anterior:\n- Ruta: ${currentSessionConfig.dataset_path}\n- Modelos: ${modelsStr}\n- Épocas: ${currentSessionConfig.epochs || 20}\n- Batch Size: ${currentSessionConfig.batch_size || 32}\n- Learning Rate: ${currentSessionConfig.learning_rate || 0.001}\n\n¿Me los listas y me preguntas si quiero cambiar algo antes de empezar?`;
            
            const inputField = document.getElementById('chat-input');
            inputField.value = autoMessage;
            
            const fakeEvent = { preventDefault: () => {} };
            handleChatSubmit(fakeEvent);
        }

        async function launchExternalValidation() {
            try {
                const response = await fetch('/api/train/browse');
                const data = await response.json();
                if(data.path) {
                    document.getElementById('session-results-panel').classList.add('hidden'); document.getElementById('training-console').classList.remove('hidden'); document.getElementById('loading-spinner').classList.remove('hidden');
                    const formData = new FormData(); formData.append('session_id', currentViewingSession); formData.append('dataset_path', data.path);
                    await fetch('/api/train/session/external_validation', { method: 'POST', body: formData });
                    if(logInterval) clearInterval(logInterval); logInterval = setInterval(fetchLogs, 2000);
                }
            } catch (error) { alert("Error abriendo el explorador."); }
        }

        async function viewSessionResults(sessionId) {
            currentViewingSession = sessionId;
            document.getElementById('config-panel').classList.add('hidden'); document.getElementById('results-panel').classList.add('hidden'); document.getElementById('training-console').classList.add('hidden'); document.getElementById('session-results-panel').classList.remove('hidden'); document.getElementById('session-title-name').innerText = sessionId;
            try {
                const res = await fetch(`/api/train/session/${sessionId}/ranking`);
                const data = await res.json();
                const tbody = document.getElementById('session-ranking-table'); const img = document.getElementById('session-heatmap-img'); const err = document.getElementById('session-heatmap-error'); const grid = document.getElementById('session-models-grid');
                tbody.innerHTML = ''; grid.innerHTML = '';
                if (data.config) {
                    currentSessionConfig = data.config;
                    document.getElementById('session-cfg-path').innerText = data.config.dataset_path ? data.config.dataset_path.split('\\').pop().split('/').pop() : 'No guardada'; document.getElementById('session-cfg-path').title = data.config.dataset_path || ''; document.getElementById('session-cfg-epochs').innerText = data.config.epochs || '-'; document.getElementById('session-cfg-batch').innerText = data.config.batch_size || '-'; document.getElementById('session-cfg-lr').innerText = data.config.learning_rate || '-';
                } else {
                    currentSessionConfig = null; document.getElementById('session-cfg-path').innerText = '-'; document.getElementById('session-cfg-epochs').innerText = '-'; document.getElementById('session-cfg-batch').innerText = '-'; document.getElementById('session-cfg-lr').innerText = '-';
                }
                if(data.status === "success") {
                    data.ranking.forEach((r, i) => {
                        let rankIcon = i === 0 ? '🏆' : (i === 1 ? '🥈' : (i === 2 ? '🥉' : `${i+1}º`));
                        let rowClass = i === 0 ? 'bg-yellow-50/50 dark:bg-yellow-900/10 font-bold' : 'hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors';
                        tbody.innerHTML += `<tr class="${rowClass} border-b dark:border-gray-700"><td class="px-4 py-4 text-center text-lg">${rankIcon}</td><td class="px-4 py-4 text-gray-800 dark:text-gray-200 font-semibold flex items-center gap-2"><i class="fa-solid fa-microchip opacity-50"></i> ${r.Model}</td><td class="px-4 py-4 font-mono text-blue-600 dark:text-blue-400 font-bold">${parseFloat(r.Mean).toFixed(4)}</td><td class="px-4 py-4 font-mono text-gray-500">±${parseFloat(r.Std).toFixed(4)}</td></tr>`;
                        grid.innerHTML += `<button onclick="viewResults('${sessionId}', '${r.Model}')" class="px-4 py-3 bg-gray-50 hover:bg-blue-50 dark:bg-gray-700 dark:hover:bg-gray-600 border border-gray-200 dark:border-gray-600 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-200 transition-colors flex items-center gap-2 shadow-sm focus:outline-none"><i class="fa-solid fa-microchip text-blue-500"></i> ${r.Model}</button>`;
                    });
                    if(data.ranking.length >= 2) { img.src = `${data.heatmap}?t=${new Date().getTime()}`; img.classList.remove('hidden'); err.classList.add('hidden'); } else { img.classList.add('hidden'); err.classList.remove('hidden'); }
                } else { tbody.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-gray-500">Resultados no encontrados.</td></tr>`; img.classList.add('hidden'); err.classList.add('hidden'); }
                try {
                    const resExt = await fetch(`/api/train/session/${sessionId}/external_results`);
                    const dataExt = await resExt.json();
                    const extContainer = document.getElementById('external-validation-container');
                    const extTbody = document.getElementById('external-ranking-table');
                    const extImg = document.getElementById('external-roc-img');
                    const extDelongImg = document.getElementById('external-delong-img');
                    const extDelongErr = document.getElementById('external-delong-error');
                    if(dataExt.status === "success") {
                        extContainer.classList.remove('hidden');
                        extTbody.innerHTML = '';
                        dataExt.metrics.forEach(r => {
                            extTbody.innerHTML += `<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="px-4 py-3 font-bold">${r.Model}</td><td class="px-4 py-3 font-mono">${parseFloat(r.Accuracy).toFixed(4)}</td><td class="px-4 py-3 font-mono">${parseFloat(r["F1-score"]).toFixed(4)}</td><td class="px-4 py-3 font-mono text-blue-600 dark:text-blue-400 font-bold">${parseFloat(r.AUC).toFixed(4)}</td></tr>`;
                        });
                        extImg.src = `${dataExt.roc}?t=${new Date().getTime()}`;
                        if (dataExt.metrics.length >= 2 && dataExt.delong) { extDelongImg.src = `${dataExt.delong}?t=${new Date().getTime()}`; extDelongImg.classList.remove('hidden'); extDelongErr.classList.add('hidden'); } else { extDelongImg.classList.add('hidden'); extDelongErr.classList.remove('hidden'); }
                    } else { extContainer.classList.add('hidden'); }
                } catch(e) { document.getElementById('external-validation-container').classList.add('hidden'); }
            } catch(e) {}
        }

        async function viewResults(sessionId, modelName) {
            currentViewingSession = sessionId; currentViewingModel = modelName;
            document.getElementById('config-panel').classList.add('hidden'); document.getElementById('session-results-panel').classList.add('hidden'); document.getElementById('training-console').classList.add('hidden'); document.getElementById('results-panel').classList.remove('hidden'); document.getElementById('res-model-name').innerText = modelName;
            try {
                const res = await fetch(`/api/train/results/${sessionId}/${modelName}`);
                const data = await res.json();
                if(data.status === "success") {
                    const tbody = document.getElementById('res-table-body'); tbody.innerHTML = '';
                    data.data.forEach(row => {
                        const isMean = isNaN(row.fold) || row.fold === 'mean' || row.fold === 'std' || row.fold === 'Media' || row.fold === 'Std';
                        const bgClass = isMean ? 'bg-blue-50/50 dark:bg-blue-900/10 font-black text-gray-900 dark:text-white border-t-2 border-blue-200 dark:border-blue-800/50' : 'bg-white dark:bg-gray-800';
                        let foldName = row.fold || "Eval"; 
                        tbody.innerHTML += `<tr class="transition-colors ${bgClass}"><td class="px-6 py-4">${foldName}</td><td class="px-6 py-4">${parseFloat(row.accuracy||0).toFixed(4)}</td><td class="px-6 py-4">${parseFloat(row.precision||0).toFixed(4)}</td><td class="px-6 py-4">${parseFloat(row.recall||0).toFixed(4)}</td><td class="px-6 py-4">${parseFloat(row.f1||0).toFixed(4)}</td><td class="px-6 py-4 ${isMean ? 'text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'}">${parseFloat(row.auc||0).toFixed(4)}</td></tr>`;
                    });
                    const imgContainer = document.getElementById('res-images'); imgContainer.innerHTML = '';
                    const mathPanel = document.getElementById('res-math-panel');
                    if(data.images && data.images.length > 0) {
                        data.images.forEach(img => { 
                            const timestampedSrc = `${img}?t=${new Date().getTime()}`;
                            imgContainer.innerHTML += `<div class="bg-white dark:bg-gray-800 p-2 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden"><img src="${timestampedSrc}" class="w-full rounded-xl object-contain bg-black cursor-zoom-in hover:scale-[1.02] transition-transform duration-300" onclick="openImageModal(this.src)"></div>`; 
                        });
                        mathPanel.classList.remove('hidden');
                        document.getElementById('ui-brier').innerText = data.calib.brier || "-"; document.getElementById('ui-ece').innerText = data.calib.ece || "-";
                        const xaiBody = document.getElementById('res-xai-table'); xaiBody.innerHTML = '';
                        if(data.xai_metrics && data.xai_metrics.length > 0){
                            data.xai_metrics.forEach(x => {
                                const del = String(x.deletion_auc).split('±')[0]; const ins = String(x.insertion_auc).split('±')[0]; const spa = String(x.sparsity).split('±')[0]; const ent = String(x.entropy).split('±')[0]; const sta = String(x.stability).split('±')[0];
                                xaiBody.innerHTML += `<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"><td class="px-4 py-3 font-bold text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-800/80">${x.Method}</td><td class="px-4 py-3 font-mono">${del}</td><td class="px-4 py-3 font-mono">${ins}</td><td class="px-4 py-3 font-mono">${spa}</td><td class="px-4 py-3 font-mono">${ent}</td><td class="px-4 py-3 font-mono text-purple-600 dark:text-purple-400 font-bold">${sta}</td></tr>`;
                            });
                        }
                    } else { mathPanel.classList.add('hidden'); imgContainer.innerHTML = `<div class="col-span-1 md:col-span-2 p-10 flex flex-col items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-2xl text-gray-500"><i class="fa-solid fa-wand-magic-sparkles text-4xl mb-4 text-purple-400 opacity-50"></i><p>Aún no hay mapas XAI. Dale a 'Generar XAI y Métricas'.</p></div>`; }
                }
            } catch(e) {}
        }

        // ==========================================
        // CORRECCIÓN MAGISTRAL: GENERACIÓN SÍNCRONA
        // ==========================================
        async function generateXAI() {
            // 1. Ocultar paneles y mostrar carga
            document.getElementById('results-panel').classList.add('hidden'); 
            document.getElementById('config-panel').classList.remove('hidden'); 
            document.getElementById('training-console').classList.remove('hidden'); 
            document.getElementById('loading-spinner').classList.remove('hidden');
            
            const formData = new FormData(); 
            formData.append('session_id', currentViewingSession); 
            formData.append('model_name', currentViewingModel);
            
            // 2. Iniciar el lector de logs para que veas qué está haciendo por detrás
            if(logInterval) clearInterval(logInterval); 
            logInterval = setInterval(fetchLogs, 2000);
            
            try {
                // 3. Esperar a que el servidor termine de calcularlo TODO (tarda unos 30 segs)
                const res = await fetch('/api/train/run_eval', { method: 'POST', body: formData });
                const result = await res.json();
                
                // 4. Parar la ruleta y los logs
                clearInterval(logInterval); 
                document.getElementById('loading-spinner').classList.add('hidden');
                
                if (res.ok && result.status === "success") {
                    // 5. ¡VOLVER A LA PANTALLA CON LOS RESULTADOS FRESCOS!
                    viewResults(currentViewingSession, currentViewingModel);
                } else {
                    alert("❌ " + result.message);
                }
            } catch(e) {
                clearInterval(logInterval); 
                document.getElementById('loading-spinner').classList.add('hidden');
            }
        }

        async function fetchLogs() {
            try {
                const response = await fetch('/api/train/logs'); const data = await response.json(); 
                const consoleDiv = document.getElementById('console-logs');
                consoleDiv.innerHTML = data.logs; consoleDiv.scrollTop = consoleDiv.scrollHeight;
                
                // Leemos los strings de cierre de los otros procesos (Entrenamiento global, etc)
                if (data.logs.includes("[SESIÓN COMPLETADA Y COMPARADA]") || data.logs.includes("[COMPARACIÓN COMPLETADA]") || data.logs.includes("[VALIDACIÓN EXTERNA COMPLETADA]") || data.logs.includes("PROCESO XAI COMPLETADO") || data.logs.includes("ERROR CRÍTICO") || data.logs.includes("[PROCESO XAI MANUAL COMPLETADO]")) {
                    clearInterval(logInterval); 
                    document.getElementById('loading-spinner').classList.add('hidden'); 
                    loadSidebarModels(); 
                    
                    if(data.logs.includes("[SESIÓN COMPLETADA Y COMPARADA]") || data.logs.includes("[COMPARACIÓN COMPLETADA]") || data.logs.includes("[VALIDACIÓN EXTERNA COMPLETADA]")) { 
                        viewSessionResults(currentViewingSession); 
                    }
                    
                    // Doble seguro de redirección por si acaso
                    if(data.logs.includes("[PROCESO XAI MANUAL COMPLETADO]") || data.logs.includes("PROCESO XAI COMPLETADO")) { 
                        viewResults(currentViewingSession, currentViewingModel); 
                    }
                }
            } catch(e) {}
        }

        async function downloadPDFReport() {
            if (!currentViewingSession) return;
            const btn = event.currentTarget;
            const originalHTML = btn.innerHTML;
            btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Generando...`;
            btn.disabled = true;
            try { window.location.href = `/api/train/session/${currentViewingSession}/report`; } catch (e) { alert("Error al generar el PDF"); } 
            finally { setTimeout(() => { btn.innerHTML = originalHTML; btn.disabled = false; }, 3000); }
        }

        window.addEventListener('DOMContentLoaded', () => {
            const sT = localStorage.getItem('theme'); if (sT === 'dark' || (!sT && window.matchMedia('(prefers-color-scheme: dark)').matches)) { document.documentElement.classList.add('dark'); document.getElementById('theme-icon').className='fa-solid fa-sun text-lg'; }
            changeLanguage(); loadSidebarModels();
        });