import {
  LayoutDashboard,
  Ticket,
  BarChart3,
  Users,
  Settings,
  LogOut,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const menuItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    title: "Tickets",
    icon: Ticket,
    path: "/tickets",
  },
  {
    title: "Analytics",
    icon: BarChart3,
    path: "/analytics",
  },
  {
    title: "Users",
    icon: Users,
    path: "/users",
  },
  {
    title: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="w-72 h-screen bg-slate-900 text-white flex flex-col">

      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-2xl font-bold">
          AI Support
        </h1>

        <p className="text-slate-400 text-sm">
          Analytics Platform
        </p>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition-all
                 ${
                   isActive
                     ? "bg-blue-600"
                     : "hover:bg-slate-800"
                 }`
              }
            >
              <Icon size={20} />

              <span>{item.title}</span>
            </NavLink>
          );
        })}

      </nav>

      {/* Logout */}

      <div className="p-4 border-t border-slate-700">

        <button className="flex items-center gap-3 w-full px-4 py-3 rounded-xl hover:bg-red-600 transition-all">

          <LogOut size={20} />

          Logout

        </button>

      </div>

    </aside>
  );
}