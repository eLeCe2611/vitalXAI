const dict = {
            es: { navDiag: "Diagnóstico Rápido", navLab: "Laboratorio MLOps", historyTitle: "Historial", noHistory: "No hay consultas recientes.", logout: "Cerrar Sesión", subtitle: "Asistente de Detección de Neumonía", modelLabel: "Modelo de IA:", welcome: "Hola, doctor. Seleccione un modelo y suba una radiografía.", dropText: "Arrastre radiografía o haga clic", analyzing: "Analizando...", diagnosis: "Diagnóstico", confidence: "Confianza", heatmap: "Mapa de Calor XAI", downloadPdf: "Descargar PDF", recovered: "Recuperado del Historial", infModel: "Modelo de Inferencia" },
            en: { navDiag: "Quick Diagnosis", navLab: "MLOps Laboratory", historyTitle: "History", noHistory: "No recent consultations.", logout: "Logout", subtitle: "Pneumonia Detection Assistant", modelLabel: "AI Model:", welcome: "Hello, doctor. Select an AI model and upload an X-ray.", dropText: "Drag an X-ray or click", analyzing: "Analyzing...", diagnosis: "Diagnosis", confidence: "Confidence", heatmap: "XAI Heatmap", downloadPdf: "Download PDF", recovered: "Recovered from History", infModel: "Inference Model" },
            zh: { navDiag: "快速诊断", navLab: "MLOps 实验室", historyTitle: "历史", noHistory: "无", logout: "登出", subtitle: "肺炎检测助手", modelLabel: "AI 模型:", welcome: "医生您好。请选择模型并上传X光片。", dropText: "拖拽或点击", analyzing: "分析中...", diagnosis: "诊断", confidence: "置信度", heatmap: "XAI 热力图", downloadPdf: "下载 PDF", recovered: "已恢复", infModel: "模型" },
            hi: { navDiag: "त्वरित निदान", navLab: "एमएलओप्स लैब", historyTitle: "इतिहास", noHistory: "कोई नहीं", logout: "लॉग आउट", subtitle: "निमोनिया जांच", modelLabel: "एआई मॉडल:", welcome: "मॉडल चुनें और एक्स-रे अपलोड करें।", dropText: "क्लिक करें", analyzing: "विश्लेषण...", diagnosis: "निदान", confidence: "आत्मविश्वास", heatmap: "हीटमैप", downloadPdf: "पीडीएफ डाउनलोड", recovered: "इतिहास से", infModel: "मॉडल" }
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

            const ids = ['ui-nav-diag', 'ui-nav-lab', 'ui-history-title', 'ui-no-history', 'ui-logout', 'ui-subtitle', 'ui-model-label', 'ui-welcome'];
            const keys = ['navDiag', 'navLab', 'historyTitle', 'noHistory', 'logout', 'subtitle', 'modelLabel', 'welcome'];
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
                if (response.ok) {
                    const isPneu = result.label === "Neumonía";
                    const col = isPneu ? "text-red-600 bg-red-50 border-red-200 dark:text-red-400 dark:bg-red-900/20" : "text-green-600 bg-green-50 border-green-200 dark:text-green-400 dark:bg-green-900/20";

                    let labelStr = result.label;
                    if (currentLang === 'en') labelStr = isPneu ? "Pneumonia" : "Normal";

                    loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = `
                        <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
                            <div class="md:col-span-2">
                                <h3 class="text-xs font-bold text-gray-500 mb-2"><span class="ui-diagnosis-txt">${t.diagnosis}</span></h3>
                                <div class="flex items-center gap-4 p-4 rounded-xl border ${col}"><i class="fa-solid ${isPneu ? 'fa-virus-covid' : 'fa-shield-heart'} text-3xl"></i><div><p class="font-black text-xl">${labelStr}</p><p class="text-sm"><span class="ui-confidence-txt">${t.confidence}</span>: ${result.confidence}%</p></div></div>
                            </div>
                            <div class="md:col-span-3">
                                <h3 class="text-xs font-bold text-gray-500 mb-2"><span class="ui-heatmap-txt">${t.heatmap}</span></h3>
                                <img src="${result.xai_image}" class="rounded-xl w-full cursor-pointer" onclick="openImageModal(this.src)">
                            </div>
                        </div>
                    `;
                    loadHistory();
                }
            } catch (error) { loadingMsg.querySelector('.bg-white, .dark\\:bg-gray-800').innerHTML = `<p class="text-red-500">Error</p>`; }
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
                            html += `<div class="bg-white dark:bg-gray-800 p-2 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer" onclick="reviewConsultation('${p}','${x}','${item.prediction_label}',${item.confidence_score},'${model}','')"><div class="flex gap-3"><img src="/${p}" class="w-10 h-10 object-cover rounded"><div class="flex-1"><p class="text-[10px] text-gray-500">${item.timestamp}</p><p class="text-[11px] font-black ${item.prediction_label === "Neumonía" ? 'text-red-500' : 'text-green-500'}">${lbl}</p></div></div></div>`;
                        });
                        historyList.innerHTML += html + `</div></div>`;
                    }
                }
            } catch (e) { }
        }

        function reviewConsultation(o, x, l, c, m, p) {
            const t = dict[currentLang];
            let lbl = l; if (currentLang === 'en') lbl = l === "Neumonía" ? "Pneumonia" : "Normal";
            addMessage('user', `<img src="/${o}" class="rounded-lg w-48 shadow-sm cursor-pointer" onclick="openImageModal(this.src)">`);
            addMessage('ai', `<div class="grid grid-cols-1 md:grid-cols-5 gap-6"><div class="md:col-span-2"><h3 class="text-xs font-bold text-gray-500 mb-2"><span class="ui-diagnosis-txt">${t.diagnosis}</span></h3><p class="font-black text-xl ${l === 'Neumonía' ? 'text-red-500' : 'text-green-500'}">${lbl} (${c}%)</p><p class="text-sm text-gray-400 mt-2">${m}</p></div><div class="md:col-span-3"><img src="/${x}" class="rounded-xl w-full cursor-pointer" onclick="openImageModal(this.src)"></div></div>`);
        }

        function openImageModal(src) { document.getElementById('modal-image-content').src = src; document.getElementById('image-modal').classList.remove('hidden'); }
        function closeImageModal() { document.getElementById('image-modal').classList.add('hidden'); }

        window.addEventListener('DOMContentLoaded', () => {
            const sT = localStorage.getItem('theme'); if (sT === 'dark' || (!sT && window.matchMedia('(prefers-color-scheme: dark)').matches)) { document.documentElement.classList.add('dark'); document.getElementById('theme-icon').className = 'fa-solid fa-sun text-lg'; }
            const sL = localStorage.getItem('appLang'); if (sL) { document.getElementById('lang-selector').value = sL; currentLang = sL; }
            changeLanguage();
        });