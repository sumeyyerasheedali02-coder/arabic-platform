import test from 'node:test'
import assert from 'node:assert/strict'
import { csvCell, markValue, total } from '../src/format.js'

test('missing mark is different from a real zero', () => {
  assert.equal(total({ writing: 0, lab: 0 }, ['writing', 'lab']), 0)
  assert.equal(total({ writing: null, lab: 10 }, ['writing', 'lab']), null)
  assert.equal(markValue(''), null)
  assert.equal(markValue('0'), 0)
})

test('CSV names and notes cannot inject spreadsheet formulas', () => {
  assert.equal(csvCell('=HYPERLINK("bad")'), '"\'=HYPERLINK(""bad"")"')
  assert.equal(csvCell('  +123'), '"\'  +123"')
  assert.equal(csvCell('000123'), '"000123"')
  assert.equal(csvCell('Ali, "A"'), '"Ali, ""A"""')
})
