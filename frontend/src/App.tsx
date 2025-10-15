import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Campaigns from "./pages/Campaigns.tsx";
import Dashboard from "./pages/Dashboard.jsx";
import Recipients from "./pages/Recipients.jsx";
import SMTPManager from "./pages/SMTPManager.jsx";
import SeedInbox from "./pages/SeedInbox.jsx";
import Settings from "./pages/Settings.jsx";


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
