// frontend/src/pages/SeedInbox.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";

// Axios instance with proper base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

export default function SeedInbox() {
  const [seedboxes, setSeedboxes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [testing, setTesting] = useState(null);
  const [adding, setAdding] = useState(false);

  const [imapHost, setImapHost] = useState("");
  const [imapUsername, setImapUsername] = useState("");
  const [imapPassword, setImapPassword] = useState("");
  const [imapInboxFolder, setImapInboxFolder] = useState("INBOX");
  const [imapSpamFolder, setImapSpamFolder] = useState("[Gmail]/Spam");

  // Load defaults from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("imap_defaults");
    if (saved) {
      const data = JSON.parse(saved);
      setImapHost(data.host || "");
      setImapInboxFolder(data.inbox || "INBOX");
      setImapSpamFolder(data.spam || "[Gmail]/Spam");
    }
  }, []);

  // Load seedboxes
  const loadSeedboxes = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/v1/seedbox/list", { params: { user_id: 1 } });

      setSeedboxes(res.data || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load seedboxes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSeedboxes();
  }, []);

  // Add seedbox
  const handleAdd = async () => {
    if (!newEmail.trim()) return toast.error("Please enter an email address");
    if (!imapHost.trim() || !imapUsername.trim() || !imapPassword.trim())
      return toast.error("Please fill in IMAP details");

    setAdding(true);
    try {
      const res = await api.post("/seedbox/add", {
        user_id: 1,
        email_address: newEmail.trim(),
        imap_host: imapHost.trim(),
        imap_port: 993,
        imap_username: imapUsername.trim(),
        imap_password: imapPassword.trim(),
        imap_use_ssl: true,
        imap_inbox_folder: imapInboxFolder.trim(),
        imap_spam_folder: imapSpamFolder.trim(),
      });

      // Save defaults
      localStorage.setItem(
        "imap_defaults",
        JSON.stringify({
          host: imapHost,
          inbox: imapInboxFolder,
          spam: imapSpamFolder,
        })
      );

      toast.success("✅ Seed box added!");
      setShowModal(false);
      setNewEmail("");
      setImapHost("");
      setImapUsername("");
      setImapPassword("");
      setSeedboxes((prev) => [res.data, ...prev]);
    } catch (err) {
      console.error(err.response?.data || err.message);
      toast.error("Failed to add seed box");
    } finally {
      setAdding(false);
    }
  };

  // Test seedbox
  const handleTest = async (id) => {
    setTesting(id);
    try {
      toast.loading("Running inbox test...", { id: "test" });
      const res = await api.post("/seedbox/test", {
        user_id: 1,
        seedbox_id: id,
      });
      toast.dismiss("test");
      toast.success(`Result: ${res.data.result.toUpperCase()}`);
      loadSeedboxes();
    } catch (err) {
      toast.dismiss("test");
      console.error(err);
      toast.error("Failed to run seed test");
    } finally {
      setTesting(null);
    }
  };

  // Delete seedbox
  const handleDelete = async (id) => {
    if (!confirm("Delete this seed box?")) return;
    try {
      await api.delete(`/seedbox/${id}`);
      setSeedboxes((prev) => prev.filter((s) => s.id !== id));
      toast.success("Deleted");
    } catch (err) {
      console.error(err);
      toast.error("Failed to delete seed box");
    }
  };

  return (
    <div className="p-6">
      <Toaster position="top-right" />
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Seed Inbox</h1>
        <button
          className="px-4 py-2 bg-green-600 text-white rounded"
          onClick={() => setShowModal(true)}
        >
          + Add Seed Box
        </button>
      </div>

      {loading ? (
        <div>Loading…</div>
      ) : (
        <table className="w-full table-auto bg-white shadow rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left">Email</th>
              <th className="px-4 py-2 text-center">Last Status</th>
              <th className="px-4 py-2 text-center">Last Checked</th>
              <th className="px-4 py-2 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {seedboxes.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-4 text-center text-gray-500">
                  No seed boxes yet.
                </td>
              </tr>
            ) : (
              seedboxes.map((sb) => (
                <tr key={sb.id} className="border-t">
                  <td className="px-4 py-2">{sb.email_address}</td>
                  <td className="px-4 py-2 text-center">
                    {sb.last_status ? (
                      <span
                        className={`px-2 py-1 rounded text-sm font-semibold ${
                          sb.last_status.toLowerCase() === "inbox"
                            ? "bg-green-100 text-green-700"
                            : sb.last_status.toLowerCase() === "spam"
                            ? "bg-red-100 text-red-700"
                            : sb.last_status.toLowerCase() === "not_found"
                            ? "bg-gray-100 text-gray-600"
                            : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {sb.last_status.toUpperCase()}
                      </span>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td className="px-4 py-2 text-center">
                    {sb.last_checked
                      ? new Date(sb.last_checked).toLocaleString()
                      : "—"}
                  </td>
                  <td className="px-4 py-2 text-center space-x-2">
                    <button
                      onClick={() => handleTest(sb.id)}
                      disabled={testing === sb.id}
                      className="px-3 py-1 bg-blue-600 text-white rounded flex items-center justify-center"
                    >
                      {testing === sb.id ? (
                        <>
                          <svg
                            className="animate-spin h-4 w-4 mr-2 text-white"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            ></circle>
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8v8H4z"
                            ></path>
                          </svg>
                          Testing…
                        </>
                      ) : (
                        "Test Inbox"
                      )}
                    </button>
                    <button
                      onClick={() => handleDelete(sb.id)}
                      className="px-3 py-1 bg-red-600 text-white rounded"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}

      {/* Add Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white rounded p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold mb-4">Add Seed Box</h2>

            <label className="block text-sm font-medium mb-1">
              Seedbox Email Address
            </label>
            <input
              type="email"
              className="w-full border p-2 rounded mb-4"
              placeholder="btcmail47@gmail.com"
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
            />

            <label className="block text-sm font-medium mb-1">IMAP Host</label>
            <input
              type="text"
              className="w-full border p-2 rounded mb-4"
              placeholder="imap.gmail.com"
              value={imapHost}
              onChange={(e) => setImapHost(e.target.value)}
            />

            <label className="block text-sm font-medium mb-1">
              IMAP Username
            </label>
            <input
              type="text"
              className="w-full border p-2 rounded mb-4"
              placeholder="youremail@gmail.com"
              value={imapUsername}
              onChange={(e) => setImapUsername(e.target.value)}
            />

            <label className="block text-sm font-medium mb-1">
              IMAP Password / App Password
            </label>
            <input
              type="password"
              className="w-full border p-2 rounded mb-4"
              value={imapPassword}
              onChange={(e) => setImapPassword(e.target.value)}
            />

            <label className="block text-sm font-medium mb-1">
              Inbox Folder
            </label>
            <input
              type="text"
              className="w-full border p-2 rounded mb-4"
              placeholder="INBOX"
              value={imapInboxFolder}
              onChange={(e) => setImapInboxFolder(e.target.value)}
            />

            <label className="block text-sm font-medium mb-1">
              Spam/Junk Folder
            </label>
            <input
              type="text"
              className="w-full border p-2 rounded mb-4"
              placeholder="[Gmail]/Spam"
              value={imapSpamFolder}
              onChange={(e) => setImapSpamFolder(e.target.value)}
            />

            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 border rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleAdd}
                disabled={adding}
                className={`px-4 py-2 text-white rounded ${
                  adding
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-green-600 hover:bg-green-700"
                }`}
              >
                {adding ? "Adding…" : "Add"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
