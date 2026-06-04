export default function HeatmapCard({
  heatmap,
}: any) {

  const zones = Object.entries(
    heatmap || {}
  ).filter(
    ([key]) =>
      ![
        "data_confidence",
        "total_zone_visits",
        "ENTRY",
        "EXIT"
      ].includes(key)


  );

  return (

    <div className="rounded-2xl border bg-card p-6 shadow-sm">

      <div className="flex items-center justify-between mb-6">

        <div>

          <h2 className="text-xl font-semibold">
            Zone Analytics
          </h2>

          <p className="text-sm text-muted-foreground mt-1">
            Customer movement across store zones
          </p>

        </div>

        <span
          className={`
            px-3 py-1 rounded-full text-xs font-medium
            ${
              heatmap?.data_confidence === "HIGH"
                ? "bg-green-500/10 text-green-500"
                : "bg-yellow-500/10 text-yellow-500"
            }
          `}
        >
          {heatmap?.data_confidence || "LOW"} CONFIDENCE
        </span>

      </div>

      <div className="overflow-hidden rounded-xl border">

        <table className="w-full">

          <thead className="bg-muted/50">

            <tr>

              <th className="p-4 text-left text-sm font-medium">
                Zone
              </th>

              <th className="p-4 text-right text-sm font-medium">
                Visits
              </th>

              <th className="p-4 text-right text-sm font-medium">
                Activity
              </th>

            </tr>

          </thead>

          <tbody>

            {zones.length === 0 ? (

              <tr>

                <td
                  colSpan={3}
                  className="p-6 text-center text-muted-foreground"
                >
                  No zone activity found
                </td>

              </tr>

            ) : (

              zones.map(
                ([zone, value]: any) => {

                  const visits =
                    value?.visits || 0;

                  return (

                    <tr
                      key={zone}
                      className="border-t hover:bg-muted/20 transition-colors"
                    >

                      <td className="p-4 font-medium">
                        {zone}
                      </td>

                      <td className="p-4 text-right">
                        {visits}
                      </td>

                      <td className="p-4">

                        <div className="flex justify-end">

                          <div className="w-32 h-2 rounded-full bg-muted overflow-hidden">

                            <div
                              className="h-full rounded-full bg-blue-500"
                              style={{
                                width: `${Math.min(
                                  visits * 20,
                                  100
                                )}%`,
                              }}
                            />

                          </div>

                        </div>

                      </td>

                    </tr>

                  );
                }
              )

            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}