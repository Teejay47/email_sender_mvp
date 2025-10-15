// frontend/src/pages/SMTPManager.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

function SMTPRow({ smtp, onTest, onEdit, onDelete }) {
  return (
    <tr className="border-b">
      <td className="px-4 py-2">{smtp.host}</td>
      <td className="px-4 py-2">{smtp.port}</td>
      <td className="px-4 py-2">{smtp.username}</td>
      <td className="px-4 py-2">{smtp.status}</td>
      <td className="px-4 py-2">{smtp.daily_limit}</td>
      <td className="px-4 py-2">{smtp.used_today}</td>
      <td className="px-4 py-2">
        <button
          className="mr-2 px-3 py-1 rounded bg-blue-500 text-white"
          onClick={() => onTest(smtp.id)}
        >
          Test
        </button>
        <button
          className="mr-2 px-3 py-1 rounded bg-yellow-500 text-white"
          onClick={() => onEdit(smtp)}
        >
          Edit
        </button>
        <button
          className="px-3 py-1 rounded bg-red-600 text-white"
          onClick={() => onDelete(smtp.id)}
        >
          Delete
        </button>
      </td>
    </tr>
  );
}

export default function SMTPManager() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({
    user_id: 1,
    host: "",
    port: 587,
    username: "",
    password: "",
    daily_limit: 0,
    hourly_limit: 0,
    status: "new",
    is_active: true,
  });

  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  });

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/v1/smtp/list"); // ✅ explicit /api/v1
      const data = Array.isArray(res.data) ? res.data : [];
      setList(data);
    } catch (err) {
      console.error(err);
      setList([]);
      alert("Failed to load SMTPs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const openAdd = () => {
    setEditing(null);
    setForm({
      user_id: 1,
      host: "",
      port: 587,
      username: "",
      password: "",
      daily_limit: 0,
      hourly_limit: 0,
      status: "new",
      is_active: true,
    });
    setShowForm(true);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await api.put(`/api/v1/smtp/${editing.id}`, form); // ✅ explicit /api/v1
        alert("Updated");
      } else {
        await api.post("/api/v1/smtp/add", form); // ✅ explicit /api/v1
        alert("Added");
      }
      setShowForm(false);
      load();
    } catch (err) {
      console.error(err);
      alert("Failed to save");
    }
  };

  const onTest = async (id) => {
    try {
      const res = await api.post("/api/v1/smtp/test", { smtp_id: id }); // ✅ explicit /api/v1
      if (res.data.status === "success") alert("Connection OK");
      else alert("Test result: " + JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      alert("Test failed: " + (err.response?.data?.detail || err.message));
    }
  };

  const onEdit = (smtp) => {
    setEditing(smtp);
    setForm({
      host: smtp.host,
      port: smtp.port,
      username: smtp.username,
      password: "",
      daily_limit: smtp.daily_limit,
      hourly_limit: smtp.hourly_limit,
      status: smtp.status,
      is_active: smtp.is_active,
    });
    setShowForm(true);
  };

  const onDelete = async (id) => {
    if (!confirm("Delete this SMTP?")) return;
    try {
      await api.delete(`/api/v1/smtp/${id}`); // ✅ explicit /api/v1
      alert("Deleted");
      load();
    } catch (err) {
      console.error(err);
      alert("Delete failed");
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">SMTP Manager</h1>
        <button
          className="px-4 py-2 bg-green-600 text-white rounded"
          onClick={openAdd}
        >
          Add SMTP
        </button>
      </div>

      {loading ? (
        <div>Loading…</div>
      ) : (
        <table className="w-full table-auto bg-white shadow rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left">Host</th>
              <th className="px-4 py-2">Port</th>
              <th className="px-4 py-2">Username</th>
              <th className="px-4 py-2">Status</th>
              <th className="px-4 py-2">Daily</th>
              <th className="px-4 py-2">Used Today</th>
              <th className="px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {list.map((smtp) => (
              <SMTPRow
                key={smtp.id}
                smtp={smtp}
                onTest={onTest}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </tbody>
        </table>
      )}

      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white rounded p-6 w-full max-w-xl">
            <h2 className="text-xl mb-4">
              {editing ? "Edit SMTP" : "Add SMTP"}
            </h2>
            <form onSubmit={onSubmit} className="space-y-3">
              <div>
                <label className="block text-sm">Host</label>
                <input
                  value={form.host}
                  onChange={(e) =>
                    setForm({ ...form, host: e.target.value })
                  }
                  className="w-full border p-2 rounded"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm">Port</label>
                  <input
                    type="number"
                    value={form.port}
                    onChange={(e) =>
                      setForm({ ...form, port: parseInt(e.target.value) })
                    }
                    className="w-full border p-2 rounded"
                  />
                </div>
                <div>
                  <label className="block text-sm">Username</label>
                  <input
                    value={form.username}
                    onChange={(e) =>
                      setForm({ ...form, username: e.target.value })
                    }
                    className="w-full border p-2 rounded"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm">Password</label>
                <input
                  type="password"
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                  className="w-full border p-2 rounded"
                />
                <small className="text-gray-500">
                  Leave empty to keep existing password (on edit)
                </small>
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 border rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
