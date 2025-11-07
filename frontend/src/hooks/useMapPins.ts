import { useEffect, useState } from "react";
import { fetchMapPins } from "../utils/api";

interface MapPin {
  name: string;
  category: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  description?: string;
  rating?: number;
}

export function useMapPins(destination?: string) {
  const [pins, setPins] = useState<MapPin[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!destination) {
      setPins([]);
      return;
    }

    let isCancelled = false;
    setIsLoading(true);
    setError(null);

    fetchMapPins({ destination })
      .then((response) => {
        if (!isCancelled) {
          setPins(response.data.pins ?? []);
        }
      })
      .catch((caughtError) => {
        if (!isCancelled) {
          const errorMessage =
            caughtError instanceof Error
              ? caughtError.message
              : "Unable to fetch map data";
          setError(errorMessage);
        }
      })
      .finally(() => {
        if (!isCancelled) {
          setIsLoading(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [destination]);

  return { pins, isLoading, error };
}
