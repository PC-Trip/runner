import pytest


@pytest.mark.parametrize("run", ["sequence.json"], indirect=True)
def test_sequence(run):
    assert run == 0


@pytest.mark.parametrize("run", ["thread.json"], indirect=True)
def test_thread(run):
    assert run == 0


@pytest.mark.parametrize("run", ["process.json"], indirect=True)
def test_process(run):
    assert run == 0


@pytest.mark.parametrize("run", ["thread_jobs.json"], indirect=True)
def test_thread_jobs(run):
    assert run == 0


@pytest.mark.parametrize("run", ["thread_jobs_broadcast.json"], indirect=True)
def test_thread_jobs_broadcast(run):
    assert run == 0


@pytest.mark.parametrize("run", ["thread_jobs_workers.json"], indirect=True)
def test_thread_jobs_workers(run):
    assert run == 0


@pytest.mark.parametrize("run", ["thread_jobs_broadcast_workers.json"], indirect=True)
def test_thread_jobs_broadcast_workers(run):
    assert run == 0


@pytest.mark.parametrize("run", ["process_jobs.json"], indirect=True)
def test_process_jobs(run):
    assert run == 0


@pytest.mark.parametrize("run", ["process_jobs_broadcast.json"], indirect=True)
def test_process_jobs_broadcast(run):
    assert run == 0


@pytest.mark.parametrize("run", ["process_jobs_workers.json"], indirect=True)
def test_process_jobs_workers(run):
    assert run == 0


@pytest.mark.parametrize("run", ["process_jobs_broadcast_workers.json"], indirect=True)
def test_process_jobs_broadcast_workers(run):
    assert run == 0


@pytest.mark.parametrize("run", ["action.json"], indirect=True)
def test_action(run):
    assert run == 0
