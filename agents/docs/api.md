# API Contracts

## Conventions
- Base URL: `http://127.0.0.1:8000`
- Auth: JWT-based via httponly cookies (`access_token` + `refresh_token`).
- CSRF: Double-submit cookie pattern. All POST/PUT/DELETE requests must include `X-CSRF-Token` header matching the `csrf_token` cookie.
- Rate limiting: 5 requests/minute on `/login`, 60 requests/minute on all other endpoints (slowapi in-memory).
- Error format: `{"error": "<message>"}` or `{"status": "error", "code": "<code>", "message": "<msg>"}`
- Pagination: None
- Versioning/compatibility: None

## Routes

### Auth
| Method | Path | Request | Response | Notes |
|---|---|---|---|---|
| GET | `/` | — | HTML login page | Query param `?error=1` shows error |
| POST | `/login` | Form: username, password | 303 redirect to `/dashboard` or `/?error=1` | Sets `access_token` + `refresh_token` httponly cookies. Password verified with bcrypt. Rate limited: 5/min. |
| POST | `/api/token/refresh` | Cookie: refresh_token | `{"status": "success"}` | Rotates refresh token, sets new access_token + refresh_token cookies |
| GET | `/dashboard` | Cookie: access_token | HTML dashboard | 303 redirect to `/` if no valid JWT |
| GET | `/training` | Cookie: access_token | HTML training page | 303 redirect to `/` if no valid JWT |
| GET | `/logout` | Cookie: access_token, refresh_token | 303 redirect to `/` | Revokes refresh token, deletes cookies |
| GET | `/register` | — | HTML register form | |
| POST | `/api/register` | Form: username, password, first_name, last_name, role | `{"status": "success", "code": "success_register"}` | Sets `access_token` + `refresh_token` httponly cookies on success. Validates email format, password >= 8 chars |

### Inference
| Method | Path | Request | Response | Notes |
|---|---|---|---|---|
| POST | `/predict` | Form: model_name + file (image/jpeg, image/png, max 10MB) | `{"status": "success", "label", "confidence", "original_image", "xai_image", "pdf_report", "model_used"}` | Requires auth cookie. Validates file type and size |

### History
| Method | Path | Request | Response | Notes |
|---|---|---|---|---|
| GET | `/api/history` | Cookie: access_token | `{"status": "success", "data": [...]}` | Returns consultations ordered by timestamp DESC |
| POST | `/api/history/update_name` | Form: consultation_id, new_name | `{"status": "success"}` | |
| POST | `/api/history/delete` | Form: consultation_id | `{"status": "success"}` | |

### Training / MLOps
| Method | Path | Request | Response | Notes |
|---|---|---|---|---|
| POST | `/api/chat` | Form: session_id, message | `{"response": "<bot_message>"}` | Groq/Llama 3.3-70B chatbot |
| GET | `/api/train/browse` | — | `{"path": "<selected_folder>"}` | Opens native Windows folder dialog (Tkinter) |
| POST | `/api/train/start` | Form: model_names, dataset_path, epochs, batch_size, learning_rate | `{"status": "success", "message": "...", "session_id": "..."}` | Launches background training queue |
| GET | `/api/train/logs` | — | `{"logs": "<last 60 lines>"}` | |
| GET | `/api/train/models` | — | `{"status": "success", "sessions": [{"session_id", "models": [...]}]}` | |
| GET | `/api/train/results/{session_id}/{model_name}` | — | `{"status": "success", "data": [...], "images": [...], "calib": {...}, "xai_metrics": [...]}` | |
| POST | `/api/train/run_eval` | Form: session_id, model_name, dataset_path | `{"status": "success", "message": "..."}` | Runs XAI scripts synchronously |
| DELETE | `/api/train/session/{session_id}` | — | `{"status": "success"}` | |
| POST | `/api/train/session/rename` | Form: old_name, new_name | `{"status": "success", "new_name": "..."}` | |
| POST | `/api/train/session/compare` | Form: session_id | `{"status": "success"}` | Recalculates Wilcoxon statistics |
| GET | `/api/train/session/{session_id}/ranking` | — | `{"status": "success", "ranking": [...], "heatmap": "...", "config": {...}}` | |
| POST | `/api/train/session/external_validation` | Form: session_id, dataset_path | `{"status": "success"}` | |
| GET | `/api/train/session/{session_id}/external_results` | — | `{"status": "success", "metrics": [...], "roc": "...", "delong": "..."}` | |
| GET | `/api/train/session/{session_id}/report` | — | PDF file download | Generates MLOps medical report PDF |

## Security
- **Authentication**: JWT access token (15 min) + refresh token (7 days, with rotation) in httponly cookies
- **Password storage**: bcrypt hashing (via bcrypt library)
- **CSRF**: Double-submit cookie pattern via Starlette middleware
- **Rate limiting**: slowapi in-memory (5/min login, 60/min general)
- **Security headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy via middleware
- **Input validation**: Email format, password >= 8 chars, file type (JPEG/PNG) and size (max 10MB)
