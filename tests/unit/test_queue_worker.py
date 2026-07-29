from unittest.mock import MagicMock, patch


class TestGetPayload:
    def test_parses_string_payload(self):
        from services.queue_worker import _get_payload
        job = {"payload": '{"model_name": "DenseNet121"}'}
        result = _get_payload(job)
        assert result["model_name"] == "DenseNet121"

    def test_passes_through_dict_payload(self):
        from services.queue_worker import _get_payload
        job = {"payload": {"model_name": "DenseNet121"}}
        result = _get_payload(job)
        assert result["model_name"] == "DenseNet121"


class TestResetRunningJobs:
    def test_resets_running_to_queued(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _reset_running_jobs
            _reset_running_jobs()
            sql = mock_cursor.execute.call_args[0][0]
            assert "UPDATE job_queue" in sql
            assert "status = 'running'" in sql


class TestClaimJob:
    def test_claims_queued_job(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 1
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _claim_job
            result = _claim_job(1)
            assert result is True

    def test_fails_if_already_taken(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.rowcount = 0
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _claim_job
            result = _claim_job(1)
            assert result is False


class TestFailJob:
    def test_updates_status_to_failed(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _fail_job
            _fail_job(1, "error occurred")
            sql = mock_cursor.execute.call_args[0][0]
            assert "status = 'failed'" in sql


class TestFinishJob:
    def test_updates_status_to_completed_with_result(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _finish_job
            _finish_job(1, {"label": "Neumonía"})
            sql = mock_cursor.execute.call_args[0][0]
            assert "status = 'completed'" in sql


class TestExecuteJob:
    def test_raises_on_unknown_type(self):
        with patch("services.queue_worker.get_db_connection"):
            import pytest

            from services.queue_worker import _execute_job
            with pytest.raises(ValueError, match="Unknown job type"):
                _execute_job({"job_type": "unknown", "payload": "{}"})


class TestNextJob:
    def test_returns_none_when_empty(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = None
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _next_job
            result = _next_job()
            assert result is None

    def test_returns_next_queued_job(self):
        with patch("services.queue_worker.get_db_connection") as mock_db:
            mock_cursor = MagicMock()
            mock_cursor.fetchone.return_value = {"id": 1, "job_type": "diagnosis", "payload": "{}"}
            mock_db.return_value.cursor.return_value = mock_cursor
            from services.queue_worker import _next_job
            result = _next_job()
            assert result is not None
            assert result["job_type"] == "diagnosis"
