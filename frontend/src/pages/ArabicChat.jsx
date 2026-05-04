import { useState, useRef, useEffect } from "react";

const API = "http://localhost:8003";

export default function ArabicChat() {
  const [messages, setMessages] = useState([
    { role: "model", content: "أهلاً! أنا مرشد، مساعدك في تعلم العربية 🌙" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const token = localStorage.getItem("token");

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const res = await fetch(`${API}/gemini/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ message: text, history: messages.map(m => ({ role: m.role, content: m.content })) }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "model", content: res.ok ? data.reply : "⚠️ تأكد من إعداد Gemini API key" }]);
    } catch {
      setMessages(prev => [...prev, { role: "model", content: "⚠️ تعذّر الاتصال بالخادم" }]);
    }
    setLoading(false);
  };

  return (
    <div style={{display:"flex",flexDirection:"column",height:"calc(100vh - 64px)",background:"#F5F0E8",fontFamily:"'Segoe UI','Noto Sans Arabic',sans-serif",direction:"rtl"}}>
      <div style={{background:"#1a2744",padding:"0.875rem 1.25rem",display:"flex",alignItems:"center",gap:"0.75rem",borderBottom:"2px solid #C9A84C"}}>
        <div style={{width:"40px",height:"40px",borderRadius:"50%",background:"#C9A84C",color:"#1a2744",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"18px",fontWeight:"700"}}>م</div>
        <div>
          <div style={{fontSize:"16px",fontWeight:"700",color:"#F5F0E8"}}>مرشد</div>
          <div style={{fontSize:"11px",color:"rgba(245,240,232,0.6)"}}>مساعد تعلم العربية · Gemini AI</div>
        </div>
      </div>

      <div style={{flex:1,overflowY:"auto",padding:"1.25rem",display:"flex",flexDirection:"column",gap:"0.875rem"}}>
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
        {loading && (
          <div style={{display:"flex",gap:"0.625rem",alignItems:"flex-end"}}>
            <div style={{width:"32px",height:"32px",borderRadius:"50%",background:"#1a2744",color:"#C9A84C",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"14px",fontWeight:"700"}}>م</div>
            <div style={{background:"#fff",border:"1px solid #e8e0d0",borderRadius:"16px",padding:"0.875rem 1rem",color:"#C9A84C",fontSize:"20px",letterSpacing:"4px"}}>···</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div style={{padding:"0.875rem 1.25rem",background:"#fff",borderTop:"1px solid #e8e0d0",display:"flex",alignItems:"center",gap:"0.625rem"}}>
        <button onClick={send} disabled={loading||!input.trim()} style={{width:"42px",height:"42px",borderRadius:"50%",background:"#1a2744",border:"1.5px solid #C9A84C",color:"#F5F0E8",fontSize:"18px",cursor:"pointer",flexShrink:0}}>↑</button>
        <input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()}
          placeholder="اكتب سؤالك..." dir="rtl" disabled={loading}
          style={{flex:1,border:"1.5px solid #d0c5b0",borderRadius:"12px",padding:"0.75rem 1rem",fontSize:"15px",color:"#1a2744",outline:"none",background:"#F5F0E8",fontFamily:"inherit"}} />
      </div>
    </div>
  );
}