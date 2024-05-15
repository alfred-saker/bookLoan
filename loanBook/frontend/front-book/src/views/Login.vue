<template>
<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-sm">
    <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
  </div>

  <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
    <form class="space-y-6" @submit.prevent="submitForm">
      <p v-if="errors.wrong_crendentials">{{ errors.wrong_crendentials }}</p>
      <div>
        <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
        <div class="mt-2">
          <input v-model="username" id="username" name="username" type="text" autocomplete="username" class="form-control">
          <small v-if="errors.username" class="text-danger">{{ errors.username }}</small>
        </div>
      </div>

      <div>
        <div class="flex items-center justify-between">
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          <div class="text-sm">
            <a href="#" class="font-semibold">Forgot password?</a>
          </div>
        </div>
        <div class="mt-2">
          <input v-model="password"  id="password" name="password" type="password" autocomplete="current-password" class="form-control">
          <small v-if="errors.password" class="text-danger">{{ errors.password }}</small>
        </div>
      </div>

      <div>
        <button type="submit" class="btn btn-outline-primary" style="width: 100%;">Sign in</button>
      </div>
    </form>

    <p class="mt-10 text-center text-sm text-gray-500">
      Not a member? You can register 
      <router-link to="/register" class="font-semibold">here</router-link>
    </p>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import { toHandlers } from 'vue';
import { useRoute } from 'vue-router';

  export default {

    name:'Login',
    data() {
      return {
        username: '',
        password: '',
        errors:{
          username : "",
          password : "",
          wrong_crendentials : ""
        }
      }
    },
  methods: {
    async submitForm() {
      this.clearErrors();
      if (this.isValidForm()) {
        try {
          const response = await axios.post('login/', {
            username: this.username,
            password: this.password
          });
          console.log(response.data);
          const { token, username, id,url,is_staff} = response.data;
          console.log(token);
          console.log(username);
          console.log(id);
          console.log(url);
          console.log(is_staff);

          localStorage.setItem('token', token);
          localStorage.setItem('username', username);
          localStorage.setItem('id', id);
          localStorage.setItem('url', url);
          localStorage.setItem('is_staff', is_staff);
          this.$router.push('home');

        } catch (error) {
          if (error.response && error.response.data) {
            this.errors.wrong_credentials = "Invalid credentials";
          }
          console.error('Error:', error.response ? error.response.data : error);
        }
      }
    },
    isValidForm() {
      let valid = true;
      if (!this.username) {
        this.errors.username = "Please enter your username";
        valid = false;
      }
      if (!this.password) {
        this.errors.password = "Please enter your password";
        valid = false;
      }
      return valid;
    },
    clearErrors() {
      this.errors.username = '';
      this.errors.password = '';
      this.errors.wrong_credentials = '';
    }
  }
}
</script>