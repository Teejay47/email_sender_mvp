// File: Campaigns.tsx
import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";
import { toast } from "react-hot-toast";

type CampaignItem = {
  id: number;
  subject: string;
  status: string;
  sent_count: number;
  total_recipients: number;
  seed_status?: string;
  created_at: string;
  updated_at: string;
};

// Set Axios default base URL to backend
axios.defaults.baseURL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";


export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<CampaignItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [editorOpen, setEditorOpen] = useState(false);

  // Campaign form state
  const [subject, setSubject] = useState("");
  const [htmlBody, setHtmlBody] = useState("");
  const [textBody, setTextBody] = useState("");
  const [fromName, setFromName] = useState("");
  const [smtpStrategy, setSmtpStrategy] = useState<"round_robin" | "single">(
    "round_robin"
  );
  const [seedCheck, setSeedCheck] = useState(true);

  // Flag to stop polling if backend fails repeatedly
  const [pollingError, setPollingError] = useState(false);

  // Fetch campaigns
  const fetchCampaigns = useCallback(async () => {
    try {
      const res = await axios.get("/api/v1/campaigns/list");
      setCampaigns(Array.isArray(res.data) ? res.data : res.data.items || []);
      setPollingError(false); // reset error flag on success
    } catch (err) {
      console.error("Error loading campaigns:", err);
      toast.error("Could not load campaigns");
      setPollingError(true);
    }
  }, []);

  useEffect(() => {
    fetchCampaigns();

    const interval = setInterval(() => {
      if (!pollingError) fetchCampaigns();
    }, 15000);

    return () => clearInterval(interval);
  }, [fetchCampaigns, pollingError]);

  // Create campaign
  const createCampaign = async () => {
    setLoading(true);
    try {
      await axios.post("/campaigns/create", {
        subject,
        html_body: htmlBody,
        text_body: textBody,
        from_name: fromName,
        smtp_strategy: smtpStrategy,
        seed_check: seedCheck,
      });
      toast.success("Campaign created");

      // Reset form
      setSubject("");
      setHtmlBody("");
      setTextBody("");
      setFromName("");
      setEditorOpen(false);

      fetchCampaigns();
    } catch (err) {
      console.error("Error creating campaign:", err);
      toast.error("Failed to create campaign");
    } finally {
      setLoading(false);
    }
  };

  // Start campaign
  const startCampaign = async (campaignId: number) => {
    try {
      const res = await axios.post(`/campaigns/start/${campaignId}`);
      toast.success(res.data.message || "Campaign started");
      fetchCampaigns();
    } catch (err) {
      console.error("Error starting campaign:", err);
      toast.error("Failed to start campaign");
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Campaigns Dashboard</h1>
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={() => setEditorOpen(!editorOpen)}
        >
          {editorOpen ? "Close Editor" : "Add New Campaign"}
        </button>
      </div>

      {/* Editor */}
      {editorOpen && (
        <div className="mb-6 p-4 border rounded">
          <h2 className="font-semibold">Create Campaign</h2>
          <div className="mt-3 grid grid-cols-2 gap-4">
            <input
              className="p-2 border"
              placeholder="Subject"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
            <input
              className="p-2 border"
              placeholder="From name"
              value={fromName}
              onChange={(e) => setFromName(e.target.value)}
            />
          </div>

          <div className="mt-3">
            <div className="mb-2">HTML Body</div>
            <ReactQuill value={htmlBody} onChange={setHtmlBody} />
          </div>

          <div className="mt-3">
            <div className="mb-2">Plain text</div>
            <textarea
              className="w-full p-2 border"
              rows={4}
              value={textBody}
              onChange={(e) => setTextBody(e.target.value)}
            />
          </div>

          <div className="mt-3 flex items-center gap-4 flex-wrap">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={seedCheck}
                onChange={() => setSeedCheck(!seedCheck)}
              />
              Seed check
            </label>

            <select
              value={smtpStrategy}
              onChange={(e) =>
                setSmtpStrategy(e.target.value as "round_robin" | "single")
              }
              className="p-2 border"
            >
              <option value="round_robin">Round Robin</option>
              <option value="single">Single</option>
            </select>

            <button
              className="px-4 py-2 bg-blue-600 text-white rounded"
              onClick={createCampaign}
              disabled={loading}
            >
              {loading ? "Creating..." : "Create Campaign"}
            </button>
          </div>
        </div>
      )}

      {/* Campaign list */}
      <div>
        <table className="w-full mt-3 table-auto border-collapse">
          <thead>
            <tr>
              <th className="text-left p-2 border-b">Subject</th>
              <th className="p-2 border-b">Status</th>
              <th className="p-2 border-b">Sent / Total</th>
              <th className="p-2 border-b">Seed</th>
              <th className="p-2 border-b">Actions</th>
            </tr>
          </thead>
          <tbody>
            {campaigns.map((c) => (
              <tr key={c.id} className="border-t">
                <td className="p-2">{c.subject}</td>
                <td className="p-2">{c.status}</td>
                <td className="p-2">
                  {c.sent_count} / {c.total_recipients}
                </td>
                <td className="p-2">{c.seed_status || "—"}</td>
                <td className="p-2 flex gap-2">
                  {c.status === "draft" && (
                    <button
                      className="px-2 py-1 bg-green-600 text-white rounded"
                      onClick={() => startCampaign(c.id)}
                    >
                      Start
                    </button>
                  )}
                  {c.status === "running" && (
                    <span className="px-2 py-1 bg-gray-400 text-white rounded">
                      Running
                    </span>
                  )}
                </td>
              </tr>
            ))}
            {campaigns.length === 0 && (
              <tr>
                <td colSpan={5} className="text-center p-4">
                  No campaigns found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
