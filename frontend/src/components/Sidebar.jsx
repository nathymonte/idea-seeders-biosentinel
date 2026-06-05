function Sidebar({ reserves, selectedReserveId, onSelectReserve }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>BioSentinel</h2>
        <span>Environmental Monitor</span>
      </div>

      <nav className="reserve-list">
        <h3>Reservas</h3>

        {reserves.map((reserve) => (
          <button
            key={reserve.id}
            className={
              reserve.id === selectedReserveId
                ? "reserve-item active"
                : "reserve-item"
            }
            onClick={() => onSelectReserve(reserve.id)}
          >
            <strong>{reserve.name}</strong>
            <small>
              {reserve.city} - {reserve.state}
            </small>
          </button>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;