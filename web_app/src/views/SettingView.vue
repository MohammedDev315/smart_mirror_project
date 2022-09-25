<template>
  <login-form v-if = 'selected_page == "login" '  v-on:login_form_data_child = 'check_data_comming'></login-form>
  <register-from v-if  = 'selected_page == "registeration" '   v-on:registeration_form_data_child = 'check_data_comming'    ></register-from>
  <user-profile v-if = 'selected_page == "user_profile" ' v-on:user_profile = 'check_data_comming'  ></user-profile>
  <!---------------->
  <div v-if='alert_type == "success" ' class=" mb-9 rounded-md bg-green-100 p-4 w-96 m-auto">
    <h3 class="text-sm font-medium text-green-800">{{alert_message}}</h3>
  </div>
  <div v-if='alert_type == "danger" ' class=" mb-9 rounded-md bg-red-50 p-4 w-96 m-auto">
    <h3 class="text-sm font-medium text-red-800">{{alert_message}}</h3>
  </div>


</template>

<script>
import LoginForm from '../components/LoginForm.vue'
import RegisterFrom from '../components/RegisterForm.vue'
import UserProfile from '../components/UserProfile.vue'
// import { XCircleIcon } from '@heroicons/vue/20/solid'
const axios = require('axios');

export default {
    components:{
        LoginForm,
        RegisterFrom,
        UserProfile
    },
    data(){
        return{
            selected_page : 'user_profile',
            alert_message : null,
            alert_type : null
        }
    },
    methods:{
        alert_box_fun(response , changed_page , next_fun){
            if (response['request']['status'] == 'success' ){
                this.alert_message = response['request']['message']
                this.alert_type = 'success'
                this.selected_page = changed_page
                if( next_fun == 'save_user_data_onLocalStorge'){
                    this.save_user_data_onLocalStorge(response)
                    this.alert_type = null
                }
            }else{
                this.alert_message = response['request']['message']
                this.alert_type = 'danger'
            }
        },
        save_user_data_onLocalStorge(data_in){
            localStorage.uid = data_in.data['uid']
            localStorage.u_fullname = data_in.data['fullname']
            localStorage.u_email = data_in.data['email']
            localStorage.u_image_url = data_in.data['user_image_url']
        },

        // ==============================
        login_function(data_in){
            const user_login = {
                "email": data_in['email'],
                "password": data_in['password']
            }
            axios.post('http://192.168.8.181:5006/user_log_in' , user_login)
            .then((res)=> this.alert_box_fun(res.data, 'user_profile' , 'save_user_data_onLocalStorge'))
            .catch((err) => console.log(err) )
        },//End login

        // ==============================
        registration_function(data_in){
            const user_login = {
                "fullname" : data_in['fullname'],
                "email": data_in['email'],
                "password": data_in['password'],
                "user_image_url" : data_in['user_image_url']
            }
            axios.post('http://192.168.8.181:5006/create_user' , user_login)
            .then((res)=> this.alert_box_fun(res.data , 'login'))
            .catch((err) => console.log(err) )
        }, //End Registration

        // =============================
        call_saved_data_fuction(){}, //End call data

        // =============================
        log_out_fun(){
            console.log('logout')
        },

        // -------------------------------
        // Receve all type of request from three components(three children)
        // first if loging, call login function and pass necessary data
        // second registration...etc, third chick storage for current login
        // -------------------------------
        check_data_comming(value){
            
            
            if (value['request_type'] == 'got_to_registeration'){
                this.selected_page = 'registeration'
            }//end registartion

            if (value['request_type'] == 'login'){
                this.login_function(value)
            }//end 

            if (value['request_type'] == 'registeration'){
                this.registration_function(value)
            }//end 

            if (value['request_type'] == 'got_to_login'){
                this.selected_page = 'login'
            }//end 

            if (value['request_type'] == 'logout'){
                this.selected_page = 'login'
            }//end 

        }
    }, //MethodEnd
    created(){
        if (localStorage.uid){
            this.selected_page = 'user_profile'
        }else{
            this.selected_page = 'login'
        }
    }

}
</script>

<style>

</style>