<template>
    <div class="login-wrapper border border-light">
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
            Namn (synligt för andra användare)
            </label> 
            <br/>

            <input v-model="name" type="name" id="inputName"
            class="form-control" placeholder="Namn" required> 
            <br/>
            </section> 

            <section>
            <label for="inputGroupnum" class="sr-only">
            Gruppnummer
            </label> 
            <br/>

            <input v-model="groupnum" type="groupnum" id="inputGroupnum"
            class="form-control" placeholder="Gruppnummer" required> 
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
</template>

<script>
export default {
    name: 'CreateAccount',
    data: function(){
        return {
            username: '',
            password:'',
            groupnum:'',
            name:''
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
            console.log("groupnum:", this.groupnum);
            console.log("name:", this.name);
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
                'groupnum': app.groupnum,
                'name': app.groupnum
            }));
            console.log("Create user sent.");
            /* eslint-enable no-console */
        }
    }
}
</script>

<style scoped>
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

</style>