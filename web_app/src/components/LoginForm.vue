<template>
  <div class="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-16 w-auto" src="https://firebasestorage.googleapis.com/v0/b/vue-upload-images-bfc36.appspot.com/o/website_assets%2Fsmart%20mirror_200x200.png?alt=media&token=ae740e33-be78-4b17-ad2f-e8104cf4eb84" alt="Your Company" />
      <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Login in to your account</h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4  sm:rounded-lg sm:px-10">
        <form class="space-y-6" v-on:submit.prevent='login_Fun'>
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <div class="mt-1">
              <input v-model="email" id="email" name="email" type="email" autocomplete="email" required="" class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="mt-1">
              <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required="" class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <button  type="submit" class="flex w-full justify-center rounded-md border border-transparent bg-green-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">Sign in</button>
          </div>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <a v-on:click='go_to_registration' href="#" class="bg-white px-2 text-gray-500">Create New Account, Click here</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>

export default {
    data(){
      return{
        email  : '' ,
        password : '',
       
      }
    },
    methods:{
      login_Fun(){
        this.$emit('login_form_data_child' , {
          'request_type' : 'login' ,
          'email' : this.email , 
          'password' : this.password

          })
      },
      go_to_registration(){
        this.email = ''
        this.password = ''
        this.$emit('login_form_data_child' , {
          'request_type' : 'got_to_registeration' ,
        })
      }
    }
}
</script>

<style>

</style>