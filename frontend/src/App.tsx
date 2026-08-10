import { useState } from "react";
import { ContractUpload } from "./components/ContractUpload";
import { RiskSummary } from "./components/RiskSummary";
import { getContractReport, uploadContract } from "./api/contractApi";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (file: File, partyName: string) => {
    setIsLoading(true);
    setError(null);
    try {
      console.log("📤 Uploading file:", file.name);
      const result = await uploadContract(file, partyName);
      console.log("📥 Upload result:", result);
      
      if (!result.contractId) {
        console.error("❌ No contractId in response:", result);
        throw new Error("No contract ID returned from server");
      }
      
      console.log("✅ Contract ID received:", result.contractId);
      
      // Tunggu sebentar, lalu ambil report
      setTimeout(async () => {
        try {
          console.log("📊 Fetching report for:", result.contractId);
          const data = await getContractReport(result.contractId);
          console.log("📊 Report received:", data);
          setReport(data);
        } catch (err) {
          console.error("❌ Report error:", err);
          setError("Failed to load report: " + (err as Error).message);
        } finally {
          setIsLoading(false);
        }
      }, 3000);
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError("Upload failed: " + (err as Error).message);
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setReport(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-[#F7F6F3] flex items-center justify-center p-8">
      <div className="w-full max-w-5xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-[#1C1B19] font-ui tracking-tight">
            📄 Contract Risk Auditor
          </h1>
          {report && (
            <button
              onClick={handleReset}
              className="text-base text-[#6B6862] hover:text-[#1C1B19] font-medium transition"
            >
              Upload New Contract →
            </button>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border-2 border-red-200 text-red-700 p-5 rounded-xl mb-6 text-lg">
            ❌ {error}
          </div>
        )}

        {!report ? (
          <div className="flex justify-center">
            <div className="w-full max-w-2xl">
              <ContractUpload onUpload={handleUpload} isLoading={isLoading} />
            </div>
          </div>
        ) : (
          <div>
            <div className="bg-white p-6 rounded-xl shadow-sm mb-6 border border-[#E4E1DA]">
              <h2 className="text-2xl font-semibold font-ui">
                {report.contract.filename}
              </h2>
              <p className="text-lg text-[#6B6862]">Party: {report.contract.party_name}</p>
              <p className="text-base text-[#6B6862]">
                {report.clauses.length} clauses detected
              </p>
            </div>

            <RiskSummary clauses={report.clauses} />

            <div className="space-y-4 max-h-[700px] overflow-y-auto pr-2">
              {report.clauses.map((clause: any) => (
                <div key={clause.id} className="bg-white p-5 rounded-xl shadow-sm border-l-4 border-[#E4E1DA] hover:shadow-md transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="text-lg font-medium font-ui">
                        {clause.section_number || "?"}
                      </span>
                      <span className="text-base text-[#6B6862] ml-3">
                        {clause.clause_type}
                      </span>
                    </div>
                    {clause.risk && (
                      <span className={`px-4 py-1.5 rounded-full text-base font-medium ${
                        clause.risk.risk_level === "HIGH" ? "bg-[#FBE6E2] text-[#B33A2E]" :
                        clause.risk.risk_level === "MEDIUM" ? "bg-[#FBEEDA] text-[#B5760C]" :
                        "bg-[#E7F0E8] text-[#3F7A4D]"
                      }`}>
                        {clause.risk.risk_level}
                        {clause.risk.needs_review && " 🔍"}
                      </span>
                    )}
                  </div>
                  <p className="text-base text-[#1C1B19] mt-3 font-document leading-relaxed">
                    {clause.clause_text}
                  </p>
                  {clause.risk?.deviation_reason && (
                    <p className="text-base text-[#6B6862] mt-2">
                      ⚠️ {clause.risk.deviation_reason}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;