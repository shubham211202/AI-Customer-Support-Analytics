import { Search, Bell, UserCircle } from "lucide-react";

export default function Header() {
  return (
    <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm">

      {/* Search Bar */}
      <div className="relative w-96">
        <Search
          className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          size={20}
        />

        <input
          type="text"
          placeholder="Search tickets..."
          className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-6">

        {/* Notification */}
        <button className="relative p-2 rounded-xl hover:bg-slate-100 transition">

          <Bell size={22} />

          <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500"></span>

        </button>

        {/* User */}
        <div className="flex items-center gap-3">

          <UserCircle
            size={40}
            className="text-slate-600"
          />

          <div>
            <h3 className="font-semibold">
              Shubham Kumar
            </h3>

            <p className="text-sm text-slate-500">
              Administrator
            </p>
          </div>

        </div>

      </div>

    </header>
  );
}