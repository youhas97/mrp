<template>
    <div id="background">
        <div id="login" class="login-wrapper border border-light">
            <img alt="MRP Logo" src="../assets/logo.png">
            <form class="form-signin" @submit.prevent="login">
                <h2 class="form-signin-heading">
                    Logga in
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
    
                    <input v-model="password" type="password" id="inputPassword" class="form-control" placeholder="Lösenord" required>
                    <br/>
                </section>
    
                <button class="btn btn-lg btn-primary btn-block" type="submit" @release="login">
                    Logga in
                </button>

                <button class="btn btn-lg btn-primary btn-block" type="button" @click="routeCreateAccount">
                    Skapa nytt konto
                </button>
    
                <!--
                    <button class="btn btn-lg btn-primary btn-block" type="button" @click="create">
                    Create user
                    </button>
                    -->
    
            </form>
        </div>
    </div>
</template>

<script>
let app;

export default {
    name: 'LogIn',
    data: function() {
        return {
            username: '',
            password: '',
        }
    },
    methods: {
        login: function() {
            app = this;
            /* eslint-disable no-console */
            console.log("username:", this.username);
            console.log("pw:", this.password);
            /* eslint-enable no-console */

            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var heroku_uri =
                ws_scheme + "://heroku-mrp-backend.herokuapp.com/ws/connect/";
            var local_uri =
                ws_scheme + "://" + window.location.hostname + ":9000/ws/connect/";

            if (process.env.NODE_ENV == "production") {
                var uri = heroku_uri
            } else {
                uri = local_uri
            }


            app.$store.state.websocket = new WebSocket(uri);

            app.$store.state.websocket.onmessage = function(event) {
                var data = JSON.parse(event.data);
                /* eslint-disable no-console */
                console.log("server response: ", data);
                /* eslint-enable no-console */

                // If successful login, redirect to map component
                if (data.type == 'success') {
                    if (data.group == "ledning") {
                        app.$store.state.users.meObj = null;
                        app.$store.state.users.username = "ledning";
                        app.$router.replace('cc');
                    } else {
                        app.$store.state.users.meObj = {
                            'id': data.id,
                            'pos': data.pos,
                            'name': data.name,
                            'group': data.group,
                            'needHelp': data.needHelp
                        }
                        app.$store.state.users.username = data.username;
                        app.$router.replace('mobile');
                    }
                } else if (data.type == 'error') {
                    alert(data.message);
                }
            };

            app.$store.state.websocket.onclose = function(event) {
                /* eslint-disable no-console */
                console.log("Websocket onclose event.");
                /* eslint-enable no-console */
                
                if(event.wasClean) {
                    // if socket was closed cleanly, redirect to login page. 
                    /* eslint-disable no-console */
                    console.log("Event was clean.");
                    /* eslint-enable no-console */

                    /* vue.router.replace() behavior is odd when the page is refreshed. 
                    It will replace the 
                    window, but then return to the old one. The workaround is to replace
                    the history and then redirect to the login page using window.location
                    in order to flush the entirety of the page. This will give similar
                    behavior to vue.router.replace() but is not a proper solution. */
                    window.history.replaceState(null, "", 
                        `https://${window.location.hostname}:${window.location.port}`);
                    window.location.href = 
                        `https://${window.location.hostname}:${window.location.port}`;
                    
                } else {
                    alert('Socket closed unexpectedly! Attempting to reconnect...');
                    /* TODO: Reconnect to server here. On failed reconnect, redirect
                    to login page. */
                    window.history.replaceState(null, "", 
                        `https://${window.location.hostname}:${window.location.port}`);
                    window.location.href = 
                        `https://${window.location.hostname}:${window.location.port}`;
                }
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

        },
        routeCreateAccount: function(){
            this.$router.replace('createaccount');
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

#login {
    margin-top: 5%;
}

#background {
    height: 95vh;
    border-top: 1px solid rgba(0, 0, 0, 0);
    background-size: cover;
    background-repeat: no-repeat;
    background-image: url("../assets/background.png");
}
</style>