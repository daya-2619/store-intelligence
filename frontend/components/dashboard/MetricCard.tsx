import {
  Card,
  CardContent,
} from "@/components/ui/card";

interface Props {

  title: string;

  value: string | number;
}

export function MetricCard({

  title,

  value,

}: Props) {

  return (

    <Card className="
    backdrop-blur-md
    bg-white/10
    border-white/20
    shadow-xl
  ">

      <CardContent className="p-6">

        <p className="text-muted-foreground text-sm">

          {title}

        </p>

        <h2 className="text-4xl font-bold mt-3">

          {value}

        </h2>

      </CardContent>

    </Card>
  );
}