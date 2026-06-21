"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface Props {
  onSend: (question: string) => void;
  disabled?: boolean;
  initialValue?: string;
}

export function ChatInput({ onSend, disabled, initialValue }: Props) {
  const [value, setValue] = useState("");

  useEffect(() => {
    if (initialValue) {
      setValue(initialValue);
    }
  }, [initialValue]);

  function handleSend() {
    if (!value.trim()) return;

    onSend(value);

    setValue("");
  }

  return (
    <div className="border-t p-4">
      <Textarea
        value={value}
        disabled={disabled}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask a question about the paper..."
      />

      <div className="flex justify-end mt-3">
        <Button onClick={handleSend} disabled={disabled}>
          Send
        </Button>
      </div>
    </div>
  );
}
