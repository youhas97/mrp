<template>
    <div class="login-wrapper border border-light">
        <form class="form-signin" v-on:submit.prevent="login">
            <h2 class="form-signin-heading">
            Please sign in
            </h2>

            <section>
            <label for="inputEmail" class="sr-only"> Email address 
            </label> 
            <br/>

            <input v-model="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autgofocus>
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

            <button class="btn btn-lg btn-primary btn-block" type="submit" v-on:release="login">
            Sign in
            </button>

            <button class="btn btn-lg btn-primary btn-block" type="button" v-on:click="create">
            Create user
            </button>

        </form>

    </div>
</template>

<script>
export default {
    name: 'LogIn',
    data: function(){
        return {
            email: '',
            password:'',
            creating: false,
        }
    },
    methods: {
        login: function(){
            /* eslint-disable no-console */
            console.log("email:", this.email);
            console.log("pw:", this.password);
            /* eslint-enable no-console */

            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                /*if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("demo").innerHTML =
                    this.responseText;
                }*/
                /* eslint-disable no-console */
                console.log("received response");
                console.log(xhttp.responseText);
                /* eslint-enable no-console */
            };
            xhttp.open("GET", "http://127.0.0.1:8000/connect/login/", true);
            xhttp.send();
            /* eslint-disable no-console */
            console.log("sending http request");
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