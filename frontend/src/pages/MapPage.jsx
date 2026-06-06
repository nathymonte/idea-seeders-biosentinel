import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polygon } from "react-leaflet";
import { Link } from "react-router-dom";

import api from "../api/api";
import Sidebar from "../components/Sidebar";
import SummaryCard from "../components/SummaryCard";
import StatusBadge from "../components/StatusBadge";
import RecenterMap from "../components/RecenterMap";

function MapPage() {
  const [reserves, setReserves] = useState([]);
  const [selectedReserveId, setSelectedReserveId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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

  const selectedReserve = reserves.find(
    (reserve) => reserve.id === selectedReserveId
  );

  const selectedCoordinates =
    getPolygonCenter(selectedReserve?.boundary) || [-14.235, -51.925];

  function geoJsonPolygonToLeafletPositions(boundary) {
  if (!boundary || boundary.type !== "Polygon") return [];

  return boundary.coordinates[0].map(([lng, lat]) => [lat, lng]);
  }

    function getPolygonCenter(boundary) {
      if (!boundary || boundary.type !== "Polygon") return null;

      const coordinates = boundary.coordinates[0];

      const total = coordinates.reduce(
        (acc, [lng, lat]) => {
          acc.lat += lat;
          acc.lng += lng;
          return acc;
        },
        { lat: 0, lng: 0 }
      );

      return [
        total.lat / coordinates.length,
        total.lng / coordinates.length,
      ];
  }

  return (
    <div className="dashboard-layout">
      <Sidebar
        reserves={reserves}
        selectedReserveId={selectedReserveId}
        onSelectReserve={setSelectedReserveId}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <main className="dashboard-main">
        <button
          className="mobile-menu-button"
          onClick={() => setIsSidebarOpen(true)}
        >
          ☰ Reservas
        </button>
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
            <RecenterMap center={selectedCoordinates} />
            <TileLayer
              attribution='&copy; OpenStreetMap contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {reserves.map((reserve) => {
              const polygonPositions = geoJsonPolygonToLeafletPositions(reserve.boundary);

              if (!polygonPositions.length) return null;

              return (
                <Polygon
                  key={`polygon-${reserve.id}`}
                  positions={polygonPositions}
                  pathOptions={{
                    color: reserve.id === selectedReserveId ? "#1b4332" : "#2d6a4f",
                    fillColor: reserve.id === selectedReserveId ? "#95d5b2" : "#b7e4c7",
                    fillOpacity: reserve.id === selectedReserveId ? 0.45 : 0.2,
                    weight: reserve.id === selectedReserveId ? 3 : 1,
                  }}
                  eventHandlers={{
                    click: () => setSelectedReserveId(reserve.id),
                  }}
                >
                  <Popup>
                    <strong>{reserve.name}</strong>
                    <br />
                    {reserve.city} - {reserve.state}
                  </Popup>
                </Polygon>
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
