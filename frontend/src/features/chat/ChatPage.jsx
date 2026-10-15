import { useState, useRef, useEffect } from "react";
import { streamReply } from './streamReply';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { role: "model", content: "اسألني بالعربية أو التركية. Arapça veya Türkçe sorabilirsin." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const listRef = useRef(null);
  const requestRef = useRef(null);
  useEffect(() => () => requestRef.current?.abort(), []);

  // Keep the newest message in view by scrolling the message list itself.
  // (scrollIntoView also scrolled the whole page, pushing the chat title away.)
  useEffect(() => {
    const list = listRef.current;
    list?.scrollTo({ top: list.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setLoading(true);
    const controller = new AbortController();
    requestRef.current = controller;
    const history = [...messages.filter(m => !m.failed), { role: 'user', content: text }];
    let reply = '';
    const replyIndex = messages.length + 1;
    try {
      await streamReply(history.map(m => ({ role: m.role, content: m.content })), chunk => {
        reply += chunk;
        setMessages(prev => [...prev.slice(0, replyIndex), { role: 'model', content: reply }]);
      }, controller.signal);
    } catch (err) {
      if (!controller.signal.aborted) {
        const content = `${reply ? reply + '\n\n' : ''}⚠️ ${err.message || 'تعذّر الاتصال بالخادم'}`;
        setMessages(prev => [...prev.slice(0, replyIndex), { role: 'model', content, failed: true }]);
      }
    } finally {
      if (!controller.signal.aborted) setLoading(false);
    }
  };

  return (
    <div style={{display:"flex",flexDirection:"column",height:"calc(100vh - 64px)",background:"#F5F0E8",fontFamily:"'Segoe UI','Noto Sans Arabic',sans-serif",direction:"rtl"}}>
      <div style={{background:"#1a2744",padding:"0.875rem 1.25rem",display:"flex",alignItems:"center",gap:"0.75rem",borderBottom:"2px solid #C9A84C"}}>
        <div style={{width:"40px",height:"40px",borderRadius:"50%",background:"#C9A84C",color:"#1a2744",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"18px",fontWeight:"700"}}>م</div>
        <div>
          <div style={{fontSize:"16px",fontWeight:"700",color:"#F5F0E8"}}>مرشد</div>
          <div style={{fontSize:"11px",color:"rgba(245,240,232,0.6)"}}>العربية · Türkçe</div>
        </div>
      </div>

      <div ref={listRef} style={{flex:1,overflowY:"auto",padding:"1.25rem",display:"flex",flexDirection:"column",gap:"0.875rem"}}>
        {messages.map((msg, i) => (
          <div key={i} style={{display:"flex",gap:"0.625rem",alignItems:"flex-end",flexDirection:msg.role==="user"?"row-reverse":"row"}}>
            {msg.role==="model" && (
              <div style={{width:"32px",height:"32px",borderRadius:"50%",background:"#1a2744",color:"#C9A84C",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"14px",fontWeight:"700",flexShrink:0}}>م</div>
            )}
            <div style={{maxWidth:"75%",padding:"0.75rem 1rem",borderRadius:"16px",fontSize:"15px",lineHeight:"1.7",background:msg.role==="user"?"#1a2744":"#fff",color:msg.role==="user"?"#F5F0E8":"#222",border:msg.role==="model"?"1px solid #e8e0d0":"none"}}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && messages.at(-1)?.role !== 'model' && (
          <div style={{display:"flex",gap:"0.625rem",alignItems:"flex-end"}}>
            <div style={{width:"32px",height:"32px",borderRadius:"50%",background:"#1a2744",color:"#C9A84C",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"14px",fontWeight:"700"}}>م</div>
            <div style={{background:"#fff",border:"1px solid #e8e0d0",borderRadius:"16px",padding:"0.875rem 1rem",color:"#C9A84C",fontSize:"20px",letterSpacing:"4px"}}>···</div>
          </div>
        )}
        <div />
      </div>

      <div style={{padding:"0.875rem 1.25rem",background:"#fff",borderTop:"1px solid #e8e0d0",display:"flex",alignItems:"center",gap:"0.625rem"}}>
        <button onClick={send} disabled={loading||!input.trim()} style={{width:"42px",height:"42px",borderRadius:"50%",background:"#1a2744",border:"1.5px solid #C9A84C",color:"#F5F0E8",fontSize:"18px",cursor:"pointer",flexShrink:0}}>↑</button>
        <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()}
          placeholder="اكتب سؤالك · Sorunu yaz..." dir="auto" disabled={loading}
          style={{flex:1,border:"1.5px solid #d0c5b0",borderRadius:"12px",padding:"0.75rem 1rem",fontSize:"15px",color:"#1a2744",outline:"none",background:"#F5F0E8",fontFamily:"inherit"}} />
      </div>
    </div>
  );
}
