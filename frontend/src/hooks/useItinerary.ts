import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { customizeTrip, planTrip } from "../utils/api";

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

interface RegenerateParams {
  persona?: string;
  destination?: string;
  start_date?: string;
  end_date?: string;
  feedback?: string;
  forceNew?: boolean;
}

function formatDate(date: Date) {
  return date.toISOString().slice(0, 10);
}

function defaultTripDetails(persona: string) {
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 14);
  const end = new Date(start);
  end.setDate(start.getDate() + 4);

  return {
    destination: "Barcelona, Spain",
    start_date: formatDate(start),
    end_date: formatDate(end),
    persona,
  };
}

export function useItinerary(persona: string) {
  const [itinerary, setItinerary] = useState<ItineraryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const defaults = useMemo(() => defaultTripDetails(persona), [persona]);
  const itineraryRef = useRef<ItineraryResponse | null>(null);
  const initializedPersonaRef = useRef<string | null>(null);

  useEffect(() => {
    itineraryRef.current = itinerary;
  }, [itinerary]);

  const regenerateItinerary = useCallback(
    async (params: RegenerateParams = {}) => {
      setIsLoading(true);
      setError(null);
      const current = itineraryRef.current;
      try {
        const personaOverride = String(
          params.persona ?? current?.persona ?? defaults.persona
        );
        const destination = String(
          params.destination ?? current?.destination ?? defaults.destination
        );
        const start_date = String(
          params.start_date ?? current?.start_date ?? defaults.start_date
        );
        const end_date = String(
          params.end_date ?? current?.end_date ?? defaults.end_date
        );

        const shouldPlanNew = params.forceNew || !current;

        if (shouldPlanNew) {
          const response = await planTrip({
            destination,
            start_date,
            end_date,
            persona: personaOverride,
          });
          setItinerary(response.data);
          itineraryRef.current = response.data;
          return response.data;
        }

        const response = await customizeTrip({
          feedback:
            params.feedback ??
            `Adjust the plan to emphasise a ${personaOverride.toLowerCase()} vibe.`,
          itinerary: {
            ...current,
            persona: personaOverride,
          },
        });
        setItinerary(response.data);
        itineraryRef.current = response.data;
        return response.data;
      } catch (caughtError) {
        const errorMessage =
          caughtError instanceof Error
            ? caughtError.message
            : "Unable to update itinerary";
        setError(errorMessage);
        throw caughtError;
      } finally {
        setIsLoading(false);
      }
    },
    [defaults]
  );

  useEffect(() => {
    if (initializedPersonaRef.current === defaults.persona) {
      return;
    }
    initializedPersonaRef.current = defaults.persona;
    regenerateItinerary({ persona: defaults.persona, forceNew: true }).catch(() => {
      /* handled via error state */
    });
  }, [defaults.persona, regenerateItinerary]);

  return {
    itinerary,
    isLoading,
    error,
    regenerateItinerary,
  };
}
