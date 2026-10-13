/* Purely decorative SVG backdrops of the login hero panel. */

const NODES = [
  {cx:10,cy:20},{cx:25,cy:12},{cx:42,cy:25},{cx:18,cy:45},{cx:35,cy:55},
  {cx:8,cy:70},{cx:28,cy:82},{cx:48,cy:72},{cx:55,cy:40},{cx:70,cy:18},
  {cx:82,cy:35},{cx:90,cy:60},{cx:75,cy:78},{cx:60,cy:90},
]
const LINKS = [[0,1],[1,2],[2,8],[0,3],[3,4],[3,5],[5,6],[4,6],[4,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[7,13],[2,9],[8,11]]

export function NeuralBackdrop() {
  return (
    <svg style={{ position:'absolute',inset:0,width:'100%',height:'100%',opacity:0.4,pointerEvents:'none' }} viewBox="0 0 100 100" preserveAspectRatio="none">
      {LINKS.map(([a,b],i) => (
        <line key={i} x1={NODES[a].cx} y1={NODES[a].cy} x2={NODES[b].cx} y2={NODES[b].cy}
          stroke="#C9A84C" strokeWidth="0.08" opacity="0.5" />
      ))}
      {NODES.map((n,i) => (
        <circle key={i} cx={n.cx} cy={n.cy} r={i%3===0?0.5:0.3} fill="#D4B96A"
          style={{ animation:`aq-pulse-node 3s ease-in-out infinite`, animationDelay:`${(i%5)*0.4}s`, transformOrigin:`${n.cx}px ${n.cy}px` }} />
      ))}
    </svg>
  )
}

export function ArabesqueCorner() {
  return (
    <svg style={{ position:'absolute',bottom:-80,left:-80,width:384,height:384,color:'#C9A84C',opacity:0.08,pointerEvents:'none' }}
      viewBox="0 0 200 200" fill="none">
      <g stroke="currentColor" strokeWidth="0.8">
        <circle cx="100" cy="100" r="90" />
        <circle cx="100" cy="100" r="70" />
        <circle cx="100" cy="100" r="50" />
        {Array.from({length:16}).map((_,i) => {
          const a = (i*Math.PI*2)/16
          return <line key={i} x1={100+Math.cos(a)*50} y1={100+Math.sin(a)*50} x2={100+Math.cos(a)*90} y2={100+Math.sin(a)*90} />
        })}
        {Array.from({length:8}).map((_,i) => {
          const a = (i*Math.PI*2)/8+Math.PI/8
          return <polygon key={i} points={`${100+Math.cos(a)*70},${100+Math.sin(a)*70} ${100+Math.cos(a+0.2)*90},${100+Math.sin(a+0.2)*90} ${100+Math.cos(a-0.2)*90},${100+Math.sin(a-0.2)*90}`} />
        })}
      </g>
    </svg>
  )
}
