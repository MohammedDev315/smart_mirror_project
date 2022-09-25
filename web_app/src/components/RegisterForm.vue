<template>
  <div class="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-16 w-auto" src="https://firebasestorage.googleapis.com/v0/b/vue-upload-images-bfc36.appspot.com/o/website_assets%2Fsmart%20mirror_200x200.png?alt=media&token=ae740e33-be78-4b17-ad2f-e8104cf4eb84" alt="Your Company" />
      <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Create New Account</h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4  sm:rounded-lg sm:px-10">
        <form class="space-y-6" v-on:submit.prevent='registreation_fun'>
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
            <div class="mt-1">
              <input v-model="name" id="name" name="name" type="text" required="" class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm" />
            </div>
          </div>          <div>
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
            <label for="re_password" class="block text-sm font-medium text-gray-700">Re Password</label>
            <div class="mt-1">
              <input v-model="re_password" id="re_password" name="re_password" type="password" autocomplete="current-password" required="" class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm" />
            </div>
          </div>

          <div >
            <p>{{progressing}}</p>
            <!-- <button @click="click1">choose a photo</button> -->
            <input type="file" ref="input1"
            @change="previewImage" accept="image/*" >                
          </div>
          <p class="text-red-500" v-if = 'show_error'>{{error_message}}</p>
          <div>
            <button  type="submit" class="flex w-full justify-center rounded-md border border-transparent bg-green-500 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2">Create Account</button>
          </div>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <a v-on:click='go_to_login' href="#" class="bg-white px-2 text-gray-500">Cancel, Click here</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>

import { getStorage, ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";


// -------extract image name------------
function resizedName (fileName, dimensions = '200x200') {
  const extIndex = fileName.lastIndexOf('.');
  const ext = fileName.substring(extIndex);
  return `${fileName.substring(0, extIndex)}_${dimensions}${ext}`;
}


export default {
    data(){
      return{
        show_error : false ,
        error_message : '' ,
        name  : '' ,
        email  : '' ,
        password : '',
        re_password : '',
        progressing : '',
        imageData: null , 
        url_text : ''
      }
    },
    // -----Send data to parant and then to database----------
    methods:{
      registreation_fun(){
        if(this.imageData == null){
          this.error_message = 'Missing upload image'
          this.show_error = true
          console.log('empyt iamge')
        }
        else if (this.password != this.re_password) {
          alert('Passwor are not same')
        }else{
        this.$emit('registeration_form_data_child' , {
          'request_type' : 'registeration' ,
          'fullname' : this.name,
          'email' : this.email , 
          'password' : this.password ,
          'user_image_url' : this.url_text
          })}
      },
      // -------------Cancel---------------
      go_to_login(){
        this.$emit('registeration_form_data_child' , {
          'request_type' : 'got_to_login' ,
        })
      },

      // ------------Upload image----------------



    previewImage(event) {
      this.imageData = event.target.files[0];
      const storage = getStorage();
      const storageRef = ref(storage, this.imageData.name);

      // ----Upload the file and metadata
      const uploadTask = uploadBytesResumable(storageRef, this.imageData);
      
      // ---Start tracking porgress------
      uploadTask.on('state_changed', 
        (snapshot) => {
          // Observe state change events such as progress, pause, and resume
          // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
          const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          console.log('Upload is ' + progress + '% done');
          this.progressing = 'Upload is ' + progress + '% done';
          switch (snapshot.state) {
            case 'paused':
              console.log('Upload is paused');
              break;
            case 'running':
              console.log('Upload is running');
              break;
          }
        }, 
        (error) => {
            console.log(error)
        }, 
        () => {

          this.progressing = 'Upload in porgress'
          setTimeout(() => {
            // const storage = getStorage();
            getDownloadURL(ref(storage, resizedName(this.imageData.name) ))
              .then((url) => {
                console.log(url)
                this.url_text = url
                this.progressing = 'Upload Done'
              })
              .catch((error) => {
                console.log(error)
                this.progressing = 'Error, please try again'
              });//=====
           }, 10000);
          
        }//Then fun
      );//uploadTaskEnd







    }//End previewImage





    }//===
}
</script>
