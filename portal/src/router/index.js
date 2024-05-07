import { createRouter, createWebHistory } from "vue-router";
import auth from "../methods/auth";

export const routes = [
  {
    path: "/",
    name: "home",
    link: "Inicio",
    component: () => import("../views/HomeView.vue"),
  }, {
    path: "/busquedaDeServicios",
    name: "busquedaDeServicios",
    link: "Buscar Servicios",
    component: () => import("../views/BuscadorDeServiciosView.vue"),
  }, {
    path: "/solicitudes",
    name: "solicitudes",   
    link: "Mis solicitudes",   
    beforeEnter: requireAuth,
    component: () => import("../views/SolicitudesView.vue"),
  }, {
    path: "/solicitudes/:id",
    name: "solicitud",
    beforeEnter: requireAuth,
    component: () => import("../views/SolicitudView.vue"),
  }, {
    path: "/estadistica",
    name: "estadistica",   
    link: "Estadísticas",   
    component: () => import("../views/EstadisticaView.vue"),
  }, 
  {
    path: "/login",
    name: "login",
    component: () => import("../views/LoginView.vue"),
  }, {
    path: "/servicios/:id",
    name: "servicio",
    component: () => import("../views/ServicioView.vue"),
  }, {
    path: "/servicios/:id/request",
    name: "serviceRequest",
    component: () => import("../views/ServiceRequestView.vue"),
  }
];

function requireAuth(to, from, next) {
  if (auth.isAuthenticated()) {
    next();
  } else {
    next("/");
  }
}

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});
