"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChatPanel } from "./chat/chat-panel";

export function PaperWorkspace() {
  return (
    <div className="max-w-6xl mx-auto p-8">
      <Tabs defaultValue="chat">
        <TabsList>
          <TabsTrigger value="chat">Chat</TabsTrigger>

          <TabsTrigger value="plan">Implementation Plan</TabsTrigger>
        </TabsList>

        <TabsContent value="chat">
          <ChatPanel />
        </TabsContent>

        <TabsContent value="plan">Plan Panel</TabsContent>
      </Tabs>
    </div>
  );
}
