// Wording for "the card comes back after N days" under each rating button.

/** Arabic counts days in four ways: one, two, 3–10, 11 and more. */
export function afterDays(days) {
  if (!Number.isFinite(days) || days < 1) return ''
  if (days === 1) return 'بعد يوم واحد'
  if (days === 2) return 'بعد يومين'
  if (days <= 10) return `بعد ${days} أيام`
  return `بعد ${days} يوماً`
}

/**
 * The label for one rating of one card. `card.next_interval_days` comes from
 * the server (rating -> days), which runs the SM-2 schedule; nothing is
 * calculated here, so the label cannot drift from what a review really does.
 */
export function ratingLabel(card, quality) {
  return afterDays(card?.next_interval_days?.[quality])
}
