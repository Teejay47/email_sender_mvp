import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Campaigns from "./pages/Campaigns";
import Recipients from "./pages/Recipients";
import SMTPManager from "./pages/SMTPManager";
import SeedInbox from "./pages/SeedInbox";
import Settings from "./pages/Settings";

function App() {
  return (
    <div className="flex h-screen bg-gray-50 text-gray-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/campaigns" element={<Campaigns />} />
          <Route path="/recipients" element={<Recipients />} />
          <Route path="/smtp" element={<SMTPManager />} />
          <Route path="/seed-inbox" element={<SeedInbox />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
