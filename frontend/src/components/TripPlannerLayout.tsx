import { CollaborationPanel } from "./CollaborationPanel";
import { usePlannerContext } from "../context/PlannerContext";
import { useItinerary } from "../hooks/useItinerary";
import { useMapPins } from "../hooks/useMapPins";
import { useChat } from "../hooks/useChat";

interface TripPlannerLayoutProps {
  persona: string;
}

export function TripPlannerLayout({ persona }: TripPlannerLayoutProps) {
  const { itinerary, isLoading: itineraryLoading, regenerateItinerary } = useItinerary();
  const { pins } = useMapPins(itinerary?.destination);
  const { messages, sendMessage } = useChat();
  const { updatePersona } = usePlannerContext();

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
          </div>
          <button
            className="self-start rounded-md bg-brand px-4 py-2 text-sm font-semibold text-slate-900"
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
            {(itinerary?.daily_plans ?? []).length === 0 ? (
              <li className="rounded-md border border-dashed border-slate-800 p-3 text-slate-400">
                Daily plans will appear here after the backend integration parses GPT
                function call responses.
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
                    <li key={activity.name} className="rounded bg-slate-900/60 p-2">
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
          <p className="text-sm text-slate-400">
            {pins.length === 0
              ? "Map data will appear here after fetching locations."
              : "Integrate Mapbox in the frontend to visualize pins."}
          </p>
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
          <button
            className="mt-3 w-full rounded-md border border-brand bg-transparent px-4 py-2 text-sm font-semibold text-brand"
            onClick={() => sendMessage("What is next on my itinerary?")}
          >
            Ask Companion
          </button>
        </div>
        <CollaborationPanel />
      </aside>
    </div>
  );
}
