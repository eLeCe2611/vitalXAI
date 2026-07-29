const dict = {
            es: { navDiag: "Diagn\u00f3stico R\u00e1pido", navLab: "Laboratorio MLOps", historyTitle: "Historial", noHistory: "No hay consultas recientes.", logout: "Cerrar Sesi\u00f3n", subtitle: "Asistente de Detecci\u00f3n de Neumon\u00eda", modelLabel: "Modelo de IA:", welcome: "Hola, doctor. Seleccione un modelo y suba una radiograf\u00eda.", dropText: "Arrastre radiograf\u00eda o haga clic", analyzing: "Analizando...", diagnosis: "Diagn\u00f3stico", confidence: "Confianza", heatmap: "Mapa de Calor XAI", downloadPdf: "Descargar PDF", recovered: "Recuperado del Historial", infModel: "Modelo de Inferencia", back: "Volver", cdRename: "Renombrar", cdDelete: "Eliminar", cdTitle: "Detalle de Consulta", cdPatient: "Paciente", cdOrigLabel: "Radiograf\u00eda Original", cdXaiLabel: "Mapas de Calor XAI", cdDiagLabel: "Diagn\u00f3stico", cdConfLabel: "Confianza", cdModelLabel: "Modelo" },
            en: { navDiag: "Quick Diagnosis", navLab: "MLOps Laboratory", historyTitle: "History", noHistory: "No recent consultations.", logout: "Logout", subtitle: "Pneumonia Detection Assistant", modelLabel: "AI Model:", welcome: "Hello, doctor. Select an AI model and upload an X-ray.", dropText: "Drag an X-ray or click", analyzing: "Analyzing...", diagnosis: "Diagnosis", confidence: "Confidence", heatmap: "XAI Heatmap", downloadPdf: "Download PDF", recovered: "Recovered from History", infModel: "Inference Model", back: "Back", cdRename: "Rename", cdDelete: "Delete", cdTitle: "Consultation Detail", cdPatient: "Patient", cdOrigLabel: "Original X-ray", cdXaiLabel: "XAI Heatmaps", cdDiagLabel: "Diagnosis", cdConfLabel: "Confidence", cdModelLabel: "Model" },
            zh: { navDiag: "\u5feb\u901f\u8bca\u65ad", navLab: "MLOps \u5b9e\u9a8c\u5ba4", historyTitle: "\u5386\u53f2", noHistory: "\u65e0", logout: "\u767b\u51fa", subtitle: "\u80ba\u708e\u68c0\u6d4b\u52a9\u624b", modelLabel: "AI \u6a21\u578b:", welcome: "\u533b\u751f\u60a8\u597d\u3002\u8bf7\u9009\u62e9\u6a21\u578b\u5e76\u4e0a\u4f20X\u5149\u7247\u3002", dropText: "\u62d6\u62fd\u6216\u70b9\u51fb", analyzing: "\u5206\u6790\u4e2d...", diagnosis: "\u8bca\u65ad", confidence: "\u7f6e\u4fe1\u5ea6", heatmap: "XAI \u70ed\u529b\u56fe", downloadPdf: "\u4e0b\u8f7d PDF", recovered: "\u5df2\u6062\u590d", infModel: "\u6a21\u578b", back: "\u8fd4\u56de", cdRename: "\u91cd\u547d\u540d", cdDelete: "\u5220\u9664", cdTitle: "\u54a8\u8be2\u8be6\u60c5", cdPatient: "\u60a3\u8005", cdOrigLabel: "\u539f\u59cbX\u5149\u7247", cdXaiLabel: "XAI \u70ed\u529b\u56fe", cdDiagLabel: "\u8bca\u65ad", cdConfLabel: "\u7f6e\u4fe1\u5ea6", cdModelLabel: "\u6a21\u578b" },
            hi: { navDiag: "\u0924\u094d\u0935\u0930\u093f\u0924 \u0928\u093f\u0926\u093e\u0928", navLab: "\u090f\u092e\u090f\u0932\u0913\u092a\u0940\u090f\u0938 \u0932\u0948\u092c", historyTitle: "\u0907\u0924\u093f\u0939\u093e\u0938", noHistory: "\u0915\u094b\u0908 \u0928\u0939\u0940\u0902", logout: "\u0932\u0949\u0917 \u0906\u0909\u091f", subtitle: "\u0928\u093f\u092e\u094b\u0928\u093f\u092f\u093e \u091c\u093e\u0901\u091a", modelLabel: "\u090f\u0906\u0908 \u092e\u0949\u0921\u0932:", welcome: "\u092e\u0949\u0921\u0932 \u091a\u0941\u0928\u0947\u0902 \u0914\u0930 \u090f\u0915\u094d\u0938-\u0930\u0947 \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u0947\u0902\u0964", dropText: "\u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u0947\u0902", analyzing: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923...", diagnosis: "\u0928\u093f\u0926\u093e\u0928", confidence: "\u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938", heatmap: "\u0939\u0940\u091f\u092e\u0948\u092a", downloadPdf: "\u092a\u0940\u0921\u0940\u090f\u092b \u0921\u093e\u0909\u0928\u0932\u094b\u0921", recovered: "\u0907\u0924\u093f\u0939\u093e\u0938 \u0938\u0947", infModel: "\u092e\u0949\u0921\u0932", back: "\u0935\u093e\u092a\u0938", cdRename: "\u0928\u092e \u092c\u0926\u0932\u0947\u0902", cdDelete: "\u0939\u091f\u093e\u090f\u0902", cdTitle: "\u092a\u0930\u093e\u092e\u0930\u094d\u0936 \u0935\u093f\u0935\u0930\u0923", cdPatient: "\u0930\u094b\u0917\u0940", cdOrigLabel: "\u092e\u0942\u0932 \u090f\u0915\u094d\u0938-\u0930\u0947", cdXaiLabel: "XAI \u0939\u0940\u091f\u092e\u0948\u092a", cdDiagLabel: "\u0928\u093f\u0926\u093e\u0928", cdConfLabel: "\u0906\u0924\u094d\u092e\u0935\u093f\u0936\u094d\u0935\u093e\u0938", cdModelLabel: "\u092e\u0949\u0921\u0932" }
        };

        let currentLang = 'es';
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

        function changeLanguage() {
            currentLang = document.getElementById('lang-selector').value;
            localStorage.setItem('appLang', currentLang);
            const t = dict[currentLang];

            const ids = ['ui-nav-diag', 'ui-nav-lab', 'ui-history-title', 'ui-no-history', 'ui-logout', 'ui-subtitle', 'ui-model-label', 'ui-welcome', 'ui-back', 'ui-cd-rename', 'ui-cd-delete', 'ui-cd-original-label', 'ui-cd-xai-label', 'ui-cd-diagnosis-label', 'ui-cd-confidence-label', 'ui-cd-model-label', 'ui-cd-patient-label'];
            const keys = ['navDiag', 'navLab', 'historyTitle', 'noHistory', 'logout', 'subtitle', 'modelLabel', 'welcome', 'back', 'cdRename', 'cdDelete', 'cdOrigLabel', 'cdXaiLabel', 'cdDiagLabel', 'cdConfLabel', 'cdModelLabel', 'cdPatient'];
            ids.forEach((id, i) => { if (document.getElementById(id)) document.getElementById(id).innerText = t[keys[i]]; });
            if (!selectedFile && document.getElementById('ui-drop-text')) document.getElementById('ui-drop-text').innerText = t.dropText;

            document.querySelectorAll('.ui-recovered-txt').forEach(el => el.innerText = t.recovered);
            document.querySelectorAll('.ui-diagnosis-txt').forEach(el => el.innerText = t.diagnosis);
            document.querySelectorAll('.ui-confidence-txt').forEach(el => el.innerText = t.confidence);
            document.querySelectorAll('.ui-infmodel-txt').forEach(el => el.innerText = t.infModel);
            document.querySelectorAll('.ui-heatmap-txt').forEach(el => el.innerText = t.heatmap);
            document.querySelectorAll('.ui-download-txt').forEach(el => el.innerText = t.downloadPdf);

            loadHistory();
        }

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
            const t = dict[currentLang];
            const imageUrl = URL.createObjectURL(selectedFile);

            addMessage('user', `<img src="${imageUrl}" class="rounded-lg w-48 h-auto shadow-sm cursor-pointer border border-blue-300 dark:border-blue-700" onclick="openImageModal(this.src)">`);
            const loadingMsg = addMessage('ai', `<div class="flex items-center gap-3"><i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i> <span>${t.analyzing}</span></div>`);

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
                    loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-clock text-yellow-500"></i> <span>Diagn\u00f3stico encolado en posici\u00f3n ' + pos + ' (trabajo #' + jobId + ')</span></div>';

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
                                        loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-circle-notch fa-spin text-blue-600"></i> <span>Procesando diagnóstico...</span></div>';
                                    } else if (job.status === "completed") {
                                        clearInterval(pollInterval);
                                        loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<div class="flex items-center gap-3"><i class="fa-solid fa-check-circle text-green-500"></i> <span>Diagnóstico completado</span></div>';
                                        loadHistory();
                                        pollQueue();
                                    } else if (job.status === "failed") {
                                        clearInterval(pollInterval);
                                        loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<p class="text-red-500">Error: ' + (job.error_message || 'Fall\u00f3') + '</p>';
                                    }
                                }
                                if (pollCount > 600) { clearInterval(pollInterval); }
                            }
                        } catch (e) {}
                    }, 2000);
                } else if (!response.ok) {
                    loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = '<p class="text-red-500">Error al encolar</p>';
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
                            if (currentLang === 'en') lbl = lbl === "Neumon\u00eda" ? "Pneumonia" : "Normal";
                            const p = item.original_image_path.replace(/\\/g, '/');
                            const x = item.xai_image_path.replace(/\\/g, '/');
                            html += `<div class="bg-white dark:bg-gray-800 p-2 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer" onclick="window.openConsultationDetail(${item.id},'${p}','${x}','${item.prediction_label}',${item.confidence_score},'${model}','${(item.patient_name || '').replace(/'/g, "\\'")}','${item.timestamp}')"><div class="flex gap-3"><img src="/${p}" class="w-10 h-10 object-cover rounded"><div class="flex-1"><p class="text-[10px] text-gray-500">${item.timestamp}</p><p class="text-[11px] font-black ${item.prediction_label === "Neumon\u00eda" ? 'text-red-500' : 'text-green-500'}">${lbl}</p></div></div></div>`;
                        });
                        historyList.innerHTML += html + `</div></div>`;
                    }
                }
            } catch (e) { }
        }

        function reviewConsultation(o, x, l, c, m, p) {
            const t = dict[currentLang];
            let lbl = l; if (currentLang === 'en') lbl = l === "Neumon\u00eda" ? "Pneumonia" : "Normal";
            addMessage('user', `<img src="/${o}" class="rounded-lg w-48 shadow-sm cursor-pointer" onclick="openImageModal(this.src)">`);
            addMessage('ai', `<div class="grid grid-cols-1 md:grid-cols-5 gap-6"><div class="md:col-span-2"><h3 class="text-xs font-bold text-gray-500 mb-2"><span class="ui-diagnosis-txt">${t.diagnosis}</span></h3><p class="font-black text-xl ${l === 'Neumon\u00eda' ? 'text-red-500' : 'text-green-500'}">${lbl} (${c}%)</p><p class="text-sm text-gray-400 mt-2">${m}</p></div><div class="md:col-span-3"><img src="/${x}" class="rounded-xl w-full cursor-pointer" onclick="openImageModal(this.src)"></div></div>`);
        }

        window._cdId = null;
        window._cdPatient = '';

        window.openConsultationDetail = function(id, imgPath, xaiPath, label, confidence, model, patient, timestamp) {
            window._cdId = id;
            window._cdPatient = patient;
            const t = dict[currentLang];
            const isPneu = label === "Neumon\u00eda";
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
            document.getElementById('cd-title').innerText = t.cdTitle;
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
            const sT = localStorage.getItem('theme'); if (sT === 'dark' || (!sT && window.matchMedia('(prefers-color-scheme: dark)').matches)) { document.documentElement.classList.add('dark'); document.getElementById('theme-icon').className = 'fa-solid fa-sun text-lg'; }
            const sL = localStorage.getItem('appLang'); if (sL) { document.getElementById('lang-selector').value = sL; currentLang = sL; }
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
