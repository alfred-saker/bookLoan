import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AddBook from '@/views/AddBook.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import BookDetails from '@/views/BookDetails.vue'
import ProfileUser from '@/views/ProfileUser.vue'
import AboutUs from '@/views/AboutUs.vue'
import User from '@/views/User.vue'
import ChartVue from '@/views/ChartVue.vue'
import { isAuthenticated } from '@/auth.js'

import Dashboard_book_admin from '../views/Dashboard_book_admin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Unprotected router
    {
      path: '/loanbook/home',
      name: 'home',
      component: Home
    },
    {
      path: '/loanbook/admin/dashboard_book_admin',
      name: 'dashboard_book_admin',
      component: Dashboard_book_admin,
      meta:{
        needAuth:true
      }
    },
    {
      path:'/loanbook/about_us',
      name:'about_us',
      component:AboutUs
    },
    {
      path: '/loanbook/login',
      name: 'login',
      component: Login
    },

    {
      path: '/loanbook/register',
      name: 'register',
      component: Register
    },
    {
      path:'/loanbook/user',
      name:'user',
      component:User,
    },
    {
      path: '/loanbook/books/detail_book/:book_id',
      name: 'detail_book',
      component: BookDetails
    },

    // Protected router
    {
      path: '/loanbook/books/add_book',
      name: 'add_book',
      component: AddBook,
      meta:{
        needAuth:true
      }
    },
    {
      path:'/loanbook/user/profile',
      name:'profiile_user',
      component:ProfileUser,
      meta:{
        needAuth:true
      }
    },
    {
      path:'/loanbook/statitic_book',
      name:'statitic_book',
      component:ChartVue,
      meta:{
        needAuth:true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.needAuth && !isAuthenticated()) {
    next({
      path: '/loanbook/login',
      query: { redirect: to.fullPath }  // Vous pouvez ajouter une redirection après login ici
    });
  } else {
    next();
  }
});
export default router
