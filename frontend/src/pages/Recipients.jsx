// frontend/src/pages/Recipients.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

export default function Recipients() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [perPage] = useState(50);
  const [filter, setFilter] = useState("all");
  const [showModal, setShowModal] = useState(false);
  const [pasted, setPasted] = useState("");
  const [file, setFile] = useState(null);
  const [importResult, setImportResult] = useState(null);
  const [importing, setImporting] = useState(false);
  const [bulkAction, setBulkAction] = useState(""); // ✅ Added this line

  const load = async () => {
    setLoading(true);
    try {
      const params = { page, per_page: perPage };
      if (filter === "valid") params.filter_status = "valid";
      if (filter === "suppressed") params.filter_status = "suppressed";
      const res = await api.get("/recipients/list", { params });
      setList(res.data || []);
    } catch (err) {
      console.error(err);
      alert("Failed to load recipients");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [page, filter]);

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] || null);
  };

  const doImport = async (asyncTask=false) => {
    setImporting(true);
    setImportResult(null);
    try {
      const form = new FormData();
      if (file) form.append("file", file);
      if (pasted) form.append("pasted", pasted);
      form.append("user_id", "1");
      if (asyncTask) form.append("async_task", "true");

      const res = await api.post("/recipients/import", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setImportResult(res.data);
      setShowModal(true);
      if (!asyncTask) load();
    } catch (err) {
      console.error(err);
      alert("Import failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setImporting(false);
    }
  };

  const toggleSuppress = async (id, current) => {
    try {
      await api.put(`/recipients/${id}/suppress`, { suppressed: !current });
      load();
    } catch (err) {
      console.error(err);
      alert("Failed to toggle suppressed");
    }
  };

  const deleteRecipient = async (id) => {
    if (!confirm("Delete recipient?")) return;
    try {
      await api.delete(`/recipients/${id}`);
      load();
    } catch (err) {
      console.error(err);
      alert("Delete failed");
    }
  };

  const handleBulkDelete = async (type, asyncTask = false) => {
    if (!confirm(`Delete all ${type} recipients? This cannot be undone.`)) return;
    try {
      const res = await api.delete(`/recipients/bulk`, {
        params: { target: type, async_task: asyncTask, user_id: 1 },
      });

      if (asyncTask && res.data.status === "queued") {
        alert(`Bulk delete task queued: ${res.data.task_id}`);
      } else {
        alert(`Deleted ${res.data.deleted} recipients`);
        load();
      }
    } catch (err) {
      console.error(err);
      alert("Bulk delete failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="p-6">
      {/* Header + Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
        <h1 className="text-2xl font-bold mb-2 sm:mb-0">Recipients</h1>

        <div className="flex items-center space-x-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="p-2 border rounded"
          >
            <option value="all">All</option>
            <option value="valid">Valid</option>
            <option value="suppressed">Suppressed</option>
          </select>

          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={() => setShowModal(true)}
          >
            Import
          </button>
        </div>
      </div>

      {/* Bulk Delete Control */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <select
          id="bulkAction"
          className="p-2 border rounded"
          onChange={(e) => setBulkAction(e.target.value)}
          value={bulkAction}
        >
          <option value="">Select bulk action</option>
          <option value="all">Delete All</option>
          <option value="invalid">Delete Invalid</option>
          <option value="suppressed">Delete Suppressed</option>
          <option value="async_all">Queue Async Delete (All)</option>
        </select>

        <button
          className="px-4 py-2 bg-red-600 text-white rounded"
          disabled={!bulkAction}
          onClick={() => {
            if (bulkAction === "async_all") handleBulkDelete("all", true);
            else if (bulkAction) handleBulkDelete(bulkAction);
          }}
        >
          Delete
        </button>
      </div>

      {/* Recipients Table */}
      {loading ? (
        <div>Loading…</div>
      ) : (
        <table className="w-full table-auto bg-white shadow rounded">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 text-left">Email</th>
              <th className="px-4 py-2">Validated</th>
              <th className="px-4 py-2">Suppressed</th>
              <th className="px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {list.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-4 text-center">
                  No recipients
                </td>
              </tr>
            ) : null}
            {list.map((r) => (
              <tr key={r.id} className={r.suppressed ? "opacity-60" : ""}>
                <td className="px-4 py-2">{r.email}</td>
                <td className="px-4 py-2">{r.validated ? "Yes" : "No"}</td>
                <td className="px-4 py-2">{r.suppressed ? "Yes" : "No"}</td>
                <td className="px-4 py-2">
                  <button
                    className="mr-2 px-3 py-1 rounded bg-yellow-500 text-white"
                    onClick={() => toggleSuppress(r.id, r.suppressed)}
                  >
                    {r.suppressed ? "Unsuppress" : "Suppress"}
                  </button>
                  <button
                    className="px-3 py-1 rounded bg-red-600 text-white"
                    onClick={() => deleteRecipient(r.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Import Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white rounded p-6 w-full max-w-2xl">
            <h2 className="text-xl mb-4">Import Recipients</h2>

            <div className="mb-3">
              <label className="block text-sm font-medium">Upload CSV or TXT</label>
              <input
                type="file"
                accept=".csv,.txt,text/csv,text/plain"
                onChange={handleFileChange}
              />
              <small className="text-gray-500 block">
                Supports CSV or TXT — one email per line or a column “email”.
              </small>
            </div>

            <div className="mb-3">
              <label className="block text-sm font-medium">Or paste emails (one per line)</label>
              <textarea
                className="w-full border p-2 rounded"
                rows={6}
                value={pasted}
                onChange={(e) => setPasted(e.target.value)}
              />
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => doImport(false)}
                disabled={importing}
                className="px-4 py-2 bg-blue-600 text-white rounded"
              >
                {importing ? "Importing…" : "Import (sync)"}
              </button>
              <button
                onClick={() => doImport(true)}
                disabled={importing}
                className="px-4 py-2 bg-gray-600 text-white rounded"
              >
                {importing ? "Queuing…" : "Queue (async)"}
              </button>
              <button
                onClick={() => {
                  setShowModal(false);
                  setImportResult(null);
                }}
                className="px-4 py-2 border rounded"
              >
                Close
              </button>
            </div>

            {importResult && (
              <div className="mt-4 p-3 bg-gray-50 rounded">
                <h3 className="font-semibold">Import Result</h3>
                <pre className="text-sm">{JSON.stringify(importResult, null, 2)}</pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
