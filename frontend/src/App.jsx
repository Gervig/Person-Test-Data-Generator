// src/App.jsx
import { useState } from 'react'
import * as api from './api/personApi'

const ENDPOINTS = {
  person: { label: 'Person', call: () => api.getPerson() },
  persons: { label: 'Persons', call: (count) => api.getPersons(count) },
  cpr: { label: 'CPR', call: () => api.getCpr() },
  name: { label: 'Name', call: () => api.getName() },
  address: { label: 'Address', call: () => api.address() },
  nameAndBirthDate: { label: 'Name and birth date', call: () => api.getNameAndBirthDate() },
  cprAndName: { label: 'CPR and name', call: () => api.getCprAndName() },
  cprNameAndBirthDate: { label: 'CPR, name and birth date', call: () => api.getCprNameAndBirthDate() },
  mobile: { label: 'Mobile phone number', call: () => api.getMobilePhoneNumber() },
}

export default function App() {
  const [selected, setSelected] = useState('person')
  const [count, setCount] = useState(2)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function generate() {
    setLoading(true)
    setError(null)
    try {
      setData(await ENDPOINTS[selected].call(count))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>Person Test Data Generator</h1>

      <select value={selected} onChange={(e) => setSelected(e.target.value)}>
        {Object.entries(ENDPOINTS).map(([key, { label }]) => (
          <option key={key} value={key}>{label}</option>
        ))}
      </select>

      {selected === 'persons' && (
        <input
          type="number"
          min={2}
          max={100}
          value={count}
          onChange={(e) => setCount(Number(e.target.value))}
        />
      )}

      <button onClick={generate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </main>
  )
}