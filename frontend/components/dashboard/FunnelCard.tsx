"use client";

export default function FunnelCard({ funnel }: any) {
  const entry = funnel?.entry || 0;
  const billing = funnel?.billing || 0;
  const purchase = funnel?.purchase || 0;

  return (
    <div className="rounded-2xl border bg-card p-6">

      <h2 className="text-xl font-semibold mb-6">
        Conversion Funnel
      </h2>

      <div className="space-y-4">

        <div>
          <div className="flex justify-between mb-2">
            <span>Entry</span>
            <span>{entry}</span>
          </div>

          <div className="h-4 rounded bg-blue-500 w-full" />
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span>Billing</span>
            <span>{billing}</span>
          </div>

          <div
            className="h-4 rounded bg-purple-500"
            style={{
              width: `${entry ? (billing / entry) * 100 : 0}%`,
            }}
          />
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span>Purchase</span>
            <span>{purchase}</span>
          </div>

          <div
            className="h-4 rounded bg-green-500"
            style={{
              width: `${entry ? (purchase / entry) * 100 : 0}%`,
            }}
          />
        </div>

      </div>
    </div>
  );
}