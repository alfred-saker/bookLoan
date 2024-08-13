<template>
  <v-app>
    <v-container>
      <v-btn outlined class="mt-4 ml-4" :to="{ path: '/loanbook/admin/dashboard_book_admin' }">
        Go to the homepage <v-icon>mdi-arrow-right</v-icon>
      </v-btn>

      <v-alert v-if="success_register" type="success" dismissible>
        {{ success_register }}
      </v-alert>

      <v-card class="mx-auto my-12" max-width="400">
        <v-card-title class="text-center">
          Sign in to your account
        </v-card-title>
        <v-card-text>
          <v-alert v-if="errors.wrong_credentials" type="error">
            {{ errors.wrong_credentials }}
          </v-alert>
          <v-form @submit.prevent="submitForm">
            <v-text-field
              v-model="username"
              label="Username"
              variant="outlined"
              :error-messages="errors.username"
              outlined
              clearable
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              variant="outlined"
              type="password"
              :error-messages="errors.password"
              outlined
              clearable
            ></v-text-field>
            <v-btn outlined type="submit" color="primary" block>Sign in</v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <router-link to="/loanbook/register">
            Not a member? Register here
          </router-link>
        </v-card-actions>
      </v-card>
    </v-container>
    <!-- <Footer></Footer> -->
  </v-app>
</template>

<script>
import axios from 'axios';
import Footer from '@/components/Footer.vue';

export default {
  components: { Footer },
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      success_register: '',
      errors: {
        username: '',
        password: '',
        wrong_credentials: ''
      }
    };
  },
  created() {
    this.success_register = localStorage.getItem('success_register');
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
          const { token, username, id, url, is_staff } = response.data;

          localStorage.setItem('token', token);
          localStorage.setItem('username', username);
          localStorage.setItem('id', id);
          localStorage.setItem('url', url);
          localStorage.setItem('is_staff', is_staff);
          localStorage.setItem('success_login', 'Welcome in the universe of BookLoan 😎🥳');
          this.$router.push('/loanbook/admin/dashboard_book_admin');

        } catch (error) {
          if (error.response && error.response.data) {
            this.errors.wrong_credentials = "Invalid credentials";
          } else {
            this.errors.wrong_credentials = "An error occurred. Please try again.";
          }
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
};
</script>

<style scoped>
/* Ajoutez vos styles personnalisés ici */
</style>
