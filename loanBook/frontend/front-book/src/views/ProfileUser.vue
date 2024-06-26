<template>
  <!-- Shine@2024 -->
    <Header></Header>
    <div class="container_user_profile">
      <div class="infos_user">
        <div class="info_user_img">
          <img :src="image_user" alt="" class="rounded-circle"> <br>
          <span class="mt-2">You are a member of the BookLoan community <strong class="fw-medium" v-if="is_staff === 'true'"><span class="fst-italic">(Administrator)</span><i class="bi bi-award"></i></strong></span>
          <h3 class="fs-3 mt-3">Borrows Books</h3>
          
          <div v-if="is_staff === 'false'">
            <ul class="mt-2" v-if="borrows">
              <li v-for="borrow in borrows" :key="borrow.id">
              
                <div class="info_borrow_user" v-if="borrow.status_borrow === true">
                  <p>{{ borrow.bookName }} <span class="fst-italic"> Borrowed on {{ borrow.borrow_date }}</span></p>
                  <p class="ml-1"><button @click="returnBorrowUser(borrow.books, borrow.id)" class="btn btn-outline-dark align-self-end">Return</button></p>
                </div>
              </li>
            </ul>
            <ul v-else>
              <div class="info_borrow_user">
                <p>Updated space. You have not added a loan recently.<router-link to="/loanbook/dashboard_book_admin"> <span class="fs-6 fw-bold text-decoration-underline">Views our book!</span> </router-link> </p>
              </div>
            </ul>
            <div>
              <h3 class="fs-3 mt-3">Borrowed books archive</h3>
              <ul class="mt-2" v-if="borrows">
                <li v-for="borrow in borrows" :key="borrow.id">
                  <div class="info_borrow_user" v-if="borrow.status_borrow === false">
                    <p>{{ borrow.bookName }} <span class="fst-italic"> Borrowed from {{ borrow.borrow_date }} to {{ borrow.return_date }}</span></p>
                  </div>
                  
                </li>
              </ul>
              <ul v-else>
                <div class="info_borrow_user">
                  <p>You haven't borrowed any books yet. Start the experience <router-link to="/loanbook/dashboard_book_admin"> <span class="fs-6 fw-bold text-decoration-underline">now!👉</span> </router-link></p>
                </div>
              </ul>
            </div>
          </div>
        </div>
        <div class="form_user">
          <h2 class="fs-2">Full information</h2>
          <form @submit.prevent="updateUser">
            
            <div class="row col-12" style="line-height: 2;">
              <div class="col-6">
                <label for="first_name">First Name</label>
                <input type="text" class="form-control" v-model="first_name" placeholder="First name" aria-label="first name" id="first_name" name="first_name">
                <small v-if="errors.first_name" style="color:red">{{errors.first_name}}</small>
              </div>
              <div class="col-6">
                <label for="last_name">Last Name</label>
                <input type="text" class="form-control" v-model="last_name" placeholder="Last name" aria-label="last name" id="last_name" name="last_name">
                <small v-if="errors.last_name" style="color:red">{{errors.last_name}}</small>

              </div>
              <div class="col-6">
                <label for="username">Username</label>
                <input type="text" class="form-control" v-model="username" placeholder="Username" aria-label="username" id="username" name="username">
                <small v-if="errors.username" style="color:red">{{errors.username}}</small>

              </div>
              <div class="col-6">
                <label for="email">Email</label>
                <input type="email" class="form-control" v-model="email" placeholder="Email" aria-label="email" id="email" name="email">
                <small v-if="errors.email" style="color:red">{{errors.email}}</small>

              </div>
              <div class="col-3">
                <button type="submit" class="btn btn-outline-primary" style="width: 100%; margin-top: 1em;">Update now</button>
              </div>
            </div>
          </form>
          <form @submit.prevent="changePassword">
        
            <div class="row col-12" style="line-height: 2;">
              <h2 class="fs-2">Section password information</h2>
              <div v-if="errors.wrong_credentials" class="alert alert-danger">{{ errors.wrong_credentials }}</div>
              <div class="col-6">
                <label for="password">Old Password</label>
                <input type="password" class="form-control" v-model="old_password" placeholder="Enter a strong password" aria-label="password" id="oldpassword" name="password">
                <small v-if="errors.old_password" style="color:red">{{errors.old_password}}</small>
              </div>
              <div class="col-6">
                <label for="password">New Password</label>
                <input type="password" class="form-control" v-model="password" placeholder="Enter a strong password" aria-label="password" id="newpassword" name="password">
                <small v-if="errors.password" style="color:red">{{errors.password}}</small>
              </div>
              <div class="col-12">
                <label for="confirm_password">Confirm a new password</label>
                <input type="password" class="form-control" v-model="confirm_password" placeholder="Enter a confirm password" aria-label="confirm_password">
                <small v-if="errors.confirm_password" style="color:red">{{errors.confirm_password}}</small>
              </div>
              <div class="col-6">
                <button type="submit" class="btn btn-outline-primary" style="width: auto; margin-top: 1em;">Change password</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </template>
  

<script>
  import axios from 'axios';
  import { RouterLink } from 'vue-router'
  import Header from '../components/header.vue'
  import Footer from '@/components/Footer.vue'
  import { useToast } from "vue-toastification";
  export default {
    components: {
      Header,
      Footer
    },
    setup() {
   // Get toast interface
      const toast = useToast();

      // Make it available inside methods
      return { toast }
    },
    data() {
      return {
        image_user: 'https://www.shareicon.net/data/512x512/2016/05/24/770137_man_512x512.png',
        borrows: [], // Ajouter un tableau pour stocker les emprunts
        user_id: '',
        is_staff:localStorage.getItem('is_staff'),
        user_data: '',
        first_name: '',
        last_name: '',
        username: '',
        email: '',
        password: '',
        old_password:'',
        confirm_password: '',
        wrong_credentials:'',
        errors:{
          first_name: '',
          last_name: '',
          username: '',
          email: '',
          password: '',
          old_password:'',
          confirm_password: '',
          wrong_credentials:''
        },
      };
    },
    created() {
      this.user_id = this.extractUserId(localStorage.getItem('url'));
      this.fetchUserDetails();
      this.fetchUserBorrows();
      // this.returnBorrowUser()
    },
    methods: {
      returnBorrowUser(book_id_borrow, borrow_id){
        const book_id_borrow_user = this.extractUserId(book_id_borrow);
        axios.patch(`emprunts/${borrow_id}/`, {
          status_borrow: false
        }, {
          headers: {
            'Authorization': `token ${localStorage.getItem('token')}`
          }
        }).then(() => {
          console.log("Status_borrow updated successfully.");
          // mettre à jour le statut du livre correspondant
          axios.get(`books/${book_id_borrow_user}/`).then((response)=>{
            let borrow_count = response.data.borrow_count
            console.log(borrow_count);
            console.log(book_id_borrow_user);
            axios.patch(`books/${book_id_borrow_user}/`, {
                status_book: false,
                borrow_count:borrow_count + 1
            }, {
                headers: {
                  'Authorization': `token ${localStorage.getItem('token')}`
                }
            }).then(() => {
              console.log("Status_book updated successfully.");
              setTimeout(() => {
              window.location.reload();
              }, 5000);

            this.toast.success('Thanks for the book review');
          })
          }).catch((error) => {
            console.error("Error updating status_book:", error);
          });
        }).catch((error) => {
          console.error("Error updating status_borrow:", error);
        });
      },

      fetchUserDetails() {
        axios.get(`users/${this.user_id}/`, 
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        }).then((response) => {
          this.user_data = response.data;
          this.first_name = response.data.first_name;
          this.last_name = response.data.last_name;
          this.username = response.data.username;
          this.email = response.data.email;
        }).catch((error) => {
          if (error.response && error.response.status === 404) {
            console.error('Utilisateur non trouvé.');
          } else {
            console.error('Erreur lors de la récupération des détails de l\'utilisateur : ', error);
          }
        });
        
      },
      async updateUser() {
        this.clearErrors();
        if (this.isValidFormUser()) {
          try {
            const response = await axios.patch(`users/${this.user_id}/`, {
              first_name: this.first_name,
              last_name: this.last_name,
              username: this.username,
              email: this.email,
            }, {
              headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`,
              }
            });
            this.toast.success("Profile updated successfully!");
          } catch (error) {
            if (error.response && error.response.data) {
              this.errors = error.response.data;
            } else {
              console.error('Error:', error);
            }
          }
        }
      },
      validatePassword(password) { 
        const passwordRegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/; 
        if(passwordRegExp.test(password)){
          return true
        }
        else{
          return false
        }
      } ,
      async changePassword() {
        this.clearErrors();

        if (this.isValidFormPassword()) {
          
          try {

            // je verifie si le mot de passe est bien valide:

            if(!this.validatePassword(this.password)){
              this.errors.password = 'The password must contain at least 8 characters, including upper and lower case letters, numbers and special characters.'
              return
            }
            // SplinterCrown@17
            if (this.password !== this.confirm_password) {
              this.errors.confirm_password = "Passwords do not match!";
              return;
            }
            const response = await axios.patch(`users/${this.user_id}/change_password/`, {
              old_password: this.old_password,
              new_password: this.password,
              confirm_password: this.confirm_password,
            },{
              headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`,
              }
            })
            this.toast.success("Password changed successfully!");
          } catch (error) {
            if (error.response && error.response.data) {
              this.errors = error.response.data;
              this.errors.wrong_credentials = "Please check that you have entered the correct password."
              console.log(this.errors);
            } else {
              console.error('Error:', error);
            }
          }
        }
      },
      async fetchUserBorrows() {
        try {
          const response = await axios.get(`emprunts/`, {
            headers: {
              'Authorization': `Token ${localStorage.getItem('token')}`
            }
          });
          
          // Parcourir chaque emprunt pour obtenir les détails des livres
          for (const borrow of response.data.results) {
            // Obtenir l'URL du livre à partir de l'emprunt
            const bookUrl = borrow.books;

            // Effectuer une requête GET pour obtenir les détails du livre
            const bookResponse = await axios.get(bookUrl, {
              headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`
              }
            });

            // Ajouter le nom du livre à l'objet d'emprunt
            borrow.bookName = bookResponse.data.title;
          }

          // Mettre à jour la liste des emprunts avec les noms des livres
          this.borrows = response.data.results;
          
          console.log(this.borrows);
        } catch (error) {
          if (error.response && error.response.status === 404) {
            console.error('Emprunts non trouvés.');
          } else {
            console.error('Erreur lors de la récupération des emprunts : ', error);
          }
        }
      },
      extractUserId(url) {
        if (url) {
          const segments = url.split('/');
          return segments[segments.length - 2]; // L'avant-dernier segment contient l'ID de l'utilisateur
        }
      },
      isValidFormUser() {
        let valid = true;
        if (!this.first_name) {
          this.errors.first_name = "Please enter your first name";
          valid = false;
        }
        if (!this.last_name) {
          this.errors.last_name = "Please enter your last name";
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
        return valid;
      },
      isValidFormPassword() {
        let valid = true;
        if (!this.password) {
          this.errors.password = "Please enter your new password";
          valid = false;
        }
        if (!this.old_password) {
          this.errors.old_password = "Please enter your old password";
          valid = false;
        }
        if (!this.confirm_password) {
          this.errors.confirm_password = "Please enter your confirmation password";
          valid = false;
        }
        return valid;
      },
      clearErrors() {
        this.errors.first_name = '';
        this.errors.last_name = '';
        this.errors.email = '';
        this.errors.username = '';
        this.errors.password = '',
        this.errors.old_password = '',
        this.errors.confirm_password = '',
        this.errors.wrong_credentials = '';
      }
    }
  };
  </script>
  


<style>
.infos_user{
    display: flex;
    justify-content: space-around;
    margin-top: 2em;
    
}
.form_user{
  max-width: 600px;
}

.info_user_img img{
  width: 200px;
  height: 200px;
  text-align: center;
  margin:0 auto;
  
}
.form_user form{
    margin-top: 2em;
}
.info_borrow_user{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px;
}
</style>