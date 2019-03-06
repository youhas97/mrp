<template>
    <div class="login-wrapper border border-light">
        <form class="form-signin" @submit.prevent="login">
            <h2 class="form-signin-heading">Please sign in</h2>
            <section>
            <label for="inputEmail" class="sr-only">Email address</label> <br/>
            <input v-model="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autgofocus>
            </section><section>
            <label for="inputPassword" class="sr-only">Password</label> <br/>
            <input v-model="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required> <br/>
            <button class="btn btn-lg btn-primary btn-block" type="submit"
            v-on:release="login()">Sign in</button>
            </section>
        </form>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return{
            email: '',
            password:''
        }
    },
    methods: {
        login(){
            /* eslint-disable no-console */
            console.log("email:", this.email);
            console.log("pw:", this.password);
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
    margin: 12px;
    font-size: 100%;
    border-radius: 30px 10px;
    padding-left: 25px;
    padding-right: 25px;
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


