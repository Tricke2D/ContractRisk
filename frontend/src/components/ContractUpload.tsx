import { useState } from "react";
import { Upload, FileText } from "lucide-react";

interface Props {
  onUpload: (file: File, partyName: string) => Promise<void>;
  isLoading: boolean;
}

export function ContractUpload({ onUpload, isLoading }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [partyName, setPartyName] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (file && partyName) {
      await onUpload(file, partyName);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-8 rounded-2xl shadow-lg border border-[#E4E1DA]">
      <div className="text-center mb-8">
        <div className="text-6xl mb-4">📄</div>
        <h2 className="text-3xl font-semibold font-ui text-[#1C1B19]">
          Upload Contract
        </h2>
        <p className="text-lg text-[#6B6862] mt-2">
          Upload a contract to analyze risks and generate redlines
        </p>
      </div>
      
      <div className="mb-6">
        <label className="block text-lg font-medium text-[#1C1B19] mb-3">
          Party Name
        </label>
        <input
          type="text"
          value={partyName}
          onChange={(e) => setPartyName(e.target.value)}
          className="w-full px-5 py-4 text-lg border-2 border-[#E4E1DA] rounded-xl focus:ring-4 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
          placeholder="Enter party name (e.g., Acme Corp)"
          required
          disabled={isLoading}
        />
      </div>

      <div className="mb-8">
        <label className="block text-lg font-medium text-[#1C1B19] mb-3">
          Contract File
        </label>
        <div className={`border-3 border-dashed border-[#E4E1DA] rounded-2xl p-10 text-center hover:border-blue-500 transition ${isLoading ? 'opacity-50' : ''}`}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="hidden"
            id="file-upload"
            accept=".pdf,.txt"
            disabled={isLoading}
          />
          <label htmlFor="file-upload" className="cursor-pointer block">
            {file ? (
              <>
                <FileText className="w-20 h-20 mx-auto text-blue-500 mb-4" />
                <p className="text-2xl font-medium text-[#1C1B19]">{file.name}</p>
                <p className="text-lg text-[#6B6862]">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </>
            ) : (
              <>
                <Upload className="w-20 h-20 mx-auto text-[#6B6862] mb-4" />
                <p className="text-xl text-[#6B6862] font-medium">Click or drag to upload</p>
                <p className="text-base text-[#6B6862] mt-2">Supports PDF and TXT files</p>
                <p className="text-sm text-[#6B6862] mt-1">Max file size: 10MB</p>
              </>
            )}
          </label>
        </div>
      </div>

      <button
        type="submit"
        disabled={!file || !partyName || isLoading}
        className="w-full bg-blue-600 text-white py-4 text-xl font-semibold rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        {isLoading ? "⏳ Processing..." : "🚀 Upload & Analyze"}
      </button>
    </form>
  );
}