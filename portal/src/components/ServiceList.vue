<script setup>
import Header from "./Header.vue"
</script>

<template>
    <div>
        <h2>Listado de Servicios</h2>
        <ul>
            <li v-for="service in services" :key="service.id" @click="selectService(service)">
                {{ service.title }}
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    props: {
        services: Array,
    },
    methods: {
        selectService(service) {
            this.$emit("selectService", service);
        },
    },
};
</script>
