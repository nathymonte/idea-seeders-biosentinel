import { useMap } from "react-leaflet";
import { useEffect } from "react";
import SummaryCard from "./SummaryCard.jsx";

function RecenterMap({ center }) {
  const map = useMap();

  useEffect(() => {
    if (center) {
      map.setView(center, 11);
    }
  }, [center, map]);

  return null;
}

export default RecenterMap;