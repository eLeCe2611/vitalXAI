from unittest.mock import MagicMock, patch


class TestGenerateMedicalReport:
    def test_pneumonia_label_uses_red(self):
        mock_pdf = MagicMock()
        with patch("services.pdf_generator.PDFReport", return_value=mock_pdf):
            from services.pdf_generator import generate_medical_report
            generate_medical_report("img.jpg", "xai.jpg", "Neumonía", 85.0, "DenseNet121")
            text_color_calls = mock_pdf.set_text_color.call_args_list
            red_calls = [c for c in text_color_calls if c[0] == (192, 57, 43)]
            assert len(red_calls) >= 1

    def test_normal_label_uses_green(self):
        mock_pdf = MagicMock()
        with patch("services.pdf_generator.PDFReport", return_value=mock_pdf):
            from services.pdf_generator import generate_medical_report
            generate_medical_report("img.jpg", "xai.jpg", "Normal", 95.0, "MobileNetV2")
            text_color_calls = mock_pdf.set_text_color.call_args_list
            green_calls = [c for c in text_color_calls if c[0] == (39, 174, 96)]
            assert len(green_calls) >= 1

    def test_returns_pdf_path(self):
        mock_pdf = MagicMock()
        with patch("services.pdf_generator.PDFReport", return_value=mock_pdf), \
             patch("services.pdf_generator.os.makedirs"):
            from services.pdf_generator import generate_medical_report
            result = generate_medical_report("img.jpg", "xai.jpg", "Neumonía", 85.0, "DenseNet121")
            assert result is not None
            assert isinstance(result, str)

    def test_handles_image_error_gracefully(self):
        mock_pdf = MagicMock()
        mock_pdf.image.side_effect = [Exception("File not found"), None]
        with patch("services.pdf_generator.PDFReport", return_value=mock_pdf):
            from services.pdf_generator import generate_medical_report
            result = generate_medical_report("bad_img.jpg", "xai.jpg", "Normal", 90.0, "ResNet50")
            assert result is not None
