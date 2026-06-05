function StatusBadge({ status }) {
  const statusClass = status ? status.toLowerCase() : "unknown";

  return (
    <span className={`status-badge ${statusClass}`}>
      {status || "UNKNOWN"}
    </span>
  );
}

export default StatusBadge;