// src/api/personApi.js
async function get(path) {
  const res = await fetch(`/api${path}`)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export const getPerson = () => get('/person')
export const getPersons = (count) => get(`/persons?count=${count}`)
export const getCpr = () => get('/cpr')
export const getName = () => get('/name')
export const address = () => get('/address')
export const getNameAndBirthDate = () => get('/name-and-birth-date')
export const getCprAndName = () => get('/cpr-and-name')
export const getCprNameAndBirthDate = () => get('/cpr-name-and-birth-date')
export const getMobilePhoneNumber = () => get('/mobile-phone-number')