<template>
    <div id="background" class="login-wrapper border border-light">
        <div id="createuser" class="login-wrapper border border-light">
            <img alt="MRP Logo" src="../assets/logo.png">
            <form class="form-signin"
            @submit.prevent="createAccount">
                <h2 class="form-signin-heading">
                Skapa nytt konto
                </h2>

                <section>
                <label for="inputUsername" class="sr-only"> Användarnamn 
                </label> 
                <br/>

                <input v-model="username" type="username" id="inputUsername" class="form-control" placeholder="Användarnamn" required autgofocus>
                </section>

                <section>
                <label for="inputPassword" class="sr-only">
                Lösenord
                </label> 
                <br/>

                <input v-model="password" type="password" id="inputPassword"
                class="form-control" placeholder="Lösenord" required> 
                <br/>
                </section> 

                <section>
                <label for="inputName" class="sr-only">
                Fullständigt Namn 
                </label> 
                <br/>

                <input v-model="name" type="name" id="inputName"
                class="form-control" placeholder="Namn" required> 
                <br/>
                </section> 

                <section>
                <label for="inputGroupname" class="sr-only">
                Gruppnamn
                </label> 
                <br/>

                <input v-model="groupname" type="groupname" id="inputGroupname"
                class="form-control" placeholder="Grupp" required> 
                <br/>
                </section> 

                <!--
                <button class="btn btn-lg btn-primary btn-block" type="submit" @release="createAccount">
                Sign in
                </button> -->

                
                <button class="btn btn-lg btn-primary btn-block" type="button" @click="createUser">
                Skapa
                </button>
                
                <button class="btn btn-lg btn-primary btn-block" type="button" @click="routeLogin">
                Tillbaka till inloggningssidan
                </button>

            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreateAccount',
    data: function(){
        return {
            username: '',
            password:'',
            groupname:'',
            name:'',
        }
    },
    methods: {
        routeLogin: function(){
            this.$router.replace('/');
        },
        createUser: function(){
            /* eslint-disable no-console */
            console.log("username:", this.username);
            console.log("pw:", this.password);
            console.log("group:", this.groupname);
            /* eslint-enable no-console */

            let app = this;
            
            var heroku_uri = 
                "https://heroku-mrp-backend.herokuapp.com/connect/register/";
            var local_uri = 
                "https://" + window.location.hostname + ":9000/connect/register/";

            if(process.env.NODE_ENV == "production")
                var uri = heroku_uri
            else 
                uri = local_uri

            var createUserRequest = new XMLHttpRequest();
            createUserRequest.onreadystatechange = function() {
                // TODO: Redirect to main page after success
                if (this.readyState == 4 && this.status == 200) {
                    alert(this.response);
                    app.$router.replace('/')
                }
                else if (this.readyState == 4 && this.status != 200){
                    alert(this.response);
                }
                /* eslint-disable no-console */
                console.log(this)
                /* eslint-enable no-console */
            };
            createUserRequest.open("POST", uri);
            createUserRequest.setRequestHeader(
                "Content-Type", "application/json;charset=UTF-8"
            );
            /* eslint-disable no-console */
            console.log("Sending create user.");
            createUserRequest.send(JSON.stringify({
                'username': app.username,
                'password': app.password,
                'groupname': app.groupname,
                'name' :    app.name,
            }));
            console.log("Create user sent.");
            /* eslint-enable no-console */
        }
    }
}
</script>

<style scoped>
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 300px;
}

h2 {
    color: #4a86e8;
    font-weight: bold;
    font-size: 150%;
}

section {
    padding: 10px;
}

label {
    font-size: 100%;
    color: #4a86e8;
}

button {
    margin: 10px;
    font-size: 100%;
    border-radius: 30px 10px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    padding-bottom: 5px;
    border: 2px solid #4a86e8;
}

input {
    font-size: 100%;
    margin: 1px;
    padding: 5px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 30px 10px;
    border: 1px solid #4a86e8;
}

#background {
    height: 95vh;
    border-top: 1px solid rgba(0, 0, 0, 0);
    background-size: cover;
    background-repeat: no-repeat;
    background-image: url("../assets/background.png");
}

#createuser {
    margin-top: 5%;
}

</style>