# Domain Model

## Entities

| Entity | Meaning | Fields | Notes |
|---|---|---|---|
| User | Medical professional using the platform | id, username (email), password_hash, first_name, last_name, role | Registered via email, authenticated with JWT |
| Consultation | Single X-ray diagnosis request | id, user_id, model_name, original_image_path, xai_image_path, prediction_label, confidence_score, patient_name, pdf_path, timestamp | Links user, model, image, XAI, and PDF report |
| TrainingJob | MLOps training session metadata | id, user_id, dataset_path, model_name, status, progress, metrics_json, started_at, finished_at | Tracks progress of offline training pipelines |
| RefreshToken | JWT refresh token for session management | id, user_id, token_hash, expires_at, revoked, created_at | Hashed (SHA-256), with rotation and expiry |

## Relationships

```
User 1──N Consultation  : one user can have many diagnosis consultations
User 1──N TrainingJob   : one user can start many training sessions
User 1──N RefreshToken  : one user can have multiple active refresh tokens
Consultation N──1 User  : each consultation belongs to one user (FK, user_id NOT NULL)
TrainingJob N──1 User   : each training job belongs to one user (FK, user_id NOT NULL, CASCADE DELETE)
RefreshToken N──1 User  : each refresh token belongs to one user (FK, CASCADE DELETE)
```

## Business Rules

### Authentication
- Users register with email (username field), password (min 8 chars, stored as bcrypt hash), first name, last name, and role.
- Login verifies email + bcrypt password. Same error message for wrong email or wrong password (prevents user enumeration).
- Session uses JWT: access token (15 min) + refresh token (7 days, with rotation).
- Refresh token rotation: using a refresh token invalidates the previous one. Grace period of 60s for concurrent requests.
- Theft detection: if a rotated token is reused outside the 60s grace period, ALL refresh tokens for that user are revoked immediately.
- Logout revokes the refresh token.

### Diagnosis (XAI)
- User uploads a chest X-ray (JPEG/PNG, max 10MB) and selects an AI model.
- System runs inference (CNN or Transformer) and returns label (Normal/Neumonía) + confidence score.
- System generates XAI heatmaps: Saliency, SmoothGrad, Grad-CAM (CNN) or Attention Maps (Transformer).
- System generates a PDF medical report with diagnosis and heatmaps.
- All consultations are saved to history, grouped by model.

### MLOps Training
- User configures training via chatbot (Groq/`openai/gpt-oss-120b`) or direct form.
- Training runs as background subprocess executing external scripts (pneumoniacnn-main/).
- Each model goes through: train → XAI qualitative → XAI quantitative.
- After all models, run ranking (Wilcoxon statistical comparison).
- Optional: external validation + DeLong test.
- Results include: K-fold CV metrics, calibration data, XAI metrics, ROC curves, statistical matrices.

### API
- CSRF protection via double-submit cookie pattern on all state-changing methods.
- Rate limiting: 5 requests/min on /login, 60 requests/min on all other endpoints.
- Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy.

## Glossary

| Term | Meaning |
|---|---|
| XAI | Explainable Artificial Intelligence — techniques to visualize model decisions |
| Saliency Map | Gradient-based heatmap showing pixel importance |
| SmoothGrad | Saliency map averaged over noisy input samples |
| Grad-CAM | Class Activation Mapping for CNN models |
| Attention Map | Self-attention visualization for Transformer models |
| AUC | Area Under the ROC Curve — model performance metric |
| K-Fold CV | Cross-validation splitting data into K folds |
| Wilcoxon Test | Non-parametric statistical test for model comparison |
| DeLong Test | Statistical test comparing AUC of two models |
| MLOps | Machine Learning Operations — pipeline for training and evaluation |
| CNN | Convolutional Neural Network |
| Transformer | Vision Transformer architecture (DeiT, Swin, ViT) |
| JWT | JSON Web Token — stateless authentication |
| CSRF | Cross-Site Request Forgery — web security attack |
| CSP | Content Security Policy — HTTP security header |
