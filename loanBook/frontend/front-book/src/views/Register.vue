<template>
  <v-app>
    <v-container>
      <v-btn outlined class="mt-4 ml-4" :to="{ path: '/loanbook/admin/dashboard_book_admin' }">
        Go to the homepage <v-icon>mdi-arrow-right</v-icon>
      </v-btn>

      <v-row class="d-flex justify-center">
        <v-col cols="12" md="8" lg="7">
          <v-card class="mt-4">
            <v-card-title class="text-center">
              Register your account
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="AddUser">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="first_name"
                      variant="outlined"
                      label="First Name"
                      :error-messages="errors.first_name"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="last_name"
                      variant="outlined"
                      label="Last Name"
                      :error-messages="errors.last_name"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="username"
                      variant="outlined"
                      label="Username"
                      :error-messages="errors.username"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="email"
                      variant="outlined"
                      label="Email"
                      :error-messages="errors.email"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="password"
                      label="Password"
                      variant="outlined"
                      type="password"
                      :error-messages="errors.password"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="confirm_password"
                      label="Confirm Password"
                      variant="outlined"
                      type="password"
                      :error-messages="errors.confirm_password"
                      outlined
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-btn type="submit" color="primary" block>Register now</v-btn>
                  </v-col>
                </v-row>
              </v-form>
              <p class="mt-10 text-center text-sm text-gray-500">
                Are you already a member? You can login 
                <router-link to="/loanbook/login" class="font-semibold">here</router-link>
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <!-- <Footer></Footer> -->
    </v-container>
  </v-app>
</template>



<script>
  import axios from 'axios';
  import { toHandlers } from 'vue';
  import { useRoute } from 'vue-router';
  import Footer from '@/components/Footer.vue'

  export default {
    components:{Footer},
    name:'Register',
    data() {
      return {
        first_name:'',
        last_name:'',
        email:'',
        username: '',
        password: '',
        confirm_password:'',
        errors:{
          first_name:'',
          last_name:'',
          email:'',
          username: '',
          password: '',
          confirm_password:'',
          wrong_crendentials : ""
        }
      }
    },
  methods: {
    validatePassword(password) { 
      const passwordRegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/; 
      if(passwordRegExp.test(password)){
        return true
      }
      else{
        return false
      }
    },
    async AddUser() {
      this.clearErrors();
      if (this.isValidForm()) {
        try {
          const response = await axios.post('users/', {
            first_name:this.first_name,
            last_name:this.last_name,
            email:this.email,
            username: this.username,
            password: this.password,
            confirm_password:this.confirm_password
          });
          localStorage.setItem('success_register', 'Your account is created, now log in to drive into the world of BookLoan🥳🥳🥳');
          this.$router.push('/loanbook/login');

        } catch (error) {
          if (error.response && error.response.data) {
            const responseData = error.response.data;
            if (responseData.password) {
              this.errors.password = responseData.password[0];
            }
            if (responseData.username) {
              this.errors.username = responseData.username[0];
            }
            if (responseData.email) {
              this.errors.email = responseData.email[0];
            }
            // Autres erreurs de validation à gérer
          } else {
            this.errors.server_error = "An error occurred. Please try again.";
          }
          console.error('Error:', error.response ? error.response.data : error);
        }
      }
    },
    isValidForm() {
      let valid = true;
      if (!this.first_name) {
        this.errors.first_name = "Please enter your first_name";
        valid = false;
      }
      if (!this.last_name) {
        this.errors.last_name = "Please enter your last_name";
        valid = false;
      }
      if (!this.email) {
        this.errors.email = "Please enter your email";
        valid = false;
      }
      if (!this.username) {
        this.errors.username = "Please enter your username";
        valid = false;
      }
      if (!this.password) {
        this.errors.password = "Please enter your password";
        valid = false;
      }
      if (!this.confirm_password) {
        this.errors.confirm_password = "Please enter your confirm password";
        valid = false;
      }
      if(!this.validatePassword(this.password)){
        this.errors.password = 'The password must contain at least 8 characters, including upper and lower case letters, numbers and special characters.'
        valid = false;
      }
      if (this.password !== this.confirm_password) {
        this.errors.confirm_password = "Passwords do not match";
        valid = false;
      }
      // SplinterCrown@17
      return valid;
    },
    clearErrors() {
      this.errors.first_name = '';
      this.errors.last_name = '';
      this.errors.email = '';
      this.errors.username = '';
      this.errors.password = '';
      this.errors.confirm_password = '';
      this.errors.wrong_credentials = '';
    }
  }
}
</script>

<style>

</style>