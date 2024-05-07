import api from './api'

export default {
  async login(user, password) {
    try {
      let result = await api.auth(user, password)

      if (result.error) {
        return result;
      }

      let token = result.token
      this.setToken(token)

      let profile = await api.profile(token)
      this.setUser(profile)

      window.location = '/'
    } catch (error) {
      return { error: 'Error al iniciar sesión. Verifica tus credenciales.' };
    }
  },
  setToken(token) {
    localStorage.setItem('token', token)
  },
  setUser(user) {
    localStorage.setItem('user', JSON.stringify(user))
  },
  getToken() {
    return localStorage.getItem('token')
  },
  getUser() {
    return JSON.parse(localStorage.getItem('user'))
  },
  removeAuthData() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
  isAuthenticated() {
    return this.getToken() !== null
  }
}
