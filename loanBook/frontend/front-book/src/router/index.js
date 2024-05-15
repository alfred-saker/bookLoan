import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AddBook from '@/views/AddBook.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import BookDetails from '@/views/BookDetails.vue'
import AddBorrow from '@/views/AddBorrow.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/',
      name: 'login',
      component: Login
    },

    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/add_book',
      name: 'add_book',
      component: AddBook
    },
    {
      path: '/detail_book/:book_id',
      name: 'detail_book',
      component: BookDetails
    },
    {
      path:'/add_borrow/:book_id?',
      name:'add_borrow',
      component:AddBorrow
    }
  ]
})

export default router
