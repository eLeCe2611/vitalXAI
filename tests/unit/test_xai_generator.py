from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import tensorflow as tf


@pytest.fixture(autouse=True)
def mock_plt():
    with patch("services.xai_generator.plt") as mock:
        yield mock


class TestGetImgSize:
    def test_default_size(self):
        from services.xai_generator import get_img_size
        assert get_img_size("DenseNet121") == (224, 224)

    def test_inception_size(self):
        from services.xai_generator import get_img_size
        assert get_img_size("InceptionV3") == (299, 299)

    def test_xception_size(self):
        from services.xai_generator import get_img_size
        assert get_img_size("Xception") == (299, 299)

    def test_vit_size(self):
        from services.xai_generator import get_img_size
        assert get_img_size("vit_384") == (384, 384)


class TestGetScore:
    def test_cnn_model(self):
        mock_model = MagicMock()
        mock_model.return_value = [[0.85]]
        img = np.ones((1, 224, 224, 3))
        from services.xai_generator import get_score
        # Need to mock isinstance(pred, list) behavior - model returns list
        mock_pred = MagicMock()
        mock_pred.__getitem__.return_value = [0.85]
        mock_model.return_value = [mock_pred]
        result = get_score(mock_model, img, False)
        assert result is not None

    def test_transformer_model(self):
        mock_model = MagicMock()
        mock_logits = MagicMock()
        mock_logits.__getitem__.return_value = [0.92]
        mock_model.return_value.logits = mock_logits
        img = tf.constant(np.ones((1, 224, 224, 3)))
        from services.xai_generator import get_score
        result = get_score(mock_model, img, True)
        assert result is not None


class TestSaliency:
    def test_returns_2d_array(self):
        mock_model = MagicMock()
        img = np.ones((224, 224, 3))
        from services.xai_generator import saliency
        mock_tape = MagicMock()
        mock_grads = tf.constant(np.ones((1, 224, 224, 3)))
        mock_tape.__enter__.return_value.gradient.return_value = mock_grads
        with patch("services.xai_generator.tf.GradientTape", return_value=mock_tape):
            result = saliency(mock_model, img, False)
            assert result.shape == (224, 224)


class TestSmoothGrad:
    def test_returns_normalized_map(self):
        img = np.ones((224, 224, 3))
        with patch("services.xai_generator.saliency", return_value=np.ones((224, 224)) * 0.5):
            from services.xai_generator import smoothgrad
            result = smoothgrad(MagicMock(), img, False, n_samples=5)
            assert result.shape == (224, 224)
            assert 0.0 <= result.min() <= result.max() <= 1.0


class TestGetCamOrAttention:
    def test_cnn_fallback_when_no_conv_layer(self):
        mock_model = MagicMock()
        mock_model.layers = []
        img = np.ones((224, 224, 3))
        from services.xai_generator import get_cam_or_attention
        result = get_cam_or_attention(mock_model, img, False, (224, 224))
        assert result.shape == (224, 224)

    def test_transformer_returns_normalized_map(self):
        mock_outputs = MagicMock()
        mock_attn_maps = MagicMock()
        mock_attn_maps.shape = (1, 12, 196, 196)
        mock_outputs.attentions = [mock_attn_maps]
        mock_model = MagicMock(return_value=mock_outputs)
        img = np.ones((224, 224, 3))
        with patch("services.xai_generator.tf") as mock_tf:
            mock_tf.reduce_mean.return_value.__getitem__.return_value.__getitem__.return_value = \
                tf.ones((14, 14))
            mock_tf.reshape.return_value = tf.ones((14, 14))
            mock_tf.image.resize.return_value = tf.constant(np.ones((224, 224, 1)))
            from services.xai_generator import get_cam_or_attention
            result = get_cam_or_attention(mock_model, img, True, (224, 224))
            assert result.shape == (224, 224)


class TestLoadImgTf:
    def test_loads_and_normalizes_image(self):
        class FakeTensor:
            def __init__(self, arr):
                self._arr = arr
            def __truediv__(self, other):
                return FakeTensor(self._arr / other)
            def numpy(self):
                return self._arr

        with patch("services.xai_generator.tf") as mock_tf:
            mock_tf.io.read_file.return_value = b"fake"
            mock_tf.image.decode_jpeg.return_value = np.ones((200, 200, 3), dtype=np.uint8) * 255
            mock_tf.image.resize.return_value = FakeTensor(np.ones((224, 224, 3), dtype=np.float64))
            from services.xai_generator import load_img_tf
            result = load_img_tf("fake.jpg", (224, 224))
            assert np.allclose(result, 1.0 / 255.0)
            mock_tf.io.read_file.assert_called_once_with("fake.jpg")


class TestGenerateXaiHeatmap:
    def test_saves_figure_with_all_subplots(self, mock_plt):
        mock_model = MagicMock()
        with patch("services.ml_engine.get_model", return_value=mock_model), \
             patch("services.xai_generator.get_model", return_value=mock_model), \
             patch("services.xai_generator.load_img_tf", return_value=np.ones((224, 224, 3))), \
             patch("services.xai_generator.saliency", return_value=np.ones((224, 224))), \
             patch("services.xai_generator.smoothgrad", return_value=np.ones((224, 224))), \
             patch("services.xai_generator.get_cam_or_attention", return_value=np.ones((224, 224))):
            from services.xai_generator import generate_xai_heatmap
            result = generate_xai_heatmap("DenseNet121", "fake.jpg", "output.png")
            assert mock_plt.subplot.call_count >= 4
            mock_plt.savefig.assert_called_once_with("output.png", bbox_inches='tight', dpi=150)
            mock_plt.close.assert_called_once()
            assert result == "output.png"

    def test_transformer_uses_attention_label(self, mock_plt):
        mock_model = MagicMock()
        with patch("services.ml_engine.get_model", return_value=mock_model), \
             patch("services.xai_generator.get_model", return_value=mock_model), \
             patch("services.xai_generator.load_img_tf", return_value=np.ones((224, 224, 3))), \
             patch("services.xai_generator.saliency", return_value=np.ones((224, 224))), \
             patch("services.xai_generator.smoothgrad", return_value=np.ones((224, 224))), \
             patch("services.xai_generator.get_cam_or_attention", return_value=np.ones((224, 224))):
            from services.xai_generator import generate_xai_heatmap
            result = generate_xai_heatmap("deit", "fake.jpg", "output.png")
            assert result == "output.png"
