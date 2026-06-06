function Sidebar({
  reserves,
  selectedReserveId,
  onSelectReserve,
  isOpen,
  onClose,
}) {
  function handleSelectReserve(reserveId) {
    onSelectReserve(reserveId);
    onClose();
  }

  return (
    <>
      <div
        className={isOpen ? "sidebar-overlay show" : "sidebar-overlay"}
        onClick={onClose}
      />

      <aside className={isOpen ? "sidebar open" : "sidebar"}>
        <div className="sidebar-header">
          <div>
            <h2>BioSentinel</h2>
            <span>Environmental Monitor</span>
          </div>

          <button className="sidebar-close-button" onClick={onClose}>
            ×
          </button>
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
              onClick={() => handleSelectReserve(reserve.id)}
            >
              <strong>{reserve.name}</strong>
              <small>
                {reserve.city} - {reserve.state}
              </small>
            </button>
          ))}
        </nav>
      </aside>
    </>
  );
}

export default Sidebar;