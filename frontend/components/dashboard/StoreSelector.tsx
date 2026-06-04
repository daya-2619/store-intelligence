"use client";

export default function StoreSelector({
  store,
  setStore,
  storesList,
}: any) {
  return (
    <select
      value={store}
      onChange={(e) =>
        setStore(e.target.value)
      }
      className="border rounded-lg px-3 py-2"
    >
      {storesList && storesList.length > 0 ? (
        storesList.map((s: any) => (
          <option key={s.store_id} value={s.store_id}>
            {s.store_name}
          </option>
        ))
      ) : (
        <option value={store}>{store}</option>
      )}
    </select>
  );
}