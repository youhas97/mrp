<template>
    <div class="login-wrapper border border-light">
        <img alt="MRP Logo" src="../assets/logo.png">
        <form class="form-signin"
        @submit.prevent="createAccount">
            <h2 class="form-signin-heading">
            Create an account
            </h2>

            <section>
            <label for="inputUsername" class="sr-only"> Username 
            </label> 
            <br/>

            <input v-model="username" type="username" id="inputUsername" class="form-control" placeholder="Username" required autgofocus>
            </section>

            <section>
            <label for="inputPassword" class="sr-only">
            Password
            </label> 
            <br/>

            <input v-model="password" type="password" id="inputPassword"
            class="form-control" placeholder="Password" required> 
            <br/>
            </section> 

            <section>
            <label for="inputName" class="sr-only">
            Name (What other users see)
            </label> 
            <br/>

            <input v-model="name" type="name" id="inputName"
            class="form-control" placeholder="Name" required> 
            <br/>
            </section> 

            <section>
            <label for="inputGroupnum" class="sr-only">
            Group Number
            </label> 
            <br/>

            <input v-model="groupnum" type="groupnum" id="inputGroupnum"
            class="form-control" placeholder="Group number" required> 
            <br/>
            </section> 

            <!--
            <button class="btn btn-lg btn-primary btn-block" type="submit" @release="createAccount">
            Sign in
            </button> -->

            
            <button class="btn btn-lg btn-primary btn-block" type="button" @click="createUser">
            Create
            </button>
            
            <button class="btn btn-lg btn-primary btn-block" type="button" @click="routeLogin">
            Back to login
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

            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var heroku_uri = 
                ws_scheme + "://heroku-mrp-backend.herokuapp.com/ws/connect/";
            var local_uri = 
                ws_scheme + "://" + window.location.hostname + ":9000/ws/connect/";

            if(process.env.NODE_ENV == "production") {
                var uri = heroku_uri
            }
            else {
                uri = local_uri
            }

            app.$store.state.websocket = new WebSocket(uri);

            app.$store.state.websocket.onmessage = function(event) {
                var data = JSON.parse(event.data);
                /* eslint-disable no-console */
                console.log("server response: ", data);
                /* eslint-enable no-console */

                // If successful login, redirect to map component
                if(data.type == 'create_success'){                    
                    app.$router.replace('login');
                } else if (data.error == 'error') {
                    alert(data.message);
                }
            };

            app.$store.state.websocket.onclose = function(event) {
                /* eslint-disable no-console */
                console.error('socket closed unexpectedly!', event.code);
                /* eslint-enable no-console */
            };

            app.$store.state.websocket.onopen = function() {
                /* After connection has opened we send authentication credentials. The type key helps back-end identify what the client wants to do, similar to HTTP requests GET,POST etc. */
                app.$store.state.websocket.send(JSON.stringify({
                    'type': 'create_account',
                    'username': app.username, 
                    'password': app.password,
                    'groupnum': app.groupnum,
                    'name': app.groupnum
                }))
            };

            app.$store.state.websocket.onerror = function(event) {
                alert("Socket unable to connect to server. Code: " + event)
            }
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