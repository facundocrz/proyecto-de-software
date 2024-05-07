<script setup>
  import { ref } from "vue";
  import { RouterView } from "vue-router";
  import Header from "./views/Header.vue";
  import Footer from "./views/Footer.vue";
  import * as api from "./methods/api";
  import { onFlash } from "./methods/alerts.js"

  const alertsStorage = localStorage.getItem("alerts");
  const alerts = ref(alertsStorage ? JSON.parse(alertsStorage) : []);

  function pushAlert(a) {
    alerts.value.push(a);
    localStorage.setItem("alerts", JSON.stringify(alerts.value));
  }

  function popAlert(a) {
    alerts.value.pop(a);
    localStorage.setItem("alerts", JSON.stringify(alerts.value));
  }

  onFlash(pushAlert);

  const message = ref(null)
  const enabled = ref(null)
  const disabled = ref(null)

  api.fetchState()
    .then(({ code, data }) => {
      if (code === 200) {
        if (data.enabled) {
          enabled.value = true
        } else {
          message.value = data.message
          disabled.value = true
        }
      } else {
        message.value = "Error al comunicarse con el servidor"
        disabled.value = true
      }
    })
    .catch(() => {
      message.value = "Error al comunicarse con el servidor"
      disabled.value = true
    })
</script>

<template>
  <template v-if="enabled">
    <Header/>
    <template v-for="a in alerts">
      <div :class="`alert alert-${a.type} alert-dismissible`" role="alert">
        {{ a.text }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" @click="popAlert(a)"></button>
      </div>
    </template>
    <main class="container-fluid">
      <RouterView/>
    </main>
    <Footer/>
  </template>
  <template v-if="disabled">
    <main class="container-fluid d-flex flex-column align-items-center justify-content-center">
      <h1>¡El sitio se encuentra en mantenimiento!</h1>
      <p>{{ message }}</p>
    </main>
  </template>
</template>