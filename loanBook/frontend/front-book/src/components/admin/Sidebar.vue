<template>
    <div :class="['sidebar', { 'sidebar--open': isOpen }]">
      <button @click="toggleSidebar" class="toggle-button">
        <font-awesome-icon :icon="isOpen ? 'times' : 'bars'" />
      </button>
      <ul>
        <li @click="changeContent('home')">
          <font-awesome-icon icon="home" />
          <span v-if="isOpen">Home</span>
        </li>
        <li @click="changeContent('about')">
          <font-awesome-icon icon="info-circle" />
          <span v-if="isOpen">About</span>
        </li>
        <li @click="changeContent('contact')">
          <font-awesome-icon icon="envelope" />
          <span v-if="isOpen">Contact</span>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { library } from '@fortawesome/fontawesome-svg-core';
  import { faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
  
  library.add(faBars, faTimes, faHome, faInfoCircle, faEnvelope,faSignOutAlt);
  
  export default {
    name: 'Sidebar',
    components: {
      FontAwesomeIcon,
    },
    setup(_, { emit }) {
      const isOpen = ref(false);
      const toggleSidebar = () => {
        isOpen.value = !isOpen.value;
      };
      const changeContent = (content) => {
        emit('change-content', content);
      };
      return { isOpen, toggleSidebar, changeContent };
    },
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 80px;
    height: 100vh;
    background: #333;
    color: white;
    transition: width 0.5s;
    position: fixed;
    overflow: hidden;
    padding: 1em;
    z-index: 1000;
  }
  .sidebar--open {
    width: 400px;
    opacity: 1;
  }
  .toggle-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 20px;
    margin: 10px;
  }
  ul {
    list-style: none;
    padding: 0;
    margin: 20px 0 0 0;
  }
  li {
    margin: 20px 10px;
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  li span {
    margin-left: 10px;
  }
  @media screen and (max-width: 1016px) {
    .sidebar {
    width: 80px;
    height: 100vh;
    background: #333;
    color: white;
    transition: width 0.5s;
    position: fixed;
    overflow: hidden;
    padding: 1em;
  
    background: rgba(51, 51, 51, 0.5);
  }
  .sidebar--open {
    width: 150px;
  }
  .toggle-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 20px;
    margin: 10px;
  }
  }
  </style>
  