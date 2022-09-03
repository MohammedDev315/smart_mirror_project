<template>
  <login-form v-if = 'selected_page == "login" '  v-on:login_form_data_child = 'check_data_comming'></login-form>
  <register-from v-if  = 'selected_page == "registeration" '   v-on:registeration_form_data_child = 'check_data_comming'    ></register-from>
  <!---------------->
  <div v-if='alert_type == "success" ' class="rounded-md bg-green-100 p-4 w-96 m-auto">
    <h3 class="text-sm font-medium text-green-800">{{alert_message}}</h3>
  </div>
  <div v-if='alert_type == "danger" ' class="rounded-md bg-red-50 p-4 w-96 m-auto">
    <h3 class="text-sm font-medium text-red-800">{{alert_message}}</h3>
  </div>


</template>

<script>
import LoginForm from '../components/LoginForm.vue'
import RegisterFrom from '../components/RegisterForm.vue'
// import { XCircleIcon } from '@heroicons/vue/20/solid'
const axios = require('axios');

export default {
    components:{
        LoginForm,
        RegisterFrom
    },
    data(){
        return{
            selected_page : 'login',
            show_alert_box : null,
            alert_message : null,
            alert_type : null
        }
    },
    methods:{
        alert_box_fun(response , changed_page){
            if (response['request']['status'] == 'success' ){
                this.show_alert_box = true
                this.alert_message = response['request']['message']
                this.alert_type = 'success'
                console.log(changed_page)
                this.selected_page = changed_page
            }else{
                this.show_alert_box = true
                this.alert_message = response['request']['message']
                this.alert_type = 'danger'
            }
        },

        // ==============================
        login_function(data_in){
            const user_login = {
                "email": data_in['email'],
                "password": data_in['password']
            }
            axios.post('http://192.168.8.188:5006/user_log_in' , user_login)
            .then((res)=> this.alert_box_fun(res.data, 'show_user_data'))
            .catch((err) => console.log(err) )
        },//End login

        // ==============================
        registration_function(data_in){
            const user_login = {
                "fullname" : data_in['fullname'],
                "email": data_in['email'],
                "password": data_in['password']
            }
            axios.post('http://192.168.8.188:5006/create_user' , user_login)
            .then((res)=> this.alert_box_fun(res.data , 'login'))
            .catch((err) => console.log(err) )
        }, //End Registration

        // =============================
        call_saved_data_fuction(){}, //End call data



        // -------------------------------
        // Receve all type of request from three components(three children)
        // first if loging, call login function and pass necessary data
        // second registration...etc, third chick storage for current login
        // -------------------------------
        check_data_comming(value){
            console.log(value['request_type'])
            
            if (value['request_type'] == 'got_to_registeration'){
                this.selected_page = 'registeration'
                console.log('registeration')
            }//end registartion

            if (value['request_type'] == 'login'){
                console.log('log in')
                this.login_function(value)
            }//end login

            if (value['request_type'] == 'registeration'){
                console.log('registeration')
                this.registration_function(value)
            }//end login

            if (value['request_type'] == 'got_to_login'){
                console.log('log in')
                this.selected_page = 'login'
            }//end login




        }
    }

}
</script>

<style>

</style>