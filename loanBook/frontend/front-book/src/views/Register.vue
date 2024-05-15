<template>
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <!-- <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company"> -->
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      </div>
      <form action="" method="post">
        <div class="row col-12" style="line-height: 2;" id="form-register-user">
          <div class="col-6">
            <label for="">First Name</label>
            <input type="text" class="form-control" placeholder="First name" aria-label="first name" id="first_name" name="first_name">
          </div>
          <div class="col-6">
            <label for="">Last Name</label>
            <input type="text" class="form-control" placeholder="Last name" aria-label="last name" id="last_name" name="last_name">
          </div>
          <div class="col-6">
            <label for="">Username</label>
            <input type="text" class="form-control" placeholder="Username" aria-label="username" id="username" name="username">
          </div>
          <div class="col-6">
            <label for="">Email</label>
            <input type="email" class="form-control" placeholder="Email" aria-label="email" id="email" name="email">
          </div>
          <div class="col-6">
            <label for="">Password</label>
            <input type="password" class="form-control" placeholder="Enter a strong password" aria-label="password" id="password" name="password">
          </div>
          <div class="col-6">
            <label for="">Confirm password</label>
            <input type="password" class="form-control" placeholder="Please confirm password" aria-label="confirm password" id="cpassword" name="cpassword">
          </div>
          <div class="col-12">
            <button type="submit" class="btn btn-outline-primary" style="width: 100%;">Register now</button>
          </div>
        </div>
        <p class="mt-10 text-center text-sm text-gray-500">
          Are you already member? You can login <router-link to="/" class="font-semibold">here</router-link>
        </p>
      </form>
    </div>
    
    </template>

<style>
  #form-register-user{
    max-width: 600px;
    margin: 0 auto;
  }
  #form-register-user div{
    margin-top: 1em;
  }
</style>