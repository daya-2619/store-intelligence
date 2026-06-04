import { Badge } from "@/components/ui/badge";

export default function AnomalyCard({
  anomalies,
}: any) {

  return (

    <div className="border rounded-xl p-6">

      <h2 className="font-semibold mb-4">

        Active Alerts

      </h2>

      <div className="space-y-3">

        {anomalies?.map(
          (
            item: any,
            idx: number
          ) => (

            <div
              key={idx}
              className="flex justify-between"
            >

              <span>
                {item.type}
              </span>

              <Badge>

                {item.severity}

              </Badge>

            </div>
          )
        )}

      </div>

    </div>
  );
}