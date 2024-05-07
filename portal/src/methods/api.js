import auth from './auth.js'

export const apiURL = 'https://admin-grupo12.proyecto2023.linti.unlp.edu.ar/api'

export async function fetchJson(url, options) {
  const response = await fetch(url, options)
  return {
    code: response.status,
    data: await response.json()
  }
}

export async function fetchService(id) {
  return await fetchJson(`${apiURL}/services/${id}`)
}

export async function fetchInstitution(id) {
  return await fetchJson(`${apiURL}/institutions/${id}`)
}

export async function fetchContactInfo() {
  return await fetchJson(`${apiURL}/contact`);
}

export async function fetchServiceSearch(q, type, page) {
  return await fetchJson(`${apiURL}/services/search?q=${q}&page=${page}&type=${type}`);
}

export async function fetchServiceTypes() {
  return await fetchJson(`${apiURL}/services-types`);
}

export async function fetchState() {
  return await fetchJson(`${apiURL}/state`);
}

export async function postJson(url, data) {
  const headers = {
    'Content-Type': 'application/json'
  }

  if (auth.isAuthenticated()) headers['Authorization'] = `Bearer ${auth.getToken()}`

  return await fetchJson(url, {
    body: JSON.stringify(data),
    cache: 'no-cache',
    method: 'POST',
    mode: 'cors',
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    headers
  })
}

export async function createServiceRequest(serviceId, request) {
  return await postJson(`${apiURL}/me/requests`, {
    service_id: serviceId,
    ...request
  })
}

export default {
  async auth(user, password) {
    try {
      const res = await fetch(`${apiURL}/auth/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user, password })
      })
      if (!res.ok) {
        const errorData = await res.json()
        return { error: errorData.error }
      }
      const data = await res.json()
      return { token: data.token }
    } catch (error) {
      console.error('Error en la solicitud:', error)
      return { error: 'Error en la solicitud' }
    }
  },
  async profile(token) {
    try {
      const res = await fetch(`${apiURL}/me/profile`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      if (!res.ok) {
        throw Error(res.statusText)
      }
      const data = await res.json()
      return data
    } catch (error) {
      console.error('Error en la solicitud:', error)
    }
  },
  async requests(token, page, perPage, order, sort, filter, startDate, endDate) {
    let requestURL = `${apiURL}/me/requests?page=${page}&filter=${filter}`

    if (perPage !== null) {
      requestURL += `&per_page=${perPage}`
    }
    if (sort !== null) {
      requestURL += `&sort=${sort}`
    }
    if (order !== null) {
      requestURL += `&order=${order}`
    }
    if (startDate !== null ) {
      requestURL += `&start_date=${startDate}`
    }
    if (endDate !== null ) {
      requestURL += `&end_date=${endDate}`
    }

    try {
      const res = await fetch(requestURL, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!res.ok) {
        throw Error(`Error en la solicitud con status: ${res.status}`)
      }

      const data = await res.json()
      return data
    } catch (error) {
      console.error('Error en la solicitud:', error)
      return { error: 'Error en la solicitud' }
    }
  },
  async request(token, id) {
    try {
      const res = await fetch(`${apiURL}/me/requests/${id}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      if (!res.ok) {
        throw Error(`Error en la solicitud con status: ${res.status}`)
      }
      const data = await res.json()
      return data
    } catch (error) {
      console.error('Error en la solicitud:', error)
      return { error: 'Error en la solicitud' }
    }
  },
  async commentRequest(token, id, text) {
    try {
      return await fetch(`${apiURL}/me/requests/${id}/notes`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      })
    } catch (error) {
      console.error('Error en la solicitud:', error)
      return { error: 'Error en la solicitud' }
    }
  }
}
