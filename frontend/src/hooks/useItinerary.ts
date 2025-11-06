import { useCallback, useState } from "react";

interface ItineraryActivity {
  name: string;
  description: string;
  category: string;
  weather_advice?: string | null;
}

interface ItineraryDay {
  date: string;
  theme?: string | null;
  activities: ItineraryActivity[];
}

export interface ItineraryResponse {
  destination: string;
  start_date: string;
  end_date: string;
  persona: string;
  summary: string;
  daily_plans: ItineraryDay[];
}

export function useItinerary() {
  const [itinerary, setItinerary] = useState<ItineraryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const regenerateItinerary = useCallback(async (params: Record<string, unknown>) => {
    setIsLoading(true);
    try {
      const persona = String(params["persona"] ?? "Luxury Relaxation");
      // Replace with real API call to POST /api/plan-trip or /api/customize-trip
      setItinerary({
        destination: "Barcelona",
        start_date: "2024-07-01",
        end_date: "2024-07-07",
        persona,
        summary: "Sample itinerary response from backend stub.",
        daily_plans: []
      });
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    itinerary,
    isLoading,
    regenerateItinerary
  };
}
