<template>
    <Header/>
    <h2 class="fs-2 text-center" style="margin-top: 2em;">OUR COMMUNITY</h2>
    <div class="container_card">
      <div class="block_user" v-for="user in users"
        :key="user.id">
        <div class="block_card">
          <img :src="link_image" class="rounded-circle" alt="images-user">
          <h3 class="block_title">{{user.username}}</h3>
        </div>
      </div>
    </div>
    <Footer></Footer>
</template>

<script>
 import { RouterLink } from 'vue-router';
  import Header from '../components/header.vue';
  import Footer from '@/components/Footer.vue'
  import axios from 'axios'

  export default {
  components: { Header,Footer },
  data() {
    return {
      users: [],
      username: localStorage.getItem('username') || '',
      token: localStorage.getItem('token') || '',
      link_image:'https://png.pngtree.com/png-clipart/20231019/original/pngtree-user-profile-avatar-png-image_13369988.png'
    };
  },
  mounted(){
    if (this.token) {
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
    }
    this.fetchUser();
  },
  methods:{
    fetchUser() {
      axios.get(`users/`).then((response) => {
        this.users = response.data.results;
      }).catch((error) => {
        console.error('Erreur lors de la récupération des données : ', error);
      });
    },
  }
  }

</script>

<style>
    .block_card .block_title{
      font-size: 20px;
      font-weight: 400;
      text-align: center;
      margin-top: 1em
    }
    .block_card{
      width:200px;
      height: 300px;
    }
    .block_card img{
      margin: 0 auto;
      border-radius: 100%;
      width:100%;
      border-radius: 100% 100% 100% 100%;
      border: 2px solid rgb(183, 182, 182);
    }
    .container_card{
      margin:1em auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: end;
      padding: 1em;
      max-width: 1400px;
    }
    .block_user{
      width: 20%;
      height: 200px;
    }

    @media screen and (max-width:760px) {
      .container_card{
        margin:1em auto;
        display: block;
        padding: 1em;
        width: 100%;
        text-align: center;
        background-color: red;
      }
    }
</style>