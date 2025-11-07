import { useEffect } from "react";
import { CollaborationPanel } from "./CollaborationPanel";
import { usePlannerContext } from "../context/PlannerContext";
import { useItinerary } from "../hooks/useItinerary";
import { useMapPins } from "../hooks/useMapPins";
import { useChat } from "../hooks/useChat";

interface TripPlannerLayoutProps {
  persona: string;
}

export function TripPlannerLayout({ persona }: TripPlannerLayoutProps) {
  const {
    itinerary,
    isLoading: itineraryLoading,
    error: itineraryError,
    regenerateItinerary,
  } = useItinerary(persona);
  const { pins, isLoading: pinsLoading, error: mapError } = useMapPins(itinerary?.destination);
  const { messages, sendMessage, isSending: chatSending, error: chatError } = useChat(
    itinerary,
    persona
  );
  const { updatePersona } = usePlannerContext();

  useEffect(() => {
    updatePersona(persona);
  }, [persona, updatePersona]);

  return (
    <div className="mx-auto grid max-w-6xl grid-cols-1 gap-6 px-6 py-8 lg:grid-cols-[2fr_1fr]">
      <section className="space-y-4">
        <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-white">Itinerary Overview</h2>
            <p className="text-sm text-slate-400">
              {itineraryLoading
                ? "Generating itinerary using GPT..."
                : itinerary?.summary ?? "Provide trip details to begin planning."}
            </p>
            {itineraryError ? (
              <p className="text-xs text-red-400">{itineraryError}</p>
            ) : null}
          </div>
          <button
            className="self-start rounded-md bg-brand px-4 py-2 text-sm font-semibold text-slate-900"
            disabled={itineraryLoading}
            onClick={() => {
              updatePersona(persona);
              regenerateItinerary({ persona });
            }}
          >
            Regenerate
          </button>
        </header>
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <h3 className="text-lg font-medium text-white">Daily Plans</h3>
          <ol className="mt-3 space-y-3 text-sm text-slate-300">
            {itineraryLoading ? (
              <li className="rounded-md border border-dashed border-slate-800 p-3 text-slate-400">
                Planning your trip with current events and weather...
              </li>
            ) : null}
            {!itineraryLoading && (itinerary?.daily_plans ?? []).length === 0 ? (
              <li className="rounded-md border border-dashed border-slate-800 p-3 text-slate-400">
                Daily plans will appear once the trip is generated.
              </li>
            ) : null}
            {(itinerary?.daily_plans ?? []).map((day) => (
              <li key={day.date} className="rounded-md border border-slate-800 p-3">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-brand-light">{day.date}</span>
                  <span className="text-xs uppercase tracking-wide text-slate-400">
                    {day.theme}
                  </span>
                </div>
                <ul className="mt-2 space-y-2">
                  {day.activities.map((activity) => (
                    <li key={`${day.date}-${activity.name}`} className="rounded bg-slate-900/60 p-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-medium text-white">{activity.name}</p>
                          <p className="text-xs text-slate-400">{activity.description}</p>
                        </div>
                        <span className="rounded bg-brand/20 px-2 py-1 text-xs text-brand">
                          {activity.category}
                        </span>
                      </div>
                      {activity.weather_advice ? (
                        <p className="mt-1 text-xs text-slate-400">
                          Weather tip: {activity.weather_advice}
                        </p>
                      ) : null}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ol>
        </div>
      </section>
      <aside className="space-y-4">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <h3 className="text-lg font-medium text-white">Map Preview</h3>
          <div className="text-sm text-slate-400">
            {pinsLoading ? "Fetching nearby highlights..." : null}
            {!pinsLoading && pins.length === 0 ? (
              <p>Map data will appear here after fetching locations.</p>
            ) : null}
            {mapError ? <p className="text-xs text-red-400">{mapError}</p> : null}
            {pins.length > 0 ? (
              <ul className="mt-3 space-y-2 text-xs text-slate-300">
                {pins.slice(0, 5).map((pin) => (
                  <li key={`${pin.name}-${pin.category}`} className="rounded bg-slate-900/60 p-2">
                    <p className="font-medium text-white">{pin.name}</p>
                    <p className="text-slate-400">{pin.category}</p>
                    {pin.description ? (
                      <p className="text-slate-500">{pin.description}</p>
                    ) : null}
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          <h3 className="text-lg font-medium text-white">Travel Companion</h3>
          <div className="space-y-2 text-sm text-slate-300">
            {messages.length === 0 ? (
              <p className="rounded border border-dashed border-slate-800 p-3 text-slate-400">
                Chat with your AI travel companion to get dining suggestions, local tips,
                and itinerary updates.
              </p>
            ) : null}
            {messages.map((message) => (
              <div key={message.id} className="rounded bg-slate-900/60 p-3">
                <p className="font-semibold text-brand-light">{message.role}</p>
                <p>{message.content}</p>
              </div>
            ))}
          </div>
          {chatError ? <p className="text-xs text-red-400">{chatError}</p> : null}
          <button
            className="mt-3 w-full rounded-md border border-brand bg-transparent px-4 py-2 text-sm font-semibold text-brand disabled:opacity-60"
            disabled={chatSending}
            onClick={() => sendMessage("What is next on my itinerary?")}
          >
            {chatSending ? "Contacting companion..." : "Ask Companion"}
          </button>
        </div>
        <CollaborationPanel />
      </aside>
    </div>
  );
}
