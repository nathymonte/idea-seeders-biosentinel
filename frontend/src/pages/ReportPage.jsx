import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
} from "recharts";

import api from "../api/api";
import StatusBadge from "../components/StatusBadge";
import SummaryCard from "../components/SummaryCard";

const COLORS = [
  "#2D6A4F",
  "#95D5B2",
  "#1D3557",
  "#E9C46A",
  "#A8DADC",
  "#6B7280",
  "#D62828",
];

function ReportPage() {
  const { reserveId } = useParams();

  const [summary, setSummary] = useState(null);
  const [analysis, setAnalysis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const groupChartData = useMemo(() => {
    if (!summary?.groups) return [];

    return Object.values(summary.groups).map((group) => ({
      name: group.label,
      value: group.percentage,
      area: group.area_hectares,
    }));
  }, [summary]);

  const analysisChartData = useMemo(() => {
    return analysis.map((item) => ({
      name: item.class_name,
      percentage: item.percentage,
      area: item.area_hectares,
    }));
  }, [analysis]);

  useEffect(() => {
    async function loadReport() {
      try {
        setLoading(true);
        setError("");

        const [summaryResponse, analysisResponse] = await Promise.all([
          api.get(`/reserves/${reserveId}/summary`),
          api.get(`/reserves/${reserveId}/analysis`),
        ]);

        setSummary(summaryResponse.data);
        setAnalysis(analysisResponse.data);
      } catch (error) {
        setError("Não foi possível carregar o relatório da reserva.");
      } finally {
        setLoading(false);
      }
    }

    loadReport();
  }, [reserveId]);

  function getDiagnosisText() {
    if (!summary) return "";

    if (summary.environmental_status === "CRITICAL") {
      return "A reserva apresenta forte predominância de uso humano ou baixa presença de vegetação nativa. Recomenda-se priorizar o monitoramento desta área e investigar possíveis pressões ambientais.";
    }

    if (summary.environmental_status === "WARNING") {
      return "A reserva apresenta sinais de atenção, com cobertura nativa reduzida ou presença relevante de uso antrópico. Recomenda-se acompanhamento periódico.";
    }

    return "A reserva apresenta bom nível de preservação ambiental, com predominância de cobertura nativa ou baixa pressão antrópica detectada.";
  }

  if (loading) {
    return (
      <main className="report-page">
        <p>Carregando relatório...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="report-page">
        <p className="error-message">{error}</p>
        <Link className="report-link" to="/map">
          Voltar para o mapa
        </Link>
      </main>
    );
  }

  return (
    <main className="report-page">
      <header className="report-header">
        <div>
          <Link className="back-link" to="/map">
            ← Voltar para o mapa
          </Link>

          <h1>Relatório Ambiental</h1>
          <p>{summary.reserve_name}</p>
        </div>

        <StatusBadge status={summary.environmental_status} />
      </header>

      <section className="summary-grid report-summary-grid">
        <SummaryCard
          title="Área analisada"
          value={`${summary.total_analyzed_area_hectares} ha`}
          subtitle="Área total processada pelo MapBiomas"
        />

        <SummaryCard
          title="Classe dominante"
          value={summary.dominant_class}
          subtitle={`${summary.dominant_percentage}% da área`}
        />

        <SummaryCard
          title="Vegetação nativa"
          value={`${summary.native_vegetation_percentage}%`}
          subtitle="Indicador de preservação"
        />

        <SummaryCard
          title="Uso humano"
          value={`${summary.human_use_percentage}%`}
          subtitle="Urbano, agropecuária ou área não vegetada"
        />
      </section>

      <section className="report-content-grid">
        <article className="report-panel">
          <h2>Distribuição por grupo ambiental</h2>
          <p>
            Consolidação das classes do MapBiomas em categorias de leitura
            ambiental.
          </p>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={groupChartData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={95}
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {groupChartData.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip
                  formatter={(value, name, props) => [
                    `${value}% | ${props.payload.area} ha`,
                    name,
                  ]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </article>

        <article className="report-panel">
          <h2>Classes detectadas</h2>
          <p>
            Percentual de cobertura identificado em cada classe do raster
            analisado.
          </p>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={analysisChartData}>
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 10 }}
                  interval={0}
                  angle={-20}
                  textAnchor="end"
                  height={80}
                />
                <YAxis />
                <Tooltip
                  formatter={(value) => [`${value}%`, "Percentual"]}
                />
                <Bar dataKey="percentage" fill="#2D6A4F" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </article>
      </section>

      <section className="report-content-grid">
        <article className="report-panel">
          <h2>Diagnóstico automático</h2>
          <p className="diagnosis-text">{getDiagnosisText()}</p>
        </article>

        <article className="report-panel">
          <h2>Tabela de cobertura do solo</h2>

          <table className="analysis-table">
            <thead>
              <tr>
                <th>Classe</th>
                <th>Área</th>
                <th>Percentual</th>
              </tr>
            </thead>

            <tbody>
              {analysis.map((item) => (
                <tr key={item.class_code}>
                  <td>
                    <strong>{item.class_name}</strong>
                    <span>Código {item.class_code}</span>
                  </td>
                  <td>{item.area_hectares} ha</td>
                  <td>{item.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>
      </section>
    </main>
  );
}

export default ReportPage;
