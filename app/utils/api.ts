import { notifications } from "@mantine/notifications";
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
  setLoading: Dispatch<SetStateAction<boolean>>,
  setDownloadUrl: Dispatch<SetStateAction<string | null>>,
  open: () => void, // open loading info model
  close: () => void // close loading info model
) => {
  if (!file) {
    notifications.show({
      title: "Error",
      message: "Please select a file",
      color: "red",
      position: "top-right",
    });
    return;
  }
  setLoading(true);
  open();
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
    notifications.show({
      title: "Error",
      message: error.message,
      color: "red",
      position: "top-right",
    });
  }
  setLoading(false);
  close();
};

export const handleTextUpload = async (
  setLoading: Dispatch<SetStateAction<boolean>>,
  setDownloadUrl: Dispatch<SetStateAction<string | null>>,
  open: () => void, // open loading info model
  close: () => void // close loading info model
) => {
  setLoading(true);
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
    notifications.show({
      title: "Error",
      message: error.message,
      color: "red",
      position: "top-right",
    });
  }
  setLoading(false);
  close();
};
