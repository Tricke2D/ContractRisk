const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export interface UploadResponse {
  contract_id: string;
  filename: string;
  party_name: string;
  total_clauses: number;
  message: string;
}

export interface ContractReport {
  contract: {
    id: string;
    filename: string;
    party_name: string;
  };
  clauses: Array<{
    id: string;
    section_number: string | null;
    clause_text: string;
    clause_type: string;
    page_number: number;
    risk: {
      risk_level: string;
      needs_review: boolean;
      deviation_reason: string;
      confidence_score: number | null;
    } | null;
    redlines: Array<{
      id: string;
      variant_label: string;
      suggested_replacement_text: string;
      rationale: string;
      status: string;
    }>;
  }>;
}

export async function uploadContract(file: File, partyName: string): Promise<{ contractId: string }> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("party_name", partyName);

  const response = await fetch(`${API_BASE}/contracts/upload`, {
    method: "POST",
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to upload: ${response.status}`);
  }
  
  const data: UploadResponse = await response.json();
  return { contractId: data.contract_id };
}

export async function getContractReport(contractId: string): Promise<ContractReport> {
  const response = await fetch(`${API_BASE}/contracts/${contractId}/report`);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to load report: ${response.status}`);
  }
  return response.json();
}

export async function updateRedlineStatus(
  redlineId: string,
  status: "APPROVED" | "REJECTED",
  reviewerNote?: string
): Promise<{ id: string; status: string }> {
  const response = await fetch(`${API_BASE}/redlines/${redlineId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, reviewer_note: reviewerNote }),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to update status: ${response.status}`);
  }
  return response.json();
}