/** The gold loading ring used across the app. */
export function Spinner({ size = 32 }) {
  return (
    <div style={{
      width: size, height: size,
      border: `${size >= 28 ? 3 : 2}px solid var(--border)`,
      borderTopColor: 'var(--gold)', borderRadius: '50%',
      animation: 'spin .8s linear infinite',
    }} />
  )
}

/** A spinner centred in a block: give either a fixed `height` or a `padding`. */
export function CenteredSpinner({ size = 32, height, padding, minHeight, background }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'center',
      ...(padding == null ? { alignItems: 'center' } : { padding }),
      ...(height == null ? {} : { height }),
      ...(minHeight == null ? {} : { minHeight }),
      ...(background == null ? {} : { background }),
    }}>
      <Spinner size={size} />
    </div>
  )
}
