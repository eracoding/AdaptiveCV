import { Dispatch, SetStateAction } from "react";

export const handleDownload = (downloadUrl: string) => {
  if (downloadUrl) {
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "demo.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
};

export const handleFileUpload = async (
  file: File | null,
  setMessage: Dispatch<SetStateAction<string>>,
  setLoading: Dispatch<SetStateAction<boolean>>,
  setDownloadUrl: Dispatch<SetStateAction<string | null>>,
  open: () => void, // open loading info model
  close: () => void // close loading info model
) => {
  if (!file) {
    setMessage("Please select a file");
    return;
  }
  setLoading(true);
  open();
  setMessage("");
  setDownloadUrl(null);
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await fetch("http://localhost:3000/upload-file", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to upload file");
    const blob = await response.blob();
    setDownloadUrl(URL.createObjectURL(blob));
  } catch (error: any) {
    setMessage("Error: " + error.message);
  }
  setLoading(false);
  close();
};

export const handleTextUpload = async (
  setMessage: Dispatch<SetStateAction<string>>,
  setLoading: Dispatch<SetStateAction<boolean>>,
  setDownloadUrl: Dispatch<SetStateAction<string | null>>,
  open: () => void, // open loading info model
  close: () => void // close loading info model
) => {
  setLoading(true);
  setMessage("");
  setDownloadUrl(null);
  open();
  const text = "yoyoo"; // need tp update to get the text from the textarea
  try {
    const response = await fetch("http://localhost:3000/upload-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!response.ok) throw new Error("Failed to upload text");
    const blob = await response.blob();
    setDownloadUrl(URL.createObjectURL(blob));
  } catch (error: any) {
    setMessage("Error: " + error.message);
  }
  setLoading(false);
  close();
};
