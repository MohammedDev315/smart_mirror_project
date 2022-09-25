import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './tailwind.css'
import { initializeApp } from "firebase/app";

const firebaseConfig = {
    apiKey: "AIzaSyC3dXWEkv2A3aeoqI0va5YycLKxCrpdjGU",
    authDomain: "vue-upload-images-bfc36.firebaseapp.com",
    projectId: "vue-upload-images-bfc36",
    storageBucket: "vue-upload-images-bfc36.appspot.com",
    messagingSenderId: "674827339045",
    appId: "1:674827339045:web:935edab8f1c4701f9306cc",
    measurementId: "G-4WZRS4RYMZ"
  };
  initializeApp(firebaseConfig);


createApp(App).use(store).use(router).mount('#app')
