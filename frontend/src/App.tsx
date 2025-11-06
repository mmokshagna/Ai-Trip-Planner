import { useEffect, useMemo, useState } from "react";
import { TripPlannerLayout } from "./components/TripPlannerLayout";
import { PlannerContextProvider } from "./context/PlannerContext";

const personas = [
  "Luxury Relaxation",
  "Backpacker Adventure",
  "Family-Friendly",
  "Romantic Getaway"
];

export default function App() {
  const [selectedPersona, setSelectedPersona] = useState(personas[0]);

  const personaOptions = useMemo(
    () => personas.map((persona) => ({ label: persona, value: persona })),
    []
  );

  useEffect(() => {
    document.title = "AI Trip Planner";
  }, []);

  return (
    <PlannerContextProvider initialPersona={selectedPersona}>
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <header className="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <div>
              <h1 className="text-2xl font-semibold text-brand">AI Trip Planner</h1>
              <p className="text-sm text-slate-400">
                Weather-aware, event-driven itineraries tailored by GPT.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <label htmlFor="persona" className="text-sm text-slate-300">
                Travel persona
              </label>
              <select
                id="persona"
                className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-sm"
                value={selectedPersona}
                onChange={(event) => setSelectedPersona(event.target.value)}
              >
                {personaOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </header>
        <TripPlannerLayout persona={selectedPersona} />
      </div>
    </PlannerContextProvider>
  );
}
