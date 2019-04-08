<template>
    <div id="login" class="login-wrapper border border-light">
        <img alt="MRP Logo" src="../assets/logo.png">
        <form class="form-signin"
        @submit.prevent="login">
            <h2 class="form-signin-heading">
            Please sign in
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

            <button class="btn btn-lg btn-primary btn-block" type="submit" @release="login">
            Sign in
            </button>

            <!--
            <button class="btn btn-lg btn-primary btn-block" type="button" @click="create">
            Create user
            </button>
            -->

        </form>

    </div>
</template>

<script>
export default {
    name: 'LogIn',
    data: function(){
        return {
            username: '',
            password:'',
        }
    },
    methods: {
        login: function(){
            /* eslint-disable no-console */
            console.log("username:", this.username);
            console.log("pw:", this.password);
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
                if(data.type == 'success'){                    
                    app.$router.replace('map');
                    app.$store.state.meObj = {
                        'id': data.id,
                        'pos' : data.pos,
                        'name' : data.name,
                        'group' : data.group,
                        'needHelp' : data.needHelp
                    }
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
                    'type': 'authorization',
                    'username': app.username, 
                    'password': app.password
                }))
            };

            app.$store.state.websocket.onerror = function(event) {
                alert("Socket unable to connect to server. Code: " + event)
            }

            // AUTHENTICATION WITH HTTP REQUEST ---------------------------------------------


            /*var credentials = this.username + ":" + this.password;
            /*
            Converts bytes from a string to a base64-encoded string. Every character in the string therefore needs to be exactly one byte to encode correctly. 
            */
            /*var base64creds = btoa(credentials); 
            var authHeader = " Basic " + base64creds;

            let that = this;
            var loginRequest = new XMLHttpRequest();
            loginRequest.onreadystatechange = function() {
                // TODO: Redirect to main page after success
                if (this.readyState == 4 && this.status == 200) {
                    that.$router.replace('map')
                }
                else if (this.readyState == 4 && this.status != 200){
                    alert('Incorrect username or password, please try again!')
                }

                /* eslint-disable no-console */
                //console.log("rdy-state: " + this.readyState)
                //console.log("status: " + loginRequest.status);
                //console.log(loginRequest.responseText);
                /* eslint-enable no-console */
            /*};
            loginRequest.open("GET", "http://127.0.0.1:9000/connect/login/", true);
            loginRequest.setRequestHeader("Authorization", authHeader);
            loginRequest.send();*/
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
#login {
    margin-top: 5%;
}

</style>