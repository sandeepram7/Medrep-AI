import { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Stethoscope,
  Users,
  ShieldCheck,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
  Sparkles,
  FileText,
  Zap,
  Mic,
  MicOff,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import { sendQuery, API_BASE } from "../services/api";
import DrugCard from "../components/DrugCard";

/* ── Typing animation ── */
function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      <div className="typing-dot w-2 h-2 rounded-full bg-blue-400" />
      <div className="typing-dot w-2 h-2 rounded-full bg-blue-400" />
      <div className="typing-dot w-2 h-2 rounded-full bg-blue-400" />
    </div>
  );
}

/* ── Interaction alert strip inside a message ── */
function InteractionAlert({ content }) {
  const lines = content.split("\n");
  const alertLines = [];
  for (const line of lines) {
    const lower = line.toLowerCase();
    if (
      (lower.includes("interaction") ||
        lower.includes("⚠") ||
        lower.includes("warning") ||
        lower.includes("caution") ||
        lower.includes("alert")) &&
      (lower.includes("severity") ||
        lower.includes("high") ||
        lower.includes("moderate") ||
        lower.includes("risk") ||
        lower.includes("avoid") ||
        lower.includes("contraindicated"))
    ) {
      alertLines.push(line.replace(/[*#]+/g, "").trim());
    }
  }
  if (alertLines.length === 0) return null;

  return (
    <div className="mb-3 px-3 py-2.5 rounded-lg bg-red-500/10 border border-red-500/25 flex items-start gap-2 animate-message-in">
      <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" />
      <div className="text-xs text-red-300 space-y-0.5 font-medium">
        {alertLines.slice(0, 2).map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>
    </div>
  );
}

/* ── Collapsible sources panel ── */
function SourcesList({ sources }) {
  const [open, setOpen] = useState(false);
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2 pt-2 border-t border-navy-600/30">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 text-[11px] text-slate-500 hover:text-slate-400 transition-colors"
      >
        {open ? (
          <ChevronDown className="w-3 h-3" />
        ) : (
          <ChevronRight className="w-3 h-3" />
        )}
        <FileText className="w-3 h-3" />
        {sources.length} source{sources.length !== 1 ? "s" : ""} referenced
      </button>
      {open && (
        <div className="flex flex-wrap gap-1 mt-1.5 animate-message-in">
          {sources.map((s, i) => (
            <span
              key={i}
              className="px-2 py-0.5 text-[10px] rounded-full bg-navy-700/60 text-slate-400 border border-navy-600/20"
            >
              {s}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Chat bubble ── */
function ChatBubble({ message }) {
  const isUser = message.role === "user";
  const isInteraction =
    message.intent === "interaction" || message.intent === "comparison";

  return (
    <div
      className={`animate-message-in flex gap-3 ${
        isUser ? "flex-row-reverse" : ""
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser
            ? "bg-sky-500/20 text-sky-400"
            : "bg-blue-500/20 text-blue-400"
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Bubble */}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-blue-500/20 text-slate-100 rounded-tr-md"
            : "glass-card text-slate-200 rounded-tl-md"
        }`}
      >
        {isUser ? (
          message.content
        ) : (
          <>
            {/* Interaction alert strip */}
            {isInteraction && <InteractionAlert content={message.content} />}

            {/* Markdown body */}
            <div
              className="prose prose-invert prose-sm max-w-none
                prose-headings:text-slate-100 prose-headings:font-semibold prose-headings:mt-3 prose-headings:mb-1
                prose-h3:text-base prose-h4:text-sm
                prose-p:text-slate-200 prose-p:my-1.5
                prose-strong:text-blue-300
                prose-li:text-slate-200 prose-li:my-0.5
                prose-ul:my-1 prose-ol:my-1
                prose-table:text-xs prose-th:text-slate-300 prose-td:text-slate-300
                prose-th:px-2 prose-th:py-1 prose-td:px-2 prose-td:py-1
                prose-th:border prose-th:border-navy-600 prose-td:border prose-td:border-navy-600
                prose-hr:border-navy-600 prose-hr:my-2
                prose-code:text-sky-300 prose-code:bg-navy-800 prose-code:px-1 prose-code:rounded
              "
            >
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>

            {/* Collapsible sources */}
            <SourcesList sources={message.sources} />
          </>
        )}
      </div>
    </div>
  );
}

/* ── Clinical scenario cards for empty state ── */
const CLINICAL_SCENARIOS = [
  {
    icon: AlertTriangle,
    label: "Drug Interaction",
    query: "Patient on Metformin + Losartan — is adding Ibuprofen safe?",
    color: "text-red-400",
    bg: "bg-red-500/10 border-red-500/15",
  },
  {
    icon: Zap,
    label: "Drug Comparison",
    query: "How does Atorvastatin compare to Rosuvastatin in efficacy and pricing?",
    color: "text-amber-400",
    bg: "bg-amber-500/10 border-amber-500/15",
  },
  {
    icon: ShieldCheck,
    label: "Reimbursement",
    query: "What is the CGHS/ESIC coverage for Amlodipine vs Telmisartan?",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10 border-emerald-500/15",
  },
  {
    icon: Sparkles,
    label: "Cost Savings",
    query: "Jan Aushadhi pricing and savings for common diabetes drugs",
    color: "text-sky-400",
    bg: "bg-sky-500/10 border-sky-500/15",
  },
];

/* ── Convert JSON-shaped API response to readable markdown ── */
function jsonResponseToMarkdown(data) {
  const parts = [];
  if (data.summary) parts.push(data.summary);

  if (data.drug_information) {
    parts.push("\n### Drug Information\n");
    if (typeof data.drug_information === "string") {
      parts.push(data.drug_information);
    } else if (typeof data.drug_information === "object") {
      Object.entries(data.drug_information).forEach(([k, v]) => {
        if (v) parts.push(`- **${k.replace(/_/g, " ")}:** ${v}`);
      });
    }
  }

  if (data.interactions && data.interactions.length > 0) {
    parts.push("\n### Interaction Alerts\n");
    data.interactions.forEach((ix) => {
      const severity = ix.severity ? `**${ix.severity}**` : "";
      const drugs = (ix.drugs_involved || []).join(", ");
      parts.push(`- ${severity} (${drugs}): ${ix.description || ""}`);
      if (ix.recommendation) {
        parts.push(`  - *Recommendation:* ${ix.recommendation}`);
      }
    });
  }

  if (data.safety_warnings && data.safety_warnings.length > 0) {
    parts.push("\n### Safety Warnings\n");
    data.safety_warnings.forEach((w) => parts.push(`- ⚠️ ${w}`));
  }

  if (data.recommendations) {
    parts.push("\n### Recommendations\n");
    if (Array.isArray(data.recommendations)) {
      data.recommendations.forEach((r) => parts.push(`- ${r}`));
    } else {
      parts.push(String(data.recommendations));
    }
  }

  if (data.reimbursement) {
    parts.push("\n### Reimbursement\n");
    if (typeof data.reimbursement === "object" && !Array.isArray(data.reimbursement)) {
      Object.entries(data.reimbursement).forEach(([k, v]) => {
        if (v) parts.push(`- **${k.replace(/_/g, " ")}:** ${v}`);
      });
    } else if (Array.isArray(data.reimbursement)) {
      data.reimbursement.forEach((r) => parts.push(`- ${r}`));
    } else {
      parts.push(String(data.reimbursement));
    }
  }

  if (data.disclaimer) {
    parts.push(`\n> ${data.disclaimer}`);
  }

  // Fallback: if we extracted almost nothing, list all non-null values
  if (parts.length <= 1) {
    Object.entries(data).forEach(([k, v]) => {
      if (v && k !== "summary" && k !== "disclaimer" && k !== "sources") {
        parts.push(`**${k.replace(/_/g, " ")}:** ${typeof v === "object" ? JSON.stringify(v) : v}`);
      }
    });
  }

  return parts.join("\n") || JSON.stringify(data, null, 2);
}

/* ── Main page ── */
export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("doctor");
  const [activeDrugs, setActiveDrugs] = useState([]);
  const [showPanel, setShowPanel] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const bottomRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  /* ── Audio Recording for STT ── */
  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm",
      });

      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });
        await sendAudioForTranscription(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Microphone access error:", err);
      alert("Could not access microphone. Please allow microphone permissions.");
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }

  async function sendAudioForTranscription(audioBlob) {
    setIsTranscribing(true);
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      const response = await fetch(`${API_BASE}/transcribe`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Transcription failed");
      }

      const data = await response.json();
      setInput(data.text || "");
    } catch (err) {
      console.error("Transcription error:", err);
      alert("Speech-to-text failed. Please try again.");
    } finally {
      setIsTranscribing(false);
    }
  }

  function toggleRecording() {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  /* Generate follow-up suggestions */
  function getFollowUps() {
    if (messages.length === 0) return [];
    const last = messages[messages.length - 1];
    if (last.role !== "assistant" || !last.drugs || last.drugs.length === 0)
      return [];

    const drug = last.drugs[0];
    const intent = last.intent || "";
    const followUps = [];

    if (intent !== "pricing")
      followUps.push(`Jan Aushadhi pricing for ${drug}`);
    if (intent !== "reimbursement")
      followUps.push(`CGHS/ESIC coverage for ${drug}`);
    if (intent !== "interaction" && last.drugs.length >= 1)
      followUps.push(`Key interactions for ${drug}`);
    if (intent !== "comparison")
      followUps.push(`Compare ${drug} with alternatives`);

    return followUps.slice(0, 3);
  }

  async function handleSend(text) {
    const query = text || input.trim();
    if (!query) return;

    const userMsg = { role: "user", content: query };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendQuery(query, mode);

      // Extract response text — handle both normal and JSON-schema responses
      let responseText;
      if (data.response) {
        responseText = data.response;
      } else if (data.answer) {
        responseText = data.answer;
      } else if (data.summary || data.drug_information || data.interactions) {
        // LLM returned structured JSON — convert to readable markdown
        responseText = jsonResponseToMarkdown(data);
      } else {
        responseText = JSON.stringify(data, null, 2);
      }

      const drugs = data.drugs || [];
      // Extract sources from either our wrapper or the LLM's JSON
      let sources = data.sources || [];
      if (Array.isArray(sources) && sources.length > 0 && typeof sources[0] === "object") {
        // LLM returned sources as objects like {database, snippet}
        sources = sources.map((s) => s.database || s.snippet || JSON.stringify(s));
      }

      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: responseText,
          sources,
          drugs,
          intent: data.intent || "",
        },
      ]);
      // Update sidebar drug cards — show up to 2 most recent drugs
      if (drugs.length > 0) {
        setActiveDrugs(drugs.slice(0, 2));
        setShowPanel(true);
      }
    } catch (err) {
      let errorMsg;
      try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
          errorMsg =
            "The AI model is temporarily rate-limited. Please wait a few seconds and try again.";
        } else {
          errorMsg =
            "Sorry, the backend is not connected yet. Please make sure the Flask server is running.";
        }
      } catch {
        errorMsg =
          "Sorry, the backend is not connected yet. Please make sure the Flask server is running.";
      }
      setMessages((m) => [
        ...m,
        { role: "assistant", content: errorMsg },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  const hasDrugPanel = activeDrugs.length > 0 && showPanel;

  return (
    <div className="flex flex-col h-full">
      {/* HCP Banner */}
      <div className="flex items-center gap-2 px-6 py-1.5 bg-amber-500/10 border-b border-amber-500/20">
        <ShieldCheck className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
        <p className="text-[11px] text-amber-300/90">
          For healthcare professionals only. Not for self-medication or patient
          self-service.
        </p>
      </div>

      {/* Header */}
      <header className="flex items-center justify-between px-6 py-3 border-b border-navy-700/40">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">MedRep AI</h2>
          <p className="text-[11px] text-slate-400">
            Drug information &bull; Interactions &bull; Pricing &bull;
            Reimbursement
          </p>
        </div>
        {/* Mode toggle */}
        <div className="flex items-center gap-1 p-1 rounded-lg bg-navy-800 border border-navy-700/50">
          <button
            onClick={() => setMode("doctor")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              mode === "doctor"
                ? "bg-blue-500/20 text-blue-400"
                : "text-slate-400 hover:text-slate-300"
            }`}
          >
            <Stethoscope className="w-3.5 h-3.5" />
            Doctor
          </button>
          <button
            onClick={() => setMode("patient")}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
              mode === "patient"
                ? "bg-teal-500/20 text-teal-400"
                : "text-slate-400 hover:text-slate-300"
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            Patient
          </button>
        </div>
      </header>

      {/* Content: Chat + Drug Panel */}
      <div className="flex-1 flex overflow-hidden">
        {/* ── Left: Chat ── */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center">
                {/* Empty state */}
                <div className="w-14 h-14 mb-4 rounded-2xl bg-gradient-to-br from-blue-500/20 to-sky-500/10 flex items-center justify-center border border-blue-500/10">
                  <Stethoscope className="w-7 h-7 text-blue-400" />
                </div>
                <h3 className="text-lg font-semibold text-slate-200 mb-1">
                  Digital Medical Representative
                </h3>
                <p className="text-xs text-slate-400 mb-6 max-w-md">
                  Evidence-based drug information for licensed HCPs — powered by
                  31 curated molecules, interaction alerts, Jan Aushadhi pricing,
                  and PM-JAY / CGHS / ESIC reimbursement data.
                </p>

                {/* Clinical Scenario Cards */}
                <div className="w-full max-w-xl">
                  <p className="text-[10px] uppercase tracking-widest text-slate-500 mb-3">
                    Clinical Scenarios
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {CLINICAL_SCENARIOS.map((s) => {
                      const Icon = s.icon;
                      return (
                        <button
                          key={s.label}
                          onClick={() => handleSend(s.query)}
                          className="text-left px-4 py-3 rounded-xl text-xs glass-card border hover:scale-[1.01] hover:border-blue-500/25 transition-all duration-150 group"
                        >
                          <div className="flex items-center gap-2 mb-1.5">
                            <div
                              className={`w-6 h-6 rounded-md flex items-center justify-center ${s.bg}`}
                            >
                              <Icon className={`w-3 h-3 ${s.color}`} />
                            </div>
                            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 group-hover:text-slate-300">
                              {s.label}
                            </span>
                          </div>
                          <p className="text-slate-300 leading-relaxed">
                            {s.query}
                          </p>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <ChatBubble key={i} message={m} />
            ))}

            {/* Follow-up chips */}
            {!loading && getFollowUps().length > 0 && (
              <div className="flex flex-wrap gap-2 pl-11">
                {getFollowUps().map((f, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(f)}
                    className="px-3 py-1.5 text-[11px] rounded-lg border border-blue-500/20 text-blue-300 hover:bg-blue-500/10 hover:border-blue-500/30 transition-all"
                  >
                    {f}
                  </button>
                ))}
              </div>
            )}

            {loading && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="px-6 py-3 border-t border-navy-700/40">
            {/* Transcription status */}
            {isTranscribing && (
              <div className="flex items-center gap-2 mb-2 px-2 max-w-3xl mx-auto">
                <div className="typing-dot w-1.5 h-1.5 rounded-full bg-blue-400" />
                <span className="text-[11px] text-slate-400">Transcribing your voice...</span>
              </div>
            )}
            <div className="flex items-end gap-3 max-w-3xl mx-auto">
              <div className="flex-1 relative">
                <textarea
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={
                    isTranscribing
                      ? "Transcribing..."
                      : mode === "doctor"
                        ? "Ask about any drug, interaction, or scheme..."
                        : "Ask about your medicine in simple language..."
                  }
                  disabled={isTranscribing}
                  className="w-full px-4 py-3 rounded-xl bg-navy-800 border border-navy-600/50 text-sm text-slate-200 placeholder-slate-500 resize-none input-glow focus:outline-none focus:border-blue-500/40 transition-all disabled:opacity-50"
                />
              </div>
              {/* Mic button */}
              <button
                onClick={toggleRecording}
                disabled={loading || isTranscribing}
                className={`flex items-center justify-center w-11 h-11 rounded-xl border transition-all ${
                  isRecording
                    ? "bg-red-500/20 border-red-500/50 text-red-400 mic-pulse"
                    : isTranscribing
                      ? "bg-blue-500/20 border-blue-500/50 text-blue-400 animate-pulse"
                      : "bg-navy-800 border-navy-600/50 text-slate-400 hover:text-slate-300 hover:border-slate-500/50"
                } disabled:cursor-not-allowed`}
                title={isRecording ? "Stop recording" : isTranscribing ? "Transcribing..." : "Voice input"}
              >
                {isRecording ? (
                  <MicOff className="w-4 h-4" />
                ) : (
                  <Mic className="w-4 h-4" />
                )}
              </button>
              {/* Send button */}
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || loading}
                className="flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-r from-blue-500 to-sky-500 text-white hover:from-blue-600 hover:to-sky-600 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* ── Right: Drug Info Panel ── */}
        {hasDrugPanel && (
          <aside className="w-72 border-l border-navy-700/40 bg-navy-900/40 overflow-y-auto flex-shrink-0 hidden lg:block animate-message-in">
            <div className="px-3 py-3 border-b border-navy-700/30 flex items-center justify-between">
              <span className="text-[10px] uppercase tracking-widest text-slate-500 font-medium">
                Drug Quick Info
              </span>
              <button
                onClick={() => setShowPanel(false)}
                className="text-slate-500 hover:text-slate-400 text-[10px] transition"
              >
                Hide
              </button>
            </div>
            <div className="p-3 space-y-3">
              {activeDrugs.map((drug) => (
                <DrugCard
                  key={drug}
                  drugName={drug}
                  onClose={() =>
                    setActiveDrugs((prev) => prev.filter((d) => d !== drug))
                  }
                />
              ))}
            </div>
          </aside>
        )}
      </div>
    </div>
  );
}
