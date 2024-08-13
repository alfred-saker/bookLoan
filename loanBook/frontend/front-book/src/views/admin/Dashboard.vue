<template>
  <div class="container_admin">
    <div id="app">
      <Sidebar @change-content="changeContent" />
      <div class="content">
        <component :is="currentComponent" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import Sidebar from '@/components/admin/Sidebar.vue';

import HomeContent from '@/components/admin/HomeContent.vue';
import AboutContent from '@/components/admin/AboutContent.vue';
import ContactContent from '@/components/admin/ContactContent.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt,faCaretDown } from '@fortawesome/free-solid-svg-icons';
  
library.add(faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt,faCaretDown);

export default {
  // name: 'App',
  components: {
    Sidebar,
    HomeContent,
    AboutContent,
    ContactContent,
    FontAwesomeIcon,
    // NavbarHead
  },

  setup() {
    const profil = ref('https://i.pravatar.cc/600')
    const currentComponent = ref('HomeContent');
    const changeContent = (content) => {
      if (content === 'home') {
        currentComponent.value = 'HomeContent';
      } else if (content === 'about') {
        currentComponent.value = 'AboutContent';
      } else if (content === 'contact') {
        currentComponent.value = 'ContactContent';
      }
    };
    return { currentComponent, changeContent };
  },
};
</script>

<style>
.container_admin{
  background-color: rgb(255, 255, 255);
  height: 100vh;
  width: 100%;
}
.container_admin div{
  width: 100%;
}
#app {
  display: flex;
}
.content {
  margin-left: 60px;
  transition: margin-left 0.3s;
  flex-grow: 1;
  padding:0.9em;
}
.sidebar--open + .content {
  margin-left: 200px;
}
</style>
