import { useState, useEffect } from "react";
import {
  Pill,
  AlertTriangle,
  IndianRupee,
  Shield,
  ChevronDown,
  ChevronUp,
  X,
  Loader2,
  BadgeCheck,
  Tag,
} from "lucide-react";
import { getDrug } from "../services/api";

function InfoRow({ icon: Icon, label, value, accent = "text-slate-300" }) {
  if (!value) return null;
  return (
    <div className="flex items-start gap-2 py-1.5">
      <Icon className="w-3.5 h-3.5 mt-0.5 text-slate-500 flex-shrink-0" />
      <div className="min-w-0">
        <span className="text-[10px] uppercase tracking-wider text-slate-500 block">
          {label}
        </span>
        <span className={`text-xs ${accent} leading-snug`}>{value}</span>
      </div>
    </div>
  );
}

function CoverageTag({ label, available }) {
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium ${
        available
          ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/20"
          : "bg-slate-700/40 text-slate-500 border border-slate-700/30"
      }`}
    >
      {available ? (
        <BadgeCheck className="w-2.5 h-2.5" />
      ) : (
        <X className="w-2.5 h-2.5" />
      )}
      {label}
    </span>
  );
}

export default function DrugCard({ drugName, onClose }) {
  const [drug, setDrug] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(true);

  useEffect(() => {
    if (!drugName) return;
    setLoading(true);
    setError(null);
    getDrug(drugName)
      .then((data) => {
        setDrug(data.drug || data);
        setLoading(false);
      })
      .catch((e) => {
        setError("Drug not found");
        setLoading(false);
      });
  }, [drugName]);

  if (loading) {
    return (
      <div className="glass-card rounded-xl p-4 flex items-center justify-center gap-2 text-slate-400 text-xs">
        <Loader2 className="w-4 h-4 animate-spin" />
        Loading {drugName}...
      </div>
    );
  }

  if (error || !drug) return null;

  const savingsPercent = drug.savings_percent || 0;
  const hasCGHS = drug.cghs_codes && drug.cghs_codes.length > 0;
  const hasESIC = drug.esic_status === "yes";
  const hasInteractions = drug.has_manual_interactions;

  return (
    <div className="glass-card rounded-xl overflow-hidden animate-message-in">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-navy-700/40">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-7 h-7 rounded-lg bg-blue-500/15 flex items-center justify-center flex-shrink-0">
            <Pill className="w-3.5 h-3.5 text-blue-400" />
          </div>
          <div className="min-w-0">
            <h4 className="text-sm font-semibold text-slate-100 truncate">
              {drug.generic_name}
            </h4>
            <span className="text-[10px] text-blue-400/80">{drug.category}</span>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setExpanded(!expanded)}
            className="p-1 rounded hover:bg-navy-700/40 text-slate-400 hover:text-slate-300 transition"
          >
            {expanded ? (
              <ChevronUp className="w-3.5 h-3.5" />
            ) : (
              <ChevronDown className="w-3.5 h-3.5" />
            )}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1 rounded hover:bg-navy-700/40 text-slate-400 hover:text-slate-300 transition"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {expanded && (
        <div className="px-4 py-3 space-y-1">
          {/* Interaction flag */}
          {hasInteractions && (
            <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 mb-2">
              <AlertTriangle className="w-3 h-3 text-amber-400 flex-shrink-0" />
              <span className="text-[10px] text-amber-300">
                Known interaction scenarios — check before co-prescribing
              </span>
            </div>
          )}

          {/* Key info */}
          <InfoRow
            icon={Tag}
            label="Strength"
            value={drug.primary_strength}
          />
          <InfoRow
            icon={Pill}
            label="Brands"
            value={drug.brands?.slice(0, 3).join(", ")}
          />

          {/* Pricing */}
          {drug.brand_mrp && drug.jan_aushadhi_mrp && (
            <div className="mt-2 pt-2 border-t border-navy-700/30">
              <span className="text-[10px] uppercase tracking-wider text-slate-500 flex items-center gap-1 mb-1.5">
                <IndianRupee className="w-3 h-3" />
                Pricing
              </span>
              <div className="flex items-center gap-2">
                <div className="flex-1">
                  <div className="text-[10px] text-slate-500">Brand</div>
                  <div className="text-xs text-slate-300 font-medium">
                    ₹{drug.brand_mrp.mrp}
                  </div>
                </div>
                <div className="flex-1">
                  <div className="text-[10px] text-slate-500">Jan Aushadhi</div>
                  <div className="text-xs text-emerald-400 font-medium">
                    ₹{drug.jan_aushadhi_mrp.mrp}
                  </div>
                </div>
                {savingsPercent > 0 && (
                  <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[10px] font-semibold">
                    {savingsPercent}% off
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Coverage */}
          <div className="mt-2 pt-2 border-t border-navy-700/30">
            <span className="text-[10px] uppercase tracking-wider text-slate-500 flex items-center gap-1 mb-1.5">
              <Shield className="w-3 h-3" />
              Coverage
            </span>
            <div className="flex flex-wrap gap-1.5">
              <CoverageTag label="CGHS" available={hasCGHS} />
              <CoverageTag label="ESIC" available={hasESIC} />
              <CoverageTag label="PM-JAY" available={true} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
