interface RiskSummaryProps {
  clauses: Array<{
    risk?: { risk_level: string; needs_review: boolean };
  }>;
}

export function RiskSummary({ clauses }: RiskSummaryProps) {
  const stats = {
    LOW: clauses.filter(c => c.risk?.risk_level === "LOW").length,
    MEDIUM: clauses.filter(c => c.risk?.risk_level === "MEDIUM").length,
    HIGH: clauses.filter(c => c.risk?.risk_level === "HIGH").length,
    needsReview: clauses.filter(c => c.risk?.needs_review).length,
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-5 mb-8">
      <div className="bg-[#E7F0E8] p-6 rounded-xl border-2 border-[#3F7A4D] text-center">
        <div className="text-4xl font-bold text-[#3F7A4D]">{stats.LOW}</div>
        <div className="text-lg text-[#3F7A4D] font-medium mt-1">LOW Risk</div>
      </div>
      <div className="bg-[#FBEEDA] p-6 rounded-xl border-2 border-[#B5760C] text-center">
        <div className="text-4xl font-bold text-[#B5760C]">{stats.MEDIUM}</div>
        <div className="text-lg text-[#B5760C] font-medium mt-1">MEDIUM Risk</div>
      </div>
      <div className="bg-[#FBE6E2] p-6 rounded-xl border-2 border-[#B33A2E] text-center">
        <div className="text-4xl font-bold text-[#B33A2E]">{stats.HIGH}</div>
        <div className="text-lg text-[#B33A2E] font-medium mt-1">HIGH Risk</div>
      </div>
      <div className="bg-[#EDE8F5] p-6 rounded-xl border-2 border-[#5B4FBA] text-center">
        <div className="text-4xl font-bold text-[#5B4FBA]">{stats.needsReview}</div>
        <div className="text-lg text-[#5B4FBA] font-medium mt-1">Needs Review</div>
      </div>
    </div>
  );
}