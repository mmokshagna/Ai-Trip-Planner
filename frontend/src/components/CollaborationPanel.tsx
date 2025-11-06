export function CollaborationPanel() {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
      <h3 className="text-lg font-medium text-white">Collaborate</h3>
      <p className="mt-1 text-sm text-slate-400">
        Invite friends to co-edit this trip by sharing a secure link. Integrate with your
        authentication system to manage permissions and track edits in real time.
      </p>
      <div className="mt-3 space-y-2">
        <button className="w-full rounded-md bg-brand px-4 py-2 text-sm font-semibold text-slate-900">
          Generate Share Link
        </button>
        <button className="w-full rounded-md border border-brand bg-transparent px-4 py-2 text-sm font-semibold text-brand">
          Export as PDF
        </button>
      </div>
    </div>
  );
}
