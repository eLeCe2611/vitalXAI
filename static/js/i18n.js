const dict = {
    es: {
        // Dashboard
        cnnClassics: "CNN Clásicas",
        navDiag: "Diagnóstico Rápido", navLab: "Laboratorio MLOps", historyTitle: "Historial",
        noHistory: "No hay consultas recientes.", logout: "Cerrar Sesión",
        subtitle: "Asistente de Detección de Neumonía", modelLabel: "Modelo de IA:",
        welcome: "Hola, doctor. Seleccione un modelo y suba una radiografía.",
        dropText: "Arrastre radiografía o haga clic", analyzing: "Analizando...",
        diagnosis: "Diagnóstico", confidence: "Confianza", heatmap: "Mapa de Calor XAI",
        downloadPdf: "Descargar PDF", recovered: "Recuperado del Historial",
        infModel: "Modelo de Inferencia", back: "Volver",
        // Detail panel
        cdRename: "Renombrar", cdDelete: "Eliminar", cdTitle: "Detalle de Consulta",
        cdPatient: "Paciente", cdOrigLabel: "Radiografía Original",
        cdXaiLabel: "Mapas de Calor XAI", cdDiagLabel: "Diagnóstico",
        cdConfLabel: "Confianza", cdModelLabel: "Modelo",
        // Admin
        adminBtn: "Panel de Administración", adminModalTitle: "Usuarios",
        adminConsultTitle: "Historial", adminNoData: "Sin datos",
        adminLoading: "Cargando...", adminPatient: "Paciente",
        adminDiagnosis: "Diagnósticos Rápidos", adminLab: "Entrenamientos",
        adminDeleteBtn: "Eliminar", adminRenameBtn: "Renombrar",
        adminStatus: "Estado", adminProgress: "Progreso", adminModel: "Modelo",
        adminDate: "Fecha", adminSave: "Guardar", adminCancel: "Cancelar",
        adminConfirmDelete: "¿Eliminar esta consulta?", adminDeleted: "Eliminado",
        adminRenamed: "Renombrado", adminRenamePrompt: "Nuevo nombre del paciente:",
        adminLabsTitle: "Sesiones de Laboratorio", adminSessionId: "Sesión",
        adminDeleteLabConfirm: "¿Eliminar esta sesión de laboratorio?",
        adminLabDeleted: "Sesión eliminada", adminOpen: "Abrir",
        // Login / Register
        loginTitle: "Iniciar Sesión", loginUser: "Usuario", loginPass: "Contraseña",
        loginBtn: "Entrar al Sistema", loginFooterTxt: "¿No tienes cuenta?",
        loginFooterLink: "Regístrate aquí", loginErr: "Credenciales inválidas",
        registerTitle: "Registro", registerFname: "Nombre", registerLname: "Apellidos",
        registerRole: "Rol", registerBtn: "Crear Cuenta",
        registerFooterTxt: "¿Ya tienes cuenta?", registerFooterLink: "Inicia sesión",
        registerOpt1: "Facultativo", registerOpt2: "Admin", registerOpt3: "Investigador",
        registerOpt4: "Estudiante", registerProcessing: "Procesando...",
        registerErrExists: "El usuario ya existe", registerErrServer: "Error del servidor",
        registerSuccess: "Registro exitoso",
        // Training page
        trainConfigAssistant: "Asistente de Configuración",
        trainChatPlaceholder: "Escribe aquí tu respuesta, pide la ruta, o pregúntame lo que quieras...",
        trainFolder: "Explorar Carpeta",
        trainSession: "Sesión", trainRankingTitle: "Ranking Global y Análisis Estadístico",
        trainBackToAssistant: "Volver al Asistente",
        trainRename: "Renombrar", trainReuseConfig: "Reutilizar Configuración",
        trainExternalValidation: "Validación Externa",
        trainGeneratePdf: "Generar Reporte PDF",
        trainRecalculateWilcoxon: "Recalcular Wilcoxon",
        trainPos: "Posición", trainModel: "Modelo", trainMeanAuc: "Media AUC",
        trainStdDev: "Std Dev", trainNoSessions: "No hay sesiones guardadas",
        trainThinking: "Pensando...", trainConnectionError: "Error de conexión con el servidor.",
        trainReady: "¡Todo listo! He configurado las máquinas con esos parámetros. Iniciando el entrenamiento de:",
        trainParseError: "¡Ups! Entendí los parámetros pero hubo un fallo interno leyendo los datos. ¿Puedes repetírmelos?",
        trainFolderError: "No se pudo abrir el explorador de Windows.",
        trainCancel: "Cancelar", trainConfirm: "Renombrar",
        trainRenamePrompt: "Nuevo nombre para esta sesión:",
        trainDeleteConfirm: "¿Eliminar DEFINITIVAMENTE la sesión '{session}'?",
        trainNoConfig: "No hay configuración guardada para esta sesión.",
        trainNoResults: "Resultados no encontrados.",
        trainNoXai: "Aún no hay mapas XAI. Dale a 'Generar XAI y Métricas'.",
        trainGenerating: "Generando...",
        trainLogWaiting: "Esperando...",
        // Queue
        queueTitle: "Cola de trabajos",         queueEmpty: "Sin trabajos pendientes",
        queueDiagnosis: "Diagnóstico", queueTraining: "Entrenamiento", queueExtValidation: "Validación Externa",
        queueProcessing: "Procesando...", queuePosition: "Posición #{pos}",
        queueCancel: "Cancelar", queueCancelConfirm: "¿Cancelar este trabajo?",
        queueEnqueued: "Diagnóstico encolado en posición {pos} (trabajo #{id})",
        queueEnqueuedExt: "Validación Externa encolada como trabajo #{id}",
        queueRunning: "Procesando diagnóstico...",
        queueCompleted: "Diagnóstico completado",
        queueError: "Error: {msg}",
        queueEnqueueError: "Error al encolar",
        // Charts / XAI
        xaiChartOriginal: "Radiografía Original",
        xaiChartSaliency: "Saliency Map",
        xaiChartSmoothGrad: "SmoothGrad",
        // Session detail
        sessionDetail: "Detalle de Consulta",
        // Admin users
        adminDiagCount: "diag.", adminLabCount: "lab.",
        adminNotFound: "Usuario no encontrado",
        adminSessionIdLabel: "Sesión", adminModelsLabel: "Modelos",
        adminClose: "Cerrar",
        // K-Fold results
        kFoldTitle: "Resultados K-Fold",
        kFoldXaiMetrics: "Métricas XAI",
        kFoldCalibration: "Calibración",
        kFoldBrier: "Brier Score", kFoldEce: "ECE",
        kFoldAccuracy: "Accuracy", kFoldPrecision: "Precision",
        kFoldRecall: "Recall", kFoldF1: "F1-Score", kFoldAUC: "AUC",
        kFoldMethod: "Método", kFoldDeletion: "Deletion",
        kFoldInsertion: "Insertion", kFoldSparsity: "Sparsity",
        kFoldEntropy: "Entropy", kFoldStability: "Stability",
        // External validation
        extValidation: "Validación Externa",
        extAccuracy: "Accuracy", extF1: "F1-score", extAUC: "AUC",
        extNoData: "Sin datos",
        // Session rank
        sessionRank: "Ranking de Sesión",
        sessionConfig: "Configuración",
        sessionPath: "Ruta", sessionEpochs: "Épocas",
        sessionBatch: "Batch Size", sessionLR: "Learning Rate",
        sessionHeatmap: "Mapa de Calor (Wilcoxon)",
        sessionModels: "Modelos",
        // Reuse auto message template
        reuseMsg: "Hola, quiero reutilizar los parámetros de un experimento anterior:\n- Ruta: {path}\n- Modelos: {models}\n- Épocas: {epochs}\n- Batch Size: {batch}\n- Learning Rate: {lr}\n\n¿Me los listas y me preguntas si quiero cambiar algo antes de empezar?",
    },
    en: {
        cnnClassics: "Classic CNNs",
        navDiag: "Quick Diagnosis", navLab: "MLOps Laboratory", historyTitle: "History",
        noHistory: "No recent consultations.", logout: "Logout",
        subtitle: "Pneumonia Detection Assistant", modelLabel: "AI Model:",
        welcome: "Hello, doctor. Select an AI model and upload an X-ray.",
        dropText: "Drag an X-ray or click", analyzing: "Analyzing...",
        diagnosis: "Diagnosis", confidence: "Confidence", heatmap: "XAI Heatmap",
        downloadPdf: "Download PDF", recovered: "Recovered from History",
        infModel: "Inference Model", back: "Back",
        cdRename: "Rename", cdDelete: "Delete", cdTitle: "Consultation Detail",
        cdPatient: "Patient", cdOrigLabel: "Original X-ray",
        cdXaiLabel: "XAI Heatmaps", cdDiagLabel: "Diagnosis",
        cdConfLabel: "Confidence", cdModelLabel: "Model",
        adminBtn: "Administration Panel", adminModalTitle: "Users",
        adminConsultTitle: "History", adminNoData: "No data",
        adminLoading: "Loading...", adminPatient: "Patient",
        adminDiagnosis: "Quick Diagnoses", adminLab: "Training Sessions",
        adminDeleteBtn: "Delete", adminRenameBtn: "Rename",
        adminStatus: "Status", adminProgress: "Progress", adminModel: "Model",
        adminDate: "Date", adminSave: "Save", adminCancel: "Cancel",
        adminConfirmDelete: "Delete this consultation?", adminDeleted: "Deleted",
        adminRenamed: "Renamed", adminRenamePrompt: "New patient name:",
        adminLabsTitle: "Lab Sessions", adminSessionId: "Session",
        adminDeleteLabConfirm: "Delete this lab session?",
        adminLabDeleted: "Session deleted", adminOpen: "Open",
        loginTitle: "Log In", loginUser: "Username", loginPass: "Password",
        loginBtn: "Sign In", loginFooterTxt: "Don't have an account?",
        loginFooterLink: "Register here", loginErr: "Invalid credentials",
        registerTitle: "Register", registerFname: "First Name", registerLname: "Last Name",
        registerRole: "Role", registerBtn: "Create Account",
        registerFooterTxt: "Already have an account?", registerFooterLink: "Sign In",
        registerOpt1: "Physician", registerOpt2: "Admin", registerOpt3: "Researcher",
        registerOpt4: "Student", registerProcessing: "Processing...",
        registerErrExists: "User already exists", registerErrServer: "Server error",
        registerSuccess: "Registration successful",
        trainConfigAssistant: "Configuration Assistant",
        trainChatPlaceholder: "Write your answer here, ask for the path, or ask me anything...",
        trainFolder: "Browse Folder",
        trainSession: "Session", trainRankingTitle: "Global Ranking & Statistical Analysis",
        trainBackToAssistant: "Back to Assistant",
        trainRename: "Rename", trainReuseConfig: "Reuse Configuration",
        trainExternalValidation: "External Validation",
        trainGeneratePdf: "Generate PDF Report",
        trainRecalculateWilcoxon: "Recalculate Wilcoxon",
        trainPos: "Position", trainModel: "Model", trainMeanAuc: "Mean AUC",
        trainStdDev: "Std Dev", trainNoSessions: "No saved sessions",
        trainThinking: "Thinking...", trainConnectionError: "Connection error.",
        trainReady: "All set! I've configured the machines with those parameters. Starting training:",
        trainParseError: "Oops! I understood the parameters but there was an internal error reading them. Can you repeat them?",
        trainFolderError: "Could not open Windows explorer.",
        trainCancel: "Cancel", trainConfirm: "Rename",
        trainRenamePrompt: "New name for this session:",
        trainDeleteConfirm: "PERMANENTLY delete session '{session}'?",
        trainNoConfig: "No saved configuration for this session.",
        trainNoResults: "Results not found.",
        trainNoXai: "No XAI maps yet. Click 'Generate XAI & Metrics'.",
        trainGenerating: "Generating...",
        trainLogWaiting: "Waiting...",
        queueTitle: "Job Queue", queueEmpty: "No pending jobs",
        queueDiagnosis: "Diagnosis", queueTraining: "Training", queueExtValidation: "Ext. Validation",
        queueProcessing: "Processing...", queuePosition: "Position #{pos}",
        queueCancel: "Cancel", queueCancelConfirm: "Cancel this job?",
        queueEnqueued: "Diagnosis queued at position {pos} (job #{id})",
        queueEnqueuedExt: "External Validation queued as job #{id}",
        queueRunning: "Processing diagnosis...",
        queueCompleted: "Diagnosis completed",
        queueError: "Error: {msg}",
        queueEnqueueError: "Queue error",
        xaiChartOriginal: "Original X-ray",
        xaiChartSaliency: "Saliency Map",
        xaiChartSmoothGrad: "SmoothGrad",
        sessionDetail: "Consultation Detail",
        adminDiagCount: "diag.", adminLabCount: "lab.",
        adminNotFound: "User not found",
        adminSessionIdLabel: "Session", adminModelsLabel: "Models",
        adminClose: "Close",
        kFoldTitle: "K-Fold Results",
        kFoldXaiMetrics: "XAI Metrics",
        kFoldCalibration: "Calibration",
        kFoldBrier: "Brier Score", kFoldEce: "ECE",
        kFoldAccuracy: "Accuracy", kFoldPrecision: "Precision",
        kFoldRecall: "Recall", kFoldF1: "F1-Score", kFoldAUC: "AUC",
        kFoldMethod: "Method", kFoldDeletion: "Deletion",
        kFoldInsertion: "Insertion", kFoldSparsity: "Sparsity",
        kFoldEntropy: "Entropy", kFoldStability: "Stability",
        extValidation: "External Validation",
        extAccuracy: "Accuracy", extF1: "F1-score", extAUC: "AUC",
        extNoData: "No data",
        sessionRank: "Session Ranking",
        sessionConfig: "Configuration",
        sessionPath: "Path", sessionEpochs: "Epochs",
        sessionBatch: "Batch Size", sessionLR: "Learning Rate",
        sessionHeatmap: "Heatmap (Wilcoxon)",
        sessionModels: "Models",
        reuseMsg: "Hi, I want to reuse the parameters from a previous experiment:\n- Path: {path}\n- Models: {models}\n- Epochs: {epochs}\n- Batch Size: {batch}\n- Learning Rate: {lr}\n\nCan you list them and ask if I want to change anything before starting?",
    },
    zh: {
        cnnClassics: "经典 CNN",
        navDiag: "快速诊断", navLab: "MLOps 实验室", historyTitle: "历史",
        noHistory: "无", logout: "登出",
        subtitle: "肺炎检测助手", modelLabel: "AI 模型:",
        welcome: "医生您好。请选择模型并上传X光片。",
        dropText: "拖拽或点击", analyzing: "分析中...",
        diagnosis: "诊断", confidence: "置信度", heatmap: "XAI 热力图",
        downloadPdf: "下载 PDF", recovered: "已恢复",
        infModel: "模型", back: "返回",
        cdRename: "重命名", cdDelete: "删除", cdTitle: "咨询详情",
        cdPatient: "患者", cdOrigLabel: "原始X光片",
        cdXaiLabel: "XAI 热力图", cdDiagLabel: "诊断",
        cdConfLabel: "置信度", cdModelLabel: "模型",
        adminBtn: "管理面板", adminModalTitle: "用户",
        adminConsultTitle: "历史", adminNoData: "无数据",
        adminLoading: "加载中...", adminPatient: "患者",
        adminDiagnosis: "快速诊断", adminLab: "训练会话",
        adminDeleteBtn: "删除", adminRenameBtn: "重命名",
        adminStatus: "状态", adminProgress: "进度", adminModel: "模型",
        adminDate: "日期", adminSave: "保存", adminCancel: "取消",
        adminConfirmDelete: "删除此咨询？", adminDeleted: "已删除",
        adminRenamed: "已重命名", adminRenamePrompt: "患者新名称:",
        adminLabsTitle: "实验室会话", adminSessionId: "会话",
        adminDeleteLabConfirm: "删除此实验室会话？",
        adminLabDeleted: "会话已删除", adminOpen: "打开",
        loginTitle: "登录", loginUser: "用户名", loginPass: "密码",
        loginBtn: "进入系统", loginFooterTxt: "没有账号？",
        loginFooterLink: "在此注册", loginErr: "凭据无效",
        registerTitle: "注册", registerFname: "名字", registerLname: "姓氏",
        registerRole: "角色", registerBtn: "创建账户",
        registerFooterTxt: "已有账号？", registerFooterLink: "登录",
        registerOpt1: "医生", registerOpt2: "管理员", registerOpt3: "研究员",
        registerOpt4: "学生", registerProcessing: "处理中...",
        registerErrExists: "用户已存在", registerErrServer: "服务器错误",
        registerSuccess: "注册成功",
        trainConfigAssistant: "配置助手",
        trainChatPlaceholder: "在此处输入您的回答、询问路径或向我提问...",
        trainFolder: "浏览文件夹",
        trainSession: "会话", trainRankingTitle: "全局排名与统计分析",
        trainBackToAssistant: "返回助手",
        trainRename: "重命名", trainReuseConfig: "重用配置",
        trainExternalValidation: "外部验证",
        trainGeneratePdf: "生成 PDF 报告",
        trainRecalculateWilcoxon: "重新计算 Wilcoxon",
        trainPos: "位置", trainModel: "模型", trainMeanAuc: "平均 AUC",
        trainStdDev: "标准差", trainNoSessions: "无保存的会话",
        trainThinking: "思考中...", trainConnectionError: "连接错误。",
        trainReady: "准备好了！我已配置好参数。开始训练：",
        trainParseError: "哎呀！我理解了参数但读取时出现内部错误。你能重复一遍吗？",
        trainFolderError: "无法打开Windows资源管理器。",
        trainCancel: "取消", trainConfirm: "重命名",
        trainRenamePrompt: "此会话的新名称:",
        trainDeleteConfirm: "永久删除会话 '{session}'？",
        trainNoConfig: "此会话未保存配置。",
        trainNoResults: "未找到结果。",
        trainNoXai: "尚无XAI地图。请点击'生成 XAI 与指标'。",
        trainGenerating: "生成中...",
        trainLogWaiting: "等待中...",
        queueTitle: "作业队列", queueEmpty: "无待处理作业",
        queueDiagnosis: "诊断", queueTraining: "训练", queueExtValidation: "外部验证",
        queueProcessing: "处理中...", queuePosition: "位置 #{pos}",
        queueCancel: "取消", queueCancelConfirm: "取消此作业？",
        queueEnqueued: "诊断已排队，位置 {pos} (作业 #{id})",
        queueEnqueuedExt: "外部验证已排队，作业 #{id}",
        queueRunning: "处理诊断中...",
        queueCompleted: "诊断完成",
        queueError: "错误: {msg}",
        queueEnqueueError: "排队错误",
        xaiChartOriginal: "原始X光片",
        xaiChartSaliency: "显著性图",
        xaiChartSmoothGrad: "平滑梯度",
        sessionDetail: "咨询详情",
        adminDiagCount: "诊断", adminLabCount: "实验室",
        adminNotFound: "未找到用户",
        adminSessionIdLabel: "会话", adminModelsLabel: "模型",
        adminClose: "关闭",
        kFoldTitle: "K-Fold 结果",
        kFoldXaiMetrics: "XAI 指标",
        kFoldCalibration: "校准",
        kFoldBrier: "Brier 分数", kFoldEce: "ECE",
        kFoldAccuracy: "准确率", kFoldPrecision: "精确率",
        kFoldRecall: "召回率", kFoldF1: "F1 分数", kFoldAUC: "AUC",
        kFoldMethod: "方法", kFoldDeletion: "Deletion",
        kFoldInsertion: "Insertion", kFoldSparsity: "Sparsity",
        kFoldEntropy: "Entropy", kFoldStability: "Stability",
        extValidation: "外部验证",
        extAccuracy: "准确率", extF1: "F1 分数", extAUC: "AUC",
        extNoData: "无数据",
        sessionRank: "会话排名",
        sessionConfig: "配置",
        sessionPath: "路径", sessionEpochs: "轮数",
        sessionBatch: "批次大小", sessionLR: "学习率",
        sessionHeatmap: "热力图 (Wilcoxon)",
        sessionModels: "模型",
        reuseMsg: "你好，我想重复使用之前实验的参数：\n- 路径：{path}\n- 模型：{models}\n- 轮数：{epochs}\n- 批次大小：{batch}\n- 学习率：{lr}\n\n你能列出它们并问我在开始前是否想更改什么吗？",
    },
    hi: {
        cnnClassics: "क्लासिक CNN",
        navDiag: "त्वरित निदान", navLab: "एमएलओपीएस लैब", historyTitle: "इतिहास",
        noHistory: "कोई नहीं", logout: "लॉग आउट",
        subtitle: "निमोनिया जाँच", modelLabel: "एआई मॉडल:",
        welcome: "मॉडल चुनें और एक्स-रे अपलोड करें।",
        dropText: "क्लिक करें", analyzing: "विश्लेषण...",
        diagnosis: "निदान", confidence: "आत्मविश्वास", heatmap: "हीटमैप",
        downloadPdf: "PDF डाउनलोड", recovered: "इतिहास से",
        infModel: "मॉडल", back: "वापस",
        cdRename: "नम बदलें", cdDelete: "हटाएं", cdTitle: "परामर्श विवरण",
        cdPatient: "रोगी", cdOrigLabel: "मूल एक्स-रे",
        cdXaiLabel: "XAI हीटमैप", cdDiagLabel: "निदान",
        cdConfLabel: "आत्मविश्वास", cdModelLabel: "मॉडल",
        adminBtn: "प्रशासन पैनल", adminModalTitle: "उपयोगकर्ता",
        adminConsultTitle: "इतिहास", adminNoData: "कोई डेटा नहीं",
        adminLoading: "लोड हो रहा...", adminPatient: "रोगी",
        adminDiagnosis: "त्वरित निदान", adminLab: "प्रशिक्षण सत्र",
        adminDeleteBtn: "हटाएं", adminRenameBtn: "नम बदलें",
        adminStatus: "स्थिति", adminProgress: "प्रगति", adminModel: "मॉडल",
        adminDate: "तारीख", adminSave: "सहेजें", adminCancel: "रद्द करें",
        adminConfirmDelete: "इस परामर्श को हटाएं?", adminDeleted: "हटा दिया",
        adminRenamed: "नम बदल दिया", adminRenamePrompt: "रोगी का नया नाम:",
        adminLabsTitle: "प्रयोगशाला सत्र", adminSessionId: "सत्र",
        adminDeleteLabConfirm: "इस प्रयोगशाला सत्र को हटाएं?",
        adminLabDeleted: "सत्र हटा दिया", adminOpen: "खोलें",
        loginTitle: "लॉग इन करें", loginUser: "उपयोगकर्ता नाम", loginPass: "पासवर्ड",
        loginBtn: "सिस्टम में प्रवेश करें", loginFooterTxt: "खाता नहीं है?",
        loginFooterLink: "यहां पंजीकरण करें", loginErr: "अमान्य क्रेडेंशियल",
        registerTitle: "पंजीकरण", registerFname: "पहला नाम", registerLname: "अंतिम नाम",
        registerRole: "भूमिका", registerBtn: "खाता बनाएं",
        registerFooterTxt: "पहले से खाता है?", registerFooterLink: "साइन इन करें",
        registerOpt1: "चिकित्सक", registerOpt2: "प्रशासक", registerOpt3: "शोधकर्ता",
        registerOpt4: "छात्र", registerProcessing: "प्रक्रिया...",
        registerErrExists: "उपयोगकर्ता मौजूद है", registerErrServer: "सर्वर त्रुटि",
        registerSuccess: "पंजीकरण सफल",
        trainConfigAssistant: "कॉन्फ़िगरेशन सहायक",
        trainChatPlaceholder: "अपना उत्तर यहां लिखें, पथ पूछें, या मुझसे कुछ भी पूछें...",
        trainFolder: "फ़ोल्डर ब्राउज़ करें",
        trainSession: "सत्र", trainRankingTitle: "वैश्विक रैंकिंग और सांख्यिकीय विश्लेषण",
        trainBackToAssistant: "सहायक पर वापस",
        trainRename: "नम बदलें", trainReuseConfig: "कॉन्फ़िगरेशन पुनः उपयोग करें",
        trainExternalValidation: "बाहरी सत्यापन",
        trainGeneratePdf: "PDF रिपोर्ट बनाएं",
        trainRecalculateWilcoxon: "Wilcoxon पुनर्गणना",
        trainPos: "स्थान", trainModel: "मॉडल", trainMeanAuc: "औसत AUC",
        trainStdDev: "मानक विचलन", trainNoSessions: "कोई सत्र नहीं",
        trainThinking: "सोच रहा...", trainConnectionError: "कनेक्शन त्रुटि।",
        trainReady: "सब तैयार! मैंने पैरामीटर कॉन्फ़िगर कर दिए हैं। प्रशिक्षण शुरू:",
        trainParseError: "ओह! मैंने पैरामीटर समझ लिए लेकिन आंतरिक त्रुटि हुई। क्या आप दोहरा सकते हैं?",
        trainFolderError: "Windows एक्सप्लोरर नहीं खोल सका।",
        trainCancel: "रद्द करें", trainConfirm: "नम बदलें",
        trainRenamePrompt: "इस सत्र का नया नाम:",
        trainDeleteConfirm: "स्थायी रूप से सत्र '{session}' हटाएं?",
        trainNoConfig: "इस सत्र के लिए कोई कॉन्फ़िगरेशन नहीं।",
        trainNoResults: "परिणाम नहीं मिले।",
        trainNoXai: "अभी तक कोई XAI मैप नहीं। 'XAI और मीट्रिक जनरेट करें' पर क्लिक करें।",
        trainGenerating: "जनरेट हो रहा...",
        trainLogWaiting: "प्रतीक्षा...",
        queueTitle: "कार्य कतार", queueEmpty: "कोई लंबित कार्य नहीं",
        queueDiagnosis: "निदान", queueTraining: "प्रशिक्षण", queueExtValidation: "बाहरी सत्यापन",
        queueProcessing: "प्रक्रिया...", queuePosition: "स्थान #{pos}",
        queueCancel: "रद्द करें", queueCancelConfirm: "यह कार्य रद्द करें?",
        queueEnqueued: "निदान कतार में स्थान {pos} (कार्य #{id})",
        queueEnqueuedExt: "बाहरी सत्यापन कतार में कार्य #{id}",
        queueRunning: "निदान प्रक्रिया...",
        queueCompleted: "निदान पूर्ण",
        queueError: "त्रुटि: {msg}",
        queueEnqueueError: "कतार त्रुटि",
        xaiChartOriginal: "मूल एक्स-रे",
        xaiChartSaliency: "सैलिएंसी मैप",
        xaiChartSmoothGrad: "स्मूथग्रेड",
        sessionDetail: "परामर्श विवरण",
        adminDiagCount: "निदान", adminLabCount: "प्रयोगशाला",
        adminNotFound: "उपयोगकर्ता नहीं मिला",
        adminSessionIdLabel: "सत्र", adminModelsLabel: "मॉडल",
        adminClose: "बंद करें",
        kFoldTitle: "K-Fold परिणाम",
        kFoldXaiMetrics: "XAI मीट्रिक",
        kFoldCalibration: "कैलिब्रेशन",
        kFoldBrier: "Brier स्कोर", kFoldEce: "ECE",
        kFoldAccuracy: "सटीकता", kFoldPrecision: "परिशुद्धता",
        kFoldRecall: "रिकॉल", kFoldF1: "F1-स्कोर", kFoldAUC: "AUC",
        kFoldMethod: "विधि", kFoldDeletion: "Deletion",
        kFoldInsertion: "Insertion", kFoldSparsity: "Sparsity",
        kFoldEntropy: "Entropy", kFoldStability: "Stability",
        extValidation: "बाहरी सत्यापन",
        extAccuracy: "सटीकता", extF1: "F1-स्कोर", extAUC: "AUC",
        extNoData: "कोई डेटा नहीं",
        sessionRank: "सत्र रैंकिंग",
        sessionConfig: "कॉन्फ़िगरेशन",
        sessionPath: "पथ", sessionEpochs: "एपॉक",
        sessionBatch: "बैच आकार", sessionLR: "सीखने की दर",
        sessionHeatmap: "हीटमैप (Wilcoxon)",
        sessionModels: "मॉडल",
        reuseMsg: "नमस्ते, मैं पिछले प्रयोग के पैरामीटर पुनः उपयोग करना चाहता हूं:\n- पथ: {path}\n- मॉडल: {models}\n- एपॉक: {epochs}\n- बैच आकार: {batch}\n- सीखने की दर: {lr}\n\nक्या आप उन्हें सूचीबद्ध कर सकते हैं और पूछ सकते हैं कि क्या मैं शुरू करने से पहले कुछ बदलना चाहता हूं?",
    }
};

let currentLang = localStorage.getItem('appLang') || 'es';

function t(key) {
    const lang = currentLang || localStorage.getItem('appLang') || 'es';
    const langDict = dict[lang] || dict.es;
    return langDict[key] || dict.es[key] || key;
}

let _refreshing = false;

async function refreshAuth() {
    if (_refreshing) return false;
    _refreshing = true;
    try {
        const resp = await fetch('/api/token/refresh', { method: 'POST' });
        if (resp.ok) return true;
    } catch (e) {}
    _refreshing = false;
    return false;
}

function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        if (icon) icon.className = 'fa-solid fa-moon text-lg';
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        if (icon) icon.className = 'fa-solid fa-sun text-lg';
        localStorage.setItem('theme', 'dark');
    }
}

function restoreTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        const icon = document.getElementById('theme-icon');
        if (icon) icon.className = 'fa-solid fa-sun text-lg';
    }
}

function restoreLang() {
    const savedLang = localStorage.getItem('appLang');
    if (savedLang) {
        currentLang = savedLang;
        const selector = document.getElementById('lang-selector');
        if (selector) selector.value = savedLang;
    }
}

function changeLanguage() {
    const selector = document.getElementById('lang-selector');
    if (selector) {
        currentLang = selector.value;
    }
    localStorage.setItem('appLang', currentLang);

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.innerText = t(key);
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        el.placeholder = t(key);
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        el.title = t(key);
    });

    document.querySelectorAll('[data-i18n-label]').forEach(el => {
        const key = el.getAttribute('data-i18n-label');
        el.setAttribute('label', t(key));
    });
}

function showToast(message, type) {
    var toast = document.createElement('div');
    var isDark = document.documentElement.classList.contains('dark');
    var bgColor = type === 'error' ? (isDark ? '#7f1d1d' : '#fef2f2') : (isDark ? '#065f46' : '#f0fdf4');
    var textColor = type === 'error' ? (isDark ? '#fca5a5' : '#991b1b') : (isDark ? '#6ee7b7' : '#065f46');
    var borderColor = type === 'error' ? (isDark ? '#991b1b' : '#fecaca') : (isDark ? '#047857' : '#bbf7d0');
    toast.setAttribute('style', 'position:fixed;bottom:24px;right:24px;z-index:99999;background:' + bgColor + ';color:' + textColor + ';border:1px solid ' + borderColor + ';border-radius:12px;padding:12px 20px;font-size:14px;font-weight:600;box-shadow:0 10px 25px rgba(0,0,0,0.15);display:flex;align-items:center;gap:10px;max-width:400px;transition:opacity 0.3s,transform 0.3s;transform:translateY(20px);opacity:0');
    toast.innerHTML = '<i class="fa-solid ' + (type === 'error' ? 'fa-circle-exclamation' : 'fa-check-circle') + '"></i> ' + message;
    document.body.appendChild(toast);
    requestAnimationFrame(function() {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    });
    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(function() { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 300);
    }, 4000);
}
