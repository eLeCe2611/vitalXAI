import os
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


@pytest.fixture
def mock_cv2():
    with patch("services.ml_engine.cv2") as mock:
        mock.imread.return_value = np.zeros((224, 224, 3), dtype=np.uint8)
        yield mock


@pytest.fixture
def mock_tf():
    with patch("services.ml_engine.tf") as mock:
        yield mock


class TestGetModel:
    def test_cnn_model_loads_keras(self):
        with patch("os.path.exists", return_value=True), \
             patch("services.ml_engine.load_model") as mock_load:
            from services.ml_engine import get_model, loaded_models
            loaded_models.clear()
            result = get_model("DenseNet121")
            expected_path = os.path.join("pneumoniacnn-main", "results", "DenseNet121", "best_fold1.keras")
            mock_load.assert_called_once_with(expected_path)
            assert result == mock_load.return_value

    def test_transformer_model_loads_hf(self):
        with patch("os.path.exists", return_value=True), \
             patch("transformers.TFAutoModelForImageClassification") as mock_hf:
            from services.ml_engine import get_model, loaded_models
            loaded_models.clear()
            mock_instance = MagicMock()
            mock_hf.from_pretrained.return_value = mock_instance
            result = get_model("deit")
            mock_hf.from_pretrained.assert_called_once_with(
                "facebook/deit-base-distilled-patch16-224",
                num_labels=1, ignore_mismatched_sizes=True, output_attentions=True
            )
            mock_instance.load_weights.assert_called_once()
            assert result == mock_instance

    def test_caches_model(self):
        with patch("os.path.exists", return_value=True), \
             patch("services.ml_engine.load_model") as mock_load:
            from services.ml_engine import get_model, loaded_models
            loaded_models.clear()
            m1 = get_model("DenseNet121")
            m2 = get_model("DenseNet121")
            assert m1 is m2
            assert mock_load.call_count == 1

    def test_raises_on_missing_cnn_weights(self):
        with patch("os.path.exists", return_value=False):
            from services.ml_engine import get_model, loaded_models
            loaded_models.clear()
            with pytest.raises(FileNotFoundError, match="no encontrado"):
                get_model("DenseNet121")

    def test_raises_on_missing_transformer_weights(self):
        with patch("os.path.exists", return_value=False), \
             patch("transformers.TFAutoModelForImageClassification"):
            from services.ml_engine import get_model, loaded_models
            loaded_models.clear()
            with pytest.raises(FileNotFoundError, match="no encontrados"):
                get_model("deit")


class TestProcessAndPredict:
    @pytest.fixture
    def mock_model_cnn(self):
        model = MagicMock()
        model.predict.return_value = [[0.85]]
        return model

    def test_cnn_prediction_pneumonia(self, mock_cv2, mock_tf, mock_model_cnn):
        with patch("services.ml_engine.get_model", return_value=mock_model_cnn):
            from services.ml_engine import process_and_predict
            label, confidence = process_and_predict("DenseNet121", "fake.jpg")
            mock_cv2.imread.assert_called_once_with("fake.jpg")
            assert label == "Neumonía"
            assert confidence == 85.0

    def test_cnn_prediction_normal(self, mock_cv2, mock_tf, mock_model_cnn):
        mock_model_cnn.predict.return_value = [[0.3]]
        with patch("services.ml_engine.get_model", return_value=mock_model_cnn):
            from services.ml_engine import process_and_predict
            label, confidence = process_and_predict("DenseNet121", "fake.jpg")
            assert label == "Normal"
            assert confidence == 70.0

    def test_transformer_prediction(self, mock_cv2, mock_tf):
        mock_tf.sigmoid.return_value = [0.92]
        mock_tf.convert_to_tensor.return_value = "tensor"
        mock_model = MagicMock()
        mock_model.return_value.logits.__getitem__.return_value = [0.92]
        with patch("services.ml_engine.get_model", return_value=mock_model):
            from services.ml_engine import process_and_predict
            label, confidence = process_and_predict("deit", "fake.jpg")
            assert label == "Neumonía"

    def test_image_size_for_inception(self, mock_cv2, mock_tf, mock_model_cnn):
        with patch("services.ml_engine.get_model", return_value=mock_model_cnn):
            from services.ml_engine import process_and_predict
            process_and_predict("InceptionV3", "fake.jpg")
            call_args = mock_cv2.resize.call_args
            assert call_args[0][1] == (299, 299)

    def test_image_size_for_vit384(self, mock_cv2, mock_tf, mock_model_cnn):
        with patch("services.ml_engine.get_model", return_value=mock_model_cnn):
            from services.ml_engine import process_and_predict
            process_and_predict("vit_384", "fake.jpg")
            call_args = mock_cv2.resize.call_args
            assert call_args[0][1] == (384, 384)

    def test_confidence_clamped_to_0_100(self, mock_cv2, mock_tf, mock_model_cnn):
        mock_model_cnn.predict.return_value = [[0.999]]
        with patch("services.ml_engine.get_model", return_value=mock_model_cnn):
            from services.ml_engine import process_and_predict
            _, confidence = process_and_predict("DenseNet121", "fake.jpg")
            assert 0 <= confidence <= 100
