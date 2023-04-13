import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  ConversationHeader,
  TypingIndicator,
  Avatar
} from "@chatscope/chat-ui-kit-react";
import { useState } from "react";
import emblemURL from "./emblem.png";

const base = "http://localhost:8000/"; // Should change according to where you are hosting, ideally should not hardcode ... but meh..
const base_pdf = "http://localhost:5173/public/constitution.pdf"

function App() {
  const [messagesList, setMessagesList] = useState([<Message
    model={{
      message: "Hi, I am ConstitutionAI, I am here to help you to learn about the Indian Constitution",
      sender: "ConstitutionAI",
      direction: "incoming"
    }}
  ><Avatar src={emblemURL} name="Emblem" /></Message>]);
  const [isTyping, setIsTyping] = useState(false);

  return (
    <div style={{height: "100vh", width:"100vw" }}>
      <ChatContainer>
        <ConversationHeader>
            <Avatar src={emblemURL} name="Emblem" />
            <ConversationHeader.Content  style={{
              background:"#F8EDE3"
            }} userName="ConstitutionAI" info="Learn about the Indian Constutution" />                                   
        </ConversationHeader>
        <MessageList typingIndicator={isTyping? <TypingIndicator content="ConstitutionAI is typing"/> : undefined}>
          {messagesList}
        </MessageList>
        <MessageInput attachDisabled={true} disabled={isTyping} placeholder="Type message here" onSend={(query) => {
          const newMessage = <Message
            model={{
              message: query,
              sender: "You",
              direction: "outgoing"
            }}
          />;
          setMessagesList(old => [...old, newMessage])
          setIsTyping(true);

          fetch(base + "query/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({query})
          })
          .then(response => response.json())
          .then(data => {
            console.log('Response:', data);

            const pageNumbers = new Set();

            for(let source of data.source_documents) {
              pageNumbers.add(source.metadata.page);
            }

            let links = "";
            let i = 1;
            for(let pageNumber of pageNumbers) {
              links += `<a href="${base_pdf}#page=${pageNumber + 1}"> Source ${i}</a><br/>`
              i++;
            }

            const htmlMessage = `${data.answer}<br/><strong>Sources:</strong><br/>${links}`;

            const newAIMessage = <Message
              model={{
                payload: htmlMessage,
                sender: "ConstitutionAI",
                direction: "incoming"
              }}
            ><Avatar src={emblemURL} name="Emblem" /></Message>;
            setIsTyping(false);
            setMessagesList(old => [...old, newAIMessage]);
          })
          .catch(error => {
            console.error('Error:', error);
          });

        }} />
      </ChatContainer>
  </div>
  )
}

export default App
