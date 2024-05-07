<script setup>
    import { ref } from 'vue';
    import * as api from '../methods/api';
    import { flash } from '../methods/alerts';

    const contact = ref(null);

    function onContactInfoFetched(code, data) {
        if (code === 200) {
            contact.value = data;
        } else {
            flash("Hubo un error al obtener la información de contacto. Por favor, vuelva a intentarlo.", "danger");
        }
    }

    api.fetchContactInfo()
        .then(({ code, data }) => {
            onContactInfoFetched(code, data);
        })
        .catch((error) => {
            onContactInfoFetched(null);
        });

</script>

<template>
    <h1 class="text-center">Centro de Investigación y Desarrollo en Tecnología de Pinturas de Argentina</h1>
    <div class="card mb-3">
        <div class="card-header">
            <h2 class="card-title mb-0">Sobre Nosotros</h2>
        </div>
        <div class="card-body">
            <p>CIDEPINT es el Centro de Investigación y Desarrollo en Tecnología de Pinturas de Argentina, nacido en los años 70 a partir de una colaboración entre varias instituciones. Su objetivo principal es promover la competitividad de los productos de pintura argentinos a nivel nacional e internacional mediante investigaciones y desarrollos en tecnología de recubrimientos. Además, se dedica a la formación de profesionales especializados y a la creación de normas en la industria. Con el tiempo, ha ampliado sus áreas de enfoque para incluir temas como el tratamiento de aceros, la protección contra la corrosión y soluciones ecológicas. Sus objetivos incluyen investigar, formar recursos humanos, difundir resultados, organizar cursos y colaborar con instituciones afines.</p>
            <p class="mb-0">CIDEPINT plantea la necesidad de que exista una plataforma para mostrar y ofrecer los servicios que prestan las diferentes Instituciones.</p>
        </div>
    </div>
    <div class="card mb-3">
        <div class="card-header">
            <h2 class="card-title mb-0">Ofrecemos</h2>
        </div>
        <div class="card-body">
            <ul class="list-group mb-0">
                <li class="list-group-item">Realizar búsqueda de servicios.</li>
                <li class="list-group-item">Iniciar solicitudes de servicios.</li>
                <li class="list-group-item">Visualizar estadísticas.</li>
                <li class="list-group-item">Visualizar cada institución y sus servicios ofrecidos.</li>
            </ul>
        </div>
    </div>
    <div class="card mb-3" v-if="contact">
        <div class="card-header">
            <h2 class="card-title mb-0">Contacto</h2>
        </div>
        <div class="card-body">
            <p>
                <h6 class="card-subtitle">Numero:</h6>
                {{ contact.phone }}
            </p>
            <p class="mb-0">
                <h6 class="card-subtitle">Correo:</h6>
                {{ contact.email }}
            </p>
        </div>
    </div>
</template>