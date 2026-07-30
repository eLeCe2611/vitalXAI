from unittest.mock import MagicMock


class TestGetText:
    def test_returns_spanish_by_default(self):
        from services.lang import get_text
        result = get_text("no_autenticado")
        assert result == "No autenticado"

    def test_returns_english_when_specified(self):
        from services.lang import get_text
        result = get_text("no_autenticado", lang="en")
        assert result == "Not authenticated"

    def test_returns_chinese_when_specified(self):
        from services.lang import get_text
        result = get_text("no_autenticado", lang="zh")
        assert result is not None
        assert len(result) > 0

    def test_returns_hindi_when_specified(self):
        from services.lang import get_text
        result = get_text("no_autenticado", lang="hi")
        assert result is not None
        assert len(result) > 0

    def test_fallback_to_spanish_for_missing_key(self):
        from services.lang import get_text
        result = get_text("clave_inexistente", lang="en")
        assert result == "clave_inexistente"

    def test_fallback_to_key_for_missing_lang(self):
        from services.lang import get_text
        result = get_text("clave_inexistente", lang="fr")
        assert result == "clave_inexistente"

    def test_pneumonia_label_spanish(self):
        from services.lang import get_text
        assert get_text("label_pneumonia", lang="es") == "Neumonía"
        assert get_text("label_normal", lang="es") == "Normal"

    def test_pneumonia_label_english(self):
        from services.lang import get_text
        assert get_text("label_pneumonia", lang="en") == "Pneumonia"
        assert get_text("label_normal", lang="en") == "Normal"


class TestGetLangFromCookie:
    def test_returns_es_when_no_cookie(self):
        from services.lang import get_lang_from_cookie
        request = MagicMock()
        request.cookies.get.return_value = None
        result = get_lang_from_cookie(request)
        assert result == "es"

    def test_returns_lang_from_cookie(self):
        from services.lang import get_lang_from_cookie
        request = MagicMock()
        request.cookies.get.return_value = "en"
        result = get_lang_from_cookie(request)
        assert result == "en"

    def test_returns_zh_from_cookie(self):
        from services.lang import get_lang_from_cookie
        request = MagicMock()
        request.cookies.get.return_value = "zh"
        result = get_lang_from_cookie(request)
        assert result == "zh"

    def test_fallback_to_es_for_invalid_lang(self):
        from services.lang import get_lang_from_cookie
        request = MagicMock()
        request.cookies.get.return_value = "fr"
        result = get_lang_from_cookie(request)
        assert result == "es"
