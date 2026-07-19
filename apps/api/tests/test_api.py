import io

HUMAN_TEXT = (
    "I walked to the corner shop this morning because we ran out of coffee, "
    "and the man behind the counter told me a long story about his brother's "
    "boat, which apparently sank twice. " * 3
)
AI_TEXT = (
    "The robot revolution in productivity tools has transformed the way we "
    "approach everyday tasks, offering streamlined workflows and enhanced "
    "efficiency across a wide range of industries and applications. " * 3
)


def test_health(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scan_human_text(client):
    response = client.post("/v1/scan", json={"text": HUMAN_TEXT})
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "human"
    assert body["ai_probability"] < 0.1
    assert body["scan_id"]
    assert body["sentences"]


def test_scan_ai_text_and_retrieve(client):
    response = client.post("/v1/scan", json={"text": AI_TEXT, "mode": "deep"})
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "ai"
    assert body["mode_used"] == "deep"

    fetched = client.get(f"/v1/scan/{body['scan_id']}")
    assert fetched.status_code == 200
    assert fetched.json()["verdict"] == "ai"


def test_scan_too_short(client):
    response = client.post("/v1/scan", json={"text": "Short text."})
    assert response.status_code == 200
    assert response.json()["verdict"] == "too_short"
    assert response.json()["warning"]


def test_scan_missing_text_rejected(client):
    assert client.post("/v1/scan", json={}).status_code == 422


def test_scan_file_txt(client):
    response = client.post(
        "/v1/scan/file",
        files={"file": ("essay.txt", io.BytesIO(HUMAN_TEXT.encode()), "text/plain")},
    )
    assert response.status_code == 200
    assert response.json()["verdict"] == "human"


def test_scan_file_unsupported_type(client):
    response = client.post(
        "/v1/scan/file",
        files={"file": ("evil.exe", io.BytesIO(b"MZ"), "application/x-msdownload")},
    )
    assert response.status_code == 415


def test_batch_scan(client):
    response = client.post(
        "/v1/scan/batch",
        json={"items": [{"text": HUMAN_TEXT}, {"text": AI_TEXT}]},
    )
    assert response.status_code == 200
    verdicts = [r["verdict"] for r in response.json()["results"]]
    assert verdicts == ["human", "ai"]


def test_get_unknown_scan_404(client):
    assert client.get("/v1/scan/doesnotexist").status_code == 404


def test_history_and_usage(client):
    history = client.get("/v1/history")
    assert history.status_code == 200
    assert len(history.json()) >= 1

    usage = client.get("/v1/usage")
    assert usage.status_code == 200
    assert usage.json()["used"] >= 1


def test_api_key_lifecycle(client):
    denied = client.post("/v1/keys", json={"name": "ci"})
    assert denied.status_code == 401

    created = client.post(
        "/v1/keys",
        json={"name": "ci"},
        headers={"Authorization": "Bearer test-admin-token"},
    )
    assert created.status_code == 200
    raw_key = created.json()["api_key"]
    assert raw_key.startswith("vk_")

    scan = client.post(
        "/v1/scan", json={"text": HUMAN_TEXT}, headers={"X-API-Key": raw_key}
    )
    assert scan.status_code == 200

    bad = client.post(
        "/v1/scan", json={"text": HUMAN_TEXT}, headers={"X-API-Key": "vk_wrong"}
    )
    assert bad.status_code == 401

    revoked = client.delete(
        f"/v1/keys/{created.json()['key_id']}",
        headers={"Authorization": "Bearer test-admin-token"},
    )
    assert revoked.status_code == 200


def test_anonymous_daily_quota_enforced(client):
    # Limit is 10/day for anonymous; earlier tests consumed some quota.
    last_status = None
    for _ in range(12):
        last_status = client.post("/v1/scan", json={"text": HUMAN_TEXT}).status_code
    assert last_status == 429
