import { Bell, Search, Store } from "lucide-react";

interface TopbarProps {
  store: string;
}

export default function Topbar({
  store,
}: TopbarProps) {
  return (
    <div className="flex items-center justify-between mb-8">

      {/* Left Section */}
      <div>

        <h1 className="text-3xl font-bold">
          Store Intelligence
        </h1>

        <div className="flex items-center gap-2 mt-2 text-muted-foreground">

          <Store size={16} />

          <span>
            Viewing Store: {store}
          </span>

        </div>

      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">

        <div
          className="
            flex items-center
            border
            rounded-xl
            px-4
            py-2
            bg-card
          "
        >

          <Search size={16} />

          <input
            placeholder="Search..."
            className="
              ml-2
              bg-transparent
              outline-none
            "
          />

        </div>

        <button
          className="
            p-2
            rounded-xl
            border
            hover:bg-muted
            transition
          "
        >

          <Bell size={20} />

        </button>

      </div>

    </div>
  );
}