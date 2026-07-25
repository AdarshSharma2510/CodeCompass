import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { Compass } from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isRepositoryReady, setIsRepositoryReady] = useState(false);
  const [repositoryName, setRepositoryName] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [error, setError] = useState("");

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".zip")) {
      setError("Please select a ZIP file.");
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setRepositoryName(file.name);
    setError("");
    setUploadStatus("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a repository ZIP file first.");
      return;
    }

    setIsUploading(true);
    setIsRepositoryReady(false);
    setMessages([]);
    setError("");
    setUploadStatus("Indexing repository...");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/repositories/upload`, {
        method: "POST",
        body: formData,
      });

      const responseText = await response.text();

      let data;

      try {
        data = JSON.parse(responseText);
      } catch {
        throw new Error(
          `Backend returned an unexpected response: ${responseText}`
        );
      }

      if (!response.ok) {
        throw new Error(data.detail || "Repository upload failed.");
      }

      setIsRepositoryReady(true);
      setUploadStatus(
        data.message || "Repository indexed successfully."
      );
    } catch (err) {
      setError(err.message);
      setUploadStatus("");
      setIsRepositoryReady(false);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async () => {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isSending || !isRepositoryReady) {
      return;
    }

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    setQuestion("");
    setIsSending(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      const responseText = await response.text();

      let data = {};
      try {
        data = responseText ? JSON.parse(responseText) : {};
      } catch {
        throw new Error(`Backend returned non-JSON: ${responseText}`);
      }

      if (!response.ok) {
        throw new Error(data.detail || data.message || "Failed to get a response.");
      }

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer ?? "No answer was returned.",
        },
      ]);
    } catch (err) {
      setError(`Chat request failed: ${err.message}`);
    } finally {
      setIsSending(false);
    }
  };

  const handleEndChat = async () => {
    if (!isRepositoryReady || isSending) {
      return;
    }

    setIsSending(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: trimmedQuestion,
        }),
      });

      const responseText = await response.text();

      let data;
      try {
        data = responseText ? JSON.parse(responseText) : {};
      } catch {
        throw new Error(`Backend returned non-JSON: ${responseText}`);
      }

      if (!response.ok) {
        throw new Error(data.detail || data.message || "Failed to get a response.");
      }

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer ?? "No answer was returned.",
        },
      ]);
    } catch (err) {
      setError(`Chat request failed: ${err.message}`);
    }
    finally {
      setIsSending(false);
    }
  };

  return (
    <div className="flex h-full min-h-0 flex-col bg-[#0b0f14] text-slate-200">
      <header className="shrink-0 border-b border-slate-800 bg-[#0e131a]">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-8">
          <div>
            <div className="flex items-center gap-2.5">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center text-cyan-400">
                <Compass size={200} strokeWidth={2} />
              </div>

              <div>
                <h1 className="text-xl font-semibold tracking-tight text-slate-100">
                  CodeCompass
                </h1>

                <p className="mt-1 text-sm text-slate-500">
                  Ask questions about your codebase
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 text-sm">
            <div
              className={`h-2.5 w-2.5 rounded-full ${
                isRepositoryReady ? "bg-emerald-400" : "bg-slate-600"
              }`}
            />

            <span className="text-slate-400">
              {isRepositoryReady
                ? "Repository ready"
                : "No repository loaded"}
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto grid min-h-0 w-full max-w-7xl flex-1 min-w-0 grid-cols-[340px_minmax(0,1fr)] gap-6 overflow-hidden py-8">
        <aside className="min-h-0 overflow-y-auto rounded-xl border border-slate-800 bg-[#10161e] p-5">
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
              Repository
            </p>

            <h2 className="mt-2 text-lg font-medium text-slate-100">
              Upload a codebase
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              Upload a GitHub repository as a ZIP file to start asking
              questions about its implementation.
            </p>
          </div>

          <label
            htmlFor="repository-upload"
            className="flex cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-slate-700 bg-[#0c1117] px-5 py-8 text-center transition hover:border-slate-500"
          >
            <div className="mb-3 text-2xl text-slate-400">↑</div>

            <p className="text-sm font-medium text-slate-300">
              Select repository ZIP
            </p>

            <p className="mt-1 text-xs text-slate-600">
              ZIP files only
            </p>

            <input
              id="repository-upload"
              type="file"
              accept=".zip"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {selectedFile && (
            <div className="mt-4 rounded-lg border border-slate-800 bg-[#0c1117] p-3">
              <p className="truncate text-sm text-slate-300">
                {selectedFile.name}
              </p>

              <p className="mt-1 text-xs text-slate-600">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading}
            className="mt-4 w-full rounded-lg bg-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-900 transition hover:bg-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            {isUploading ? "Indexing..." : "Upload and index"}
          </button>

          {uploadStatus && (
            <div className="mt-4 rounded-lg border border-emerald-900/60 bg-emerald-950/20 p-3 text-sm text-emerald-400">
              {uploadStatus}
            </div>
          )}

          {repositoryName && isRepositoryReady && (
            <div className="mt-6 border-t border-slate-800 pt-5">
              <p className="text-xs uppercase tracking-widest text-slate-600">
                Active repository
              </p>

              <p className="mt-2 truncate text-sm text-slate-300">
                {repositoryName}
              </p>
            </div>
          )}
        </aside>

        <section className="flex min-h-0 min-w-0 flex-col overflow-hidden rounded-xl border border-slate-800 bg-[#10161e]">
          <div className="shrink-0 flex items-center justify-between border-b border-slate-800 px-6 py-5">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-slate-500">
                Repository chat
              </p>

              <h2 className="mt-1 text-lg font-medium text-slate-100">
                {isRepositoryReady
                  ? "Ask about your codebase"
                  : "Upload a repository to begin"}
              </h2>
            </div>

            <button
              onClick={handleEndChat}
              disabled={!isRepositoryReady || isSending}
              className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-400 transition hover:border-slate-500 hover:text-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              End chat
            </button>
          </div>

          <div className="min-h-0 flex-1 overflow-y-auto p-6">
            {messages.length === 0 ? (
              <div className="flex min-h-full items-center justify-center text-center">
                <div>
                  <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl border border-slate-800 bg-[#0c1117] text-xl text-slate-500">
                    &lt;/&gt;
                  </div>

                  <h3 className="text-base font-medium text-slate-300">
                    Your repository assistant is ready when you are
                  </h3>

                  <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-600">
                    Upload a repository and ask questions about its
                    architecture, implementation, files, and behavior.
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-5">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      message.role === "user"
                        ? "justify-end"
                        : "justify-start"
                    }`}
                  >
                    <div
                      className={`min-w-0 max-w-[75%] overflow-hidden rounded-xl px-4 py-3 text-sm leading-6 ${
                        message.role === "user"
                          ? "bg-slate-200 text-slate-900"
                          : "border border-slate-800 bg-[#0c1117] text-slate-300"
                      }`}
                    >
                      {message.role === "assistant" ? (
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {message.content}
                        </ReactMarkdown>
                      ) : (
                        message.content
                      )}
                    </div>
                  </div>
                ))}

                {isSending && (
                  <div className="flex justify-start">
                    <div className="rounded-xl border border-slate-800 bg-[#0c1117] px-4 py-3 text-sm text-slate-500">
                      Thinking...
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {error && (
            <div className="mx-6 mb-4 shrink-0 rounded-lg border border-red-900/60 bg-red-950/20 px-4 py-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <div className="shrink-0 border-t border-slate-800 p-5">
            <div className="flex gap-3">
              <input
                type="text"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleSendMessage();
                  }
                }}
                disabled={!isRepositoryReady || isSending}
                placeholder={
                  isRepositoryReady
                    ? "Ask a question about the repository..."
                    : "Upload a repository to start chatting"
                }
                className="flex-1 rounded-lg border border-slate-800 bg-[#0c1117] px-4 py-3 text-sm text-slate-200 outline-none placeholder:text-slate-600 focus:border-slate-600 disabled:cursor-not-allowed disabled:opacity-50"
              />

              <button
                onClick={handleSendMessage}
                disabled={!isRepositoryReady || !question.trim() || isSending}
                className="rounded-lg bg-slate-200 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:bg-white disabled:cursor-not-allowed disabled:opacity-40"
              >
                Send
              </button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;