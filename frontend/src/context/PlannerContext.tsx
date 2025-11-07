import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

interface PlannerContextState {
  persona: string;
  updatePersona: (persona: string) => void;
}

const PlannerContext = createContext<PlannerContextState | undefined>(undefined);

interface PlannerProviderProps {
  children: ReactNode;
  initialPersona: string;
}

export function PlannerContextProvider({ children, initialPersona }: PlannerProviderProps) {
  const [persona, setPersona] = useState(initialPersona);

  useEffect(() => {
    setPersona(initialPersona);
  }, [initialPersona]);

  const value = useMemo(
    () => ({
      persona,
      updatePersona: setPersona
    }),
    [persona]
  );

  return <PlannerContext.Provider value={value}>{children}</PlannerContext.Provider>;
}

export function usePlannerContext() {
  const context = useContext(PlannerContext);

  if (!context) {
    throw new Error("usePlannerContext must be used within a PlannerContextProvider");
  }

  return context;
}
