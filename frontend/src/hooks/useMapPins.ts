import { useEffect, useState } from "react";

interface MapPin {
  name: string;
  category: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  description?: string;
}

export function useMapPins(destination?: string) {
  const [pins, setPins] = useState<MapPin[]>([]);

  useEffect(() => {
    if (!destination) {
      setPins([]);
      return;
    }

    // Replace with call to GET /api/map once backend is wired up.
    setPins([
      {
        name: "Central Plaza",
        category: "Explore",
        coordinates: { lat: 41.3874, lng: 2.1686 },
        description: "Historic city square with popular landmarks."
      }
    ]);
  }, [destination]);

  return { pins };
}
