import { useId } from 'react'

/**
 * The Arabiq Akademi mark: the letter ع inside a dotted gold ring, drawn as SVG.
 *
 * It is drawn rather than loaded because the logo.png that was committed to the
 * repository is not a readable image (its zero bytes were replaced by spaces
 * before it was added), which showed as a broken-image icon on the login page.
 * To use a real logo file again, add it under src/assets and render an <img>
 * here; every page that shows the logo uses this component.
 */
export default function BrandMark({ size = 140, letterColor = '#0F2044', style }) {
  const gradientId = useId()
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" role="img" aria-label="Arabiq Akademi" style={style}>
      <defs>
        <radialGradient id={gradientId} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#E8D48A" />
          <stop offset="100%" stopColor="#C9A84C" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="78" fill="none" stroke={`url(#${gradientId})`} strokeWidth="1.5" strokeDasharray="3 4" opacity="0.85" />
      <circle cx="100" cy="100" r="68" fill="none" stroke="#C9A84C" strokeWidth="0.6" opacity="0.4" />
      {Array.from({ length: 12 }).map((_, i) => {
        const a = (i * Math.PI * 2) / 12
        const x = 100 + Math.cos(a) * 78
        const y = 100 + Math.sin(a) * 78
        return <circle key={i} cx={x} cy={y} r="2.2" fill="#E8D48A" />
      })}
      <text x="100" y="135" textAnchor="middle" fontFamily="'Amiri', serif" fontSize="110" fontWeight="700" fill={letterColor}>ع</text>
    </svg>
  )
}
