import { type NextRequest, NextResponse } from "next/server"

// This is a simple implementation. In a real application, you might want to use
// a more sophisticated NLP approach or connect to an external API.
export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json()

    // Simple keyword-based response logic
    const userMessage = message.toLowerCase()
    let response = ""

    if (userMessage.includes("hours") || userMessage.includes("timing")) {
      response = "The library is open Monday to Friday from 9 AM to 8 PM, and on weekends from 10 AM to 6 PM."
    } else if (userMessage.includes("borrow") || userMessage.includes("loan") || userMessage.includes("check out")) {
      response =
        "You can borrow up to 5 books at a time for a period of 2 weeks. You'll need your library card to check out books."
    } else if (userMessage.includes("return")) {
      response =
        "Books can be returned at the front desk during library hours or through the book drop box available 24/7 outside the main entrance."
    } else if (userMessage.includes("fine") || userMessage.includes("fee")) {
      response = "Late returns incur a fine of $0.50 per day per book. The maximum fine per book is $10."
    } else if (userMessage.includes("card") || userMessage.includes("membership")) {
      response =
        "To get a library card, please visit the front desk with a valid ID and proof of address. The membership is free for residents."
    } else if (
      userMessage.includes("book") &&
      (userMessage.includes("find") || userMessage.includes("search") || userMessage.includes("where"))
    ) {
      response =
        "You can search for books using our online catalog or ask a librarian for assistance. Books are organized by subject and author's last name."
    } else if (userMessage.includes("reserve") || userMessage.includes("hold")) {
      response =
        "You can place a hold on a book through our online portal or by calling the library. We'll notify you when it's available."
    } else if (userMessage.includes("renew")) {
      response =
        "Books can be renewed online, by phone, or in person, as long as no one else has requested them. You can renew a book up to 2 times."
    } else if (userMessage.includes("hello") || userMessage.includes("hi") || userMessage.includes("hey")) {
      response = "Hello! How can I assist you with the library services today?"
    } else if (userMessage.includes("thank")) {
      response = "You're welcome! Feel free to ask if you have any other questions about our library services."
    } else if (userMessage.includes("bye") || userMessage.includes("goodbye")) {
      response = "Goodbye! Have a great day. Come back if you have more questions!"
    } else {
      response =
        "I'm not sure I understand. Could you rephrase your question? You can ask about library hours, borrowing books, returns, fines, or finding specific resources."
    }

    return NextResponse.json({ response })
  } catch (error) {
    console.error("Error processing chat message:", error)
    return NextResponse.json({ error: "Failed to process your message" }, { status: 500 })
  }
}

