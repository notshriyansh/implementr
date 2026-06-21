"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChatPanel } from "./chat/chat-panel";
import { ImplementationPlan } from "./plan/implementation-plan";

export function PaperWorkspace() {
  return (
    <div className="max-w-6xl mx-auto p-8">
      <Tabs defaultValue="chat">
        <TabsList className="mb-6">
          <TabsTrigger value="chat">Research Chat</TabsTrigger>

          <TabsTrigger value="plan">Implementation Strategy</TabsTrigger>
        </TabsList>

        <TabsContent value="chat">
          <ChatPanel />
        </TabsContent>

        <TabsContent value="plan">
          <ImplementationPlan />
        </TabsContent>
      </Tabs>
    </div>
  );
}
