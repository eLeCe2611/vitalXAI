from unittest.mock import MagicMock, patch


class TestGetImgSize:
    def test_default_size(self):
        from services.trainer_engine import get_img_size
        assert get_img_size("DenseNet121") == (224, 224)

    def test_inception_size(self):
        from services.trainer_engine import get_img_size
        assert get_img_size("InceptionV3") == (299, 299)

    def test_efficientnetb1(self):
        from services.trainer_engine import get_img_size
        assert get_img_size("EfficientNetB1") == (240, 240)

    def test_efficientnetb7(self):
        from services.trainer_engine import get_img_size
        assert get_img_size("EfficientNetB7") == (600, 600)

    def test_efficientnetv2s(self):
        from services.trainer_engine import get_img_size
        assert get_img_size("EfficientNetV2S") == (384, 384)


class TestBuildDataframe:
    def test_creates_dataframe_with_labels(self):
        with patch("services.trainer_engine.os.listdir") as mock_listdir, \
             patch("services.trainer_engine.os.path.isdir", return_value=True):
            mock_listdir.side_effect = [
                ["NORMAL", "PNEUMONIA"],
                ["img1.jpg", "img2.png"],
                ["img3.jpg"],
            ]
            from services.trainer_engine import build_dataframe
            df = build_dataframe("/fake/dataset")
            assert len(df) == 3
            assert list(df["label_id"]) == [0, 0, 1]

    def test_ignores_non_image_files(self):
        with patch("services.trainer_engine.os.listdir") as mock_listdir, \
             patch("services.trainer_engine.os.path.isdir", return_value=True):
            mock_listdir.side_effect = [
                ["NORMAL"],
                ["readme.txt", "img1.jpg", "data.csv"],
            ]
            from services.trainer_engine import build_dataframe
            df = build_dataframe("/fake/dataset")
            assert len(df) == 1


class TestBuildCnnModel:
    def test_returns_model_object(self):
        with patch("services.trainer_engine.tf.keras.applications") as mock_apps, \
             patch("services.trainer_engine.Adam") as mock_adam, \
             patch("services.trainer_engine.layers") as mock_layers, \
             patch("services.trainer_engine.models") as mock_models:
            mock_apps.DenseNet121.return_value = MagicMock()
            mock_apps.DenseNet121.return_value.output = MagicMock()
            mock_apps.DenseNet121.return_value.input = MagicMock()
            mock_models.Model.return_value = MagicMock()
            from services.trainer_engine import build_cnn_model
            model = build_cnn_model("DenseNet121", (224, 224))
            assert model is not None
            mock_models.Model.assert_called_once()

    def test_fallback_on_invalid_architecture(self):
        with patch("services.trainer_engine.tf.keras.applications") as mock_apps, \
             patch("services.trainer_engine.MobileNetV2") as mock_mobilenet, \
             patch("services.trainer_engine.Adam") as mock_adam, \
             patch("services.trainer_engine.layers") as mock_layers, \
             patch("services.trainer_engine.models") as mock_models:
            mock_apps.DenseNet121.side_effect = AttributeError("not found")
            mock_mobilenet.return_value = MagicMock()
            mock_mobilenet.return_value.output = MagicMock()
            mock_mobilenet.return_value.input = MagicMock()
            mock_models.Model.return_value = MagicMock()
            from services.trainer_engine import build_cnn_model
            model = build_cnn_model("InvalidModel", (224, 224))
            assert model is not None
            mock_mobilenet.assert_called()


class TestDbProgressCallback:
    @patch("services.trainer_engine.get_db_connection")
    def test_on_epoch_end_updates_db(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.cursor.return_value = mock_cursor
        from services.trainer_engine import DBProgressCallback
        cb = DBProgressCallback(job_id=1, total_epochs=10)
        cb.on_epoch_end(0, {"loss": 0.5, "accuracy": 0.8, "val_loss": 0.4, "val_accuracy": 0.85})
        assert len(cb.metrics_history) == 1
        assert cb.current_epoch_global == 1
        mock_cursor.execute.assert_called_once()

    @patch("services.trainer_engine.get_db_connection")
    def test_progress_calculation(self, mock_db):
        from services.trainer_engine import DBProgressCallback
        cb = DBProgressCallback(job_id=1, total_epochs=10)
        cb.on_epoch_end(0, {"loss": 0.5, "accuracy": 0.8, "val_loss": 0.4, "val_accuracy": 0.85})
        cb.on_epoch_end(1, {"loss": 0.3, "accuracy": 0.9, "val_loss": 0.2, "val_accuracy": 0.92})
        assert cb.current_epoch_global == 2
        assert len(cb.metrics_history) == 2


class TestCreateTfDatasets:
    def test_returns_two_datasets(self):
        with patch("services.trainer_engine.tf") as mock_tf:
            mock_ds = MagicMock()
            mock_ds.map.return_value = mock_ds
            mock_ds.shuffle.return_value = mock_ds
            mock_ds.batch.return_value = mock_ds
            mock_ds.prefetch.return_value = mock_ds
            mock_tf.data.Dataset.from_tensor_slices.return_value = mock_ds
            import numpy as np

            from services.trainer_engine import create_tf_datasets_from_indices
            train_ds, val_ds = create_tf_datasets_from_indices(
                np.array(["a.jpg", "b.jpg", "c.jpg"]),
                np.array([0, 1, 0]),
                np.array([0, 1]), np.array([2]),
                (224, 224), 2
            )
            assert train_ds is not None
            assert val_ds is not None
            assert mock_tf.data.Dataset.from_tensor_slices.call_count == 2


class TestRunTrainingJobSync:
    @patch("services.trainer_engine.get_db_connection")
    def test_sets_failed_status_on_missing_dataset(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.cursor.return_value = mock_cursor
        with patch("os.path.exists", return_value=False):
            from services.trainer_engine import run_training_job_sync
            run_training_job_sync(1, "/fake/path", "DenseNet121")
            update_calls = [c for c in mock_cursor.execute.call_args_list
                            if "Failed" in str(c)]
            assert len(update_calls) >= 1

    @patch("services.trainer_engine.get_db_connection")
    def test_sets_failed_status_on_empty_dataset(self, mock_db):
        mock_cursor = MagicMock()
        mock_db.return_value.cursor.return_value = mock_cursor
        mock_df = MagicMock()
        mock_df.__len__.return_value = 0
        with patch("os.path.exists", return_value=True), \
             patch("services.trainer_engine.build_dataframe", return_value=mock_df):
            from services.trainer_engine import run_training_job_sync
            run_training_job_sync(1, "/fake/path", "DenseNet121")
            update_calls = [c for c in mock_cursor.execute.call_args_list
                            if "Failed" in str(c)]
            assert len(update_calls) >= 1
