"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function LibraryChatbot() {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([
    { text: "Hello! I'm the Library Assistant. How can I help you today?", isUser: false },
  ])
  const [input, setInput] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to the bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Function to handle user messages and generate bot responses
  const handleSendMessage = () => {
    if (input.trim() === "") return

    // Add user message
    setMessages((prev) => [...prev, { text: input, isUser: true }])

    // Process the message and generate a response
    const userMessage = input.toLowerCase()
    let botResponse = ""

    // Simple response logic based on keywords
    if (userMessage.includes("hours") || userMessage.includes("timing")) {
      botResponse = "The library is open Monday to Friday from 9 AM to 8 PM, and on weekends from 10 AM to 6 PM."
    } else if (userMessage.includes("borrow") || userMessage.includes("loan") || userMessage.includes("check out")) {
      botResponse =
        "You can borrow up to 5 books at a time for a period of 2 weeks. You'll need your library card to check out books."
    } else if (userMessage.includes("return")) {
      botResponse =
        "Books can be returned at the front desk during library hours or through the book drop box available 24/7 outside the main entrance."
    } else if (userMessage.includes("fine") || userMessage.includes("fee")) {
      botResponse = "Late returns incur a fine of $0.50 per day per book. The maximum fine per book is $10."
    } else if (userMessage.includes("card") || userMessage.includes("membership")) {
      botResponse =
        "To get a library card, please visit the front desk with a valid ID and proof of address. The membership is free for residents."
    } else if (
      userMessage.includes("book") &&
      (userMessage.includes("find") || userMessage.includes("search") || userMessage.includes("where"))
    ) {
      botResponse =
        "You can search for books using our online catalog or ask a librarian for assistance. Books are organized by subject and author's last name."
    } else if (userMessage.includes("reserve") || userMessage.includes("hold")) {
      botResponse =
        "You can place a hold on a book through our online portal or by calling the library. We'll notify you when it's available."
    } else if (userMessage.includes("renew")) {
      botResponse =
        "Books can be renewed online, by phone, or in person, as long as no one else has requested them. You can renew a book up to 2 times."
    } else if (userMessage.includes("hello") || userMessage.includes("hi") || userMessage.includes("hey")) {
      botResponse = "Hello! How can I assist you with the library services today?"
    } else if (userMessage.includes("thank")) {
      botResponse = "You're welcome! Feel free to ask if you have any other questions about our library services."
    } else if (userMessage.includes("bye") || userMessage.includes("goodbye")) {
      botResponse = "Goodbye! Have a great day. Come back if you have more questions!"
    } else {
      botResponse =
        "I'm not sure I understand. Could you rephrase your question? You can ask about library hours, borrowing books, returns, fines, or finding specific resources."
    }

    // Add bot response after a short delay to simulate thinking
    setTimeout(() => {
      setMessages((prev) => [...prev, { text: botResponse, isUser: false }])
    }, 500)

    // Clear input field
    setInput("")
  }

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSendMessage()
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="bg-primary text-primary-foreground">
          <CardTitle className="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="lucide lucide-book-open"
            >
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
            </svg>
            Library Information System
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="h-[400px] overflow-y-auto p-4">
            {messages.map((message, index) => (
              <div key={index} className={`mb-4 flex ${message.isUser ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.isUser ? "bg-primary text-primary-foreground" : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="border-t p-4">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Type your question here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                className="flex-1"
              />
              <Button onClick={handleSendMessage} size="icon">
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

