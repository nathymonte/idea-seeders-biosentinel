import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Link } from "react-router-dom";

import api from "../api/api";
import Sidebar from "../components/Sidebar";
import SummaryCard from "../components/SummaryCard";
import StatusBadge from "../components/StatusBadge";

const RESERVE_COORDINATES = {
  1: [-23.595, -46.695],
  2: [-2.04, -60.34],
  3: [-18.99, -57.64],
};

function MapPage() {
  const [reserves, setReserves] = useState([]);
  const [selectedReserveId, setSelectedReserveId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

  useEffect(() => {
    async function loadReserves() {
      const response = await api.get("/reserves");
      setReserves(response.data);

      if (response.data.length > 0) {
        setSelectedReserveId(response.data[0].id);
      }
    }

    loadReserves();
  }, []);

  useEffect(() => {
    async function loadSummary() {
      if (!selectedReserveId) return;

      setLoadingSummary(true);

      try {
        const response = await api.get(`/reserves/${selectedReserveId}/summary`);
        setSummary(response.data);
      } catch (error) {
        setSummary(null);
      } finally {
        setLoadingSummary(false);
      }
    }

    loadSummary();
  }, [selectedReserveId]);

  const selectedCoordinates =
    RESERVE_COORDINATES[selectedReserveId] || [-14.235, -51.925];

  return (
    <div className="dashboard-layout">
      <Sidebar
        reserves={reserves}
        selectedReserveId={selectedReserveId}
        onSelectReserve={setSelectedReserveId}
      />

      <main className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <h1>Monitoramento Ambiental</h1>
            <p>Visualização das reservas analisadas por dados do MapBiomas.</p>
          </div>

          {summary && <StatusBadge status={summary.environmental_status} />}
        </header>

        <section className="map-section">
          <MapContainer
            center={selectedCoordinates}
            zoom={11}
            scrollWheelZoom={true}
            className="map-container"
          >
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {reserves.map((reserve) => {
              const position =
                RESERVE_COORDINATES[reserve.id] || [-14.235, -51.925];

              return (
                <Marker key={reserve.id} position={position}>
                  <Popup>
                    <strong>{reserve.name}</strong>
                    <br />
                    {reserve.city} - {reserve.state}
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </section>

        <section className="summary-grid">
          {loadingSummary && <p>Carregando resumo...</p>}

          {!loadingSummary && summary && (
            <>
              <SummaryCard
                title="Classe dominante"
                value={summary.dominant_class}
                subtitle={`${summary.dominant_percentage}% da área analisada`}
              />

              <SummaryCard
                title="Vegetação nativa"
                value={`${summary.native_vegetation_percentage}%`}
                subtitle="Cobertura preservada"
              />

              <SummaryCard
                title="Uso humano"
                value={`${summary.human_use_percentage}%`}
                subtitle="Urbano, agropecuária ou área não vegetada"
              />

              <SummaryCard
                title="Área analisada"
                value={`${summary.total_analyzed_area_hectares} ha`}
                subtitle={`${summary.number_of_detected_classes} classes detectadas`}
              />
            </>
          )}
        </section>

        {selectedReserveId && (
          <Link className="report-link" to={`/report/${selectedReserveId}`}>
            Ver relatório detalhado
          </Link>
        )}
      </main>
    </div>
  );
}

export default MapPage;
