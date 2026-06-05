from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint_should_return_api_status():
    """
    Cenário:
        Verificar se a API está online.

    Entrada:
        GET /

    Saída esperada:
        Mensagem padrão da aplicação.

    Status esperado:
        200 OK
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "BioSentinel API running"
    }


def test_list_reserves_should_return_success_status():
    """
    Cenário:
        Listar reservas ambientais cadastradas.

    Entrada:
        GET /reserves

    Saída esperada:
        Lista de reservas em formato JSON.

    Status esperado:
        200 OK
    """
    response = client.get("/reserves")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_datasets_should_return_success_status():
    """
    Cenário:
        Listar datasets de satélite cadastrados.

    Entrada:
        GET /datasets

    Saída esperada:
        Lista de datasets em formato JSON.

    Status esperado:
        200 OK
    """
    response = client.get("/datasets")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_reserve_analysis_should_return_analysis_data():
    """
    Cenário:
        Consultar análise de cobertura do solo de uma reserva existente.

    Entrada:
        GET /reserves/1/analysis

    Saída esperada:
        Lista com classes de cobertura, área em hectares e percentual.

    Status esperado:
        200 OK
    """
    response = client.get("/reserves/1/analysis")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if data:
        first_item = data[0]

        assert "class_code" in first_item
        assert "class_name" in first_item
        assert "area_hectares" in first_item
        assert "percentage" in first_item


def test_get_reserve_summary_should_return_environmental_summary():
    """
    Cenário:
        Consultar resumo ambiental de uma reserva existente.

    Entrada:
        GET /reserves/1/summary

    Saída esperada:
        Objeto JSON com classe dominante, grupos ambientais e status ambiental.

    Status esperado:
        200 OK
    """
    response = client.get("/reserves/1/summary")

    assert response.status_code == 200

    data = response.json()

    assert "reserve_id" in data
    assert "reserve_name" in data
    assert "dominant_class" in data
    assert "groups" in data
    assert "environmental_status" in data


def test_update_non_existing_reserve_should_return_not_found():
    """
    Cenário:
        Tentar atualizar uma reserva inexistente.

    Entrada:
        PUT /reserves/999999
        Body: {"name": "Reserva Inexistente"}

    Saída esperada:
        Mensagem de erro informando que a reserva não foi encontrada.

    Status esperado:
        404 Not Found
    """
    response = client.put(
        "/reserves/999999",
        json={
            "name": "Reserva Inexistente"
        }
    )

    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_non_existing_dataset_should_return_not_found():
    """
    Cenário:
        Tentar deletar um dataset inexistente.

    Entrada:
        DELETE /datasets/999999

    Saída esperada:
        Mensagem de erro informando que o dataset não foi encontrado.

    Status esperado:
        404 Not Found
    """
    response = client.delete("/datasets/999999")

    assert response.status_code == 404
    assert "detail" in response.json()