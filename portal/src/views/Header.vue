<script setup>
import { routes } from '../router';
import auth from '../methods/auth.js';

const logout = () => {
  auth.removeAuthData();
  window.location.href = '/';
}
</script>

<template>
  <header class="mb-3 border-bottom bg-body-tertiary">
    <nav class="navbar navbar-expand-md">
      <div class="container-fluid">
        <span class="navbar-brand">CIDEPINT</span>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-md-0">
            <template v-for="r in routes">
              <li class="nav-item" v-if="r.link">
                <RouterLink v-if="r.path !== '/solicitudes' || auth.isAuthenticated()" class="nav-link" :to="r.path">{{
                  r.link }}</RouterLink>
              </li>
            </template>
          </ul>
          <template v-if="auth.getUser() !== null">
            <span class="navbar-text me-3">{{ `${auth.getUser().first_name} ${auth.getUser().last_name}` }}</span>
            <button class="btn btn-outline-primary" type="button" @click="logout">Cerrar sesión</button>
          </template>
          <template v-else>
            <RouterLink to="/login">
              <button class="btn btn-outline-primary" type="button">Iniciar sesión</button>
            </RouterLink>
          </template>
        </div>
      </div>
    </nav>
  </header>
</template>
